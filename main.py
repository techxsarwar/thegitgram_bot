import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import User, Base, engine

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

# Try to create tables right at the start
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected and tables verified!")
except Exception as e:
    print(f"❌ DATABASE CONNECTION FAILED: {e}")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# FSM for Login
class LoginStates(StatesGroup):
    waiting_for_token = State()

# The State Map: Maps Telegram message_id -> GitHub Issue Data
issue_map = {} 

def get_issue_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔒 Close", callback_data="close_issue"),
            InlineKeyboardButton(text="🙋 Assign Me", callback_data="assign_issue"),
        ],
        [
            InlineKeyboardButton(text="🪲 Bug", callback_data="label_bug"),
            InlineKeyboardButton(text="✨ Feature", callback_data="label_feature"),
        ]
    ])
    return keyboard

# --- COMMANDS ---
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Welcome to **TheGitGram Bot**! Use /login to link your GitHub account and start receiving alerts.")

@router.message(Command("login"))
async def login_handler(message: Message, state: FSMContext):
    await message.answer("Please send your **GitHub Personal Access Token (PAT)**. 🛡️\n"
                         "Make sure it has 'repo' and 'notifications' scopes.")
    await state.set_state(LoginStates.waiting_for_token)

@router.message(LoginStates.waiting_for_token)
async def process_token(message: Message, state: FSMContext):
    token = message.text.strip()
    
    # 1. Validate Token with GitHub API
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            github_user = response.json()
            github_username = github_user["login"]
            
            # 2. Save to DB
            with Session(engine) as session:
                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
                if not user:
                    user = User(telegram_id=message.from_user.id, github_token=token, username=github_username)
                    session.add(user)
                else:
                    user.github_token = token
                    user.username = github_username
                session.commit()
            
            await message.answer(f"✅ Success! Connected to GitHub as **@{github_username}**.\nYou will now receive alerts for your repositories.")
            await state.clear()
        else:
            await message.answer("❌ Invalid token or error connecting to GitHub. Please try again with a valid PAT.")

# --- HELPERS ---
def get_user_by_github_login(github_login: str):
    with Session(engine) as session:
        return session.query(User).filter(User.username.ilike(github_login)).first()

def get_user_by_telegram_id(telegram_id: int):
    with Session(engine) as session:
        return session.query(User).filter_by(telegram_id=telegram_id).first()

from typing import Optional, Any, Dict, Tuple

# --- GITHUB API HELPER ---
async def github_request(method: str, url: str, token: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[Optional[httpx.Response], Optional[str]]:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
    response = None
    error = None
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=payload)
            elif method.upper() == "PATCH":
                response = await client.patch(url, headers=headers, json=payload)
            
            if response is None:
                error = "Unsupported method or failed to get response"
    except Exception as e:
        error = str(e)
    
    return response, error

# --- CALLBACK HANDLERS: Inline Buttons ---
@dp.callback_query()
async def process_callback(callback_query: CallbackQuery):
    user = get_user_by_telegram_id(callback_query.from_user.id)
    if not user:
        await callback_query.answer("Please /login first.", show_alert=True)
        return

    message_id = callback_query.message.message_id
    if message_id not in issue_map:
        await callback_query.answer("Issue data not found.", show_alert=True)
        return

    issue_data = issue_map[message_id]
    owner = issue_data['owner']
    repo = issue_data['repo']
    issue_num = issue_data['issue_number']
    
    action = callback_query.data
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_num}"
    
    method = "PATCH" if action == "close_issue" else "POST"
    payload = {}
    
    if action == "close_issue":
        payload = {"state": "closed"}
    elif action == "assign_issue":
        url = f"{url}/assignees"
        payload = {"assignees": [user.username]}
    elif action.startswith("label_"):
        label = action.replace("label_", "")
        url = f"{url}/labels"
        payload = {"labels": [label]}

    response, error = await github_request(method, url, user.github_token, payload)
    
    if error or response is None:
        msg = f"⚠️ System error: {error or 'No response'}"
    elif response.status_code in [200, 201]:
        success_msgs = {
            "close_issue": "✅ Issue closed!",
            "assign_issue": "🙋 Assigned to you!",
            "label_": f"🏷️ Label added!"
        }
        key = "label_" if action.startswith("label_") else action
        msg = success_msgs.get(key, "✅ Action completed!")
    else:
        msg = f"❌ GitHub Error: {response.status_code} - {response.text[:50]}"

    await callback_query.answer(msg)

# --- OUTGOING ---
@dp.message(F.reply_to_message)
async def reply_to_github(message: Message):
    user = get_user_by_telegram_id(message.from_user.id)
    if not user: return

    original_msg_id = message.reply_to_message.message_id
    if original_msg_id in issue_map:
        issue_data = issue_map[original_msg_id]
        url = f"https://api.github.com/repos/{issue_data['owner']}/{issue_data['repo']}/issues/{issue_data['issue_number']}/comments"
        
        response, error = await github_request("POST", url, user.github_token, {"body": message.text})
        
        if error or response is None:
            await message.reply(f"⚠️ System error: {error or 'No response'}")
        elif response.status_code == 201:
            await message.reply("✅ Comment posted!")
        else:
            await message.reply(f"❌ Failed: {response.status_code} - {response.text[:50]}")

from aiogram import Bot, Dispatcher, F, Router, types

# --- INCOMING: Telegram Webhook ---
@app.post("/tg-webhook")
async def telegram_webhook(request: Request):
    """
    Handle incoming Telegram updates via Webhook.
    """
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# --- LIFESPAN & STARTUP ---
@app.on_event("startup")
async def on_startup():
    # Set the webhook URL (ensure this matches your Render URL)
    webhook_url = "https://thegitgram-bot.onrender.com/tg-webhook"
    await bot.set_webhook(url=webhook_url)
    print(f"🚀 Telegram Webhook set to: {webhook_url}")
    
    # Magic Line for the database
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected and tables verified!")
    except Exception as e:
        print(f"❌ DATABASE CONNECTION FAILED: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # No polling needed for webhooks!
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/github-webhook")
async def handle_github_webhook(request: Request):
    payload = await request.json()
    action = payload.get("action")
    
    # Identify the Repository Owner
    owner_name = payload.get("repository", {}).get("owner", {}).get("login")
    print(f"🚀 WEBHOOK RECEIVED! Repo Owner: {owner_name}")
    
    if "issue" in payload and action in ["opened", "created"]:
        repo_name = payload["repository"]["name"]
        issue_title = payload["issue"]["title"]
        issue_num = payload["issue"]["number"]
        
        # Route to Correct User (Case-Insensitive)
        user = get_user_by_github_login(owner_name)
        if not user:
            print(f"❌ DATABASE MATCH FAILED: Could not find user '{owner_name}' in Supabase.")
            return {"status": "ignored"}

        print(f"✅ MATCH FOUND: Sending to Telegram ID {user.telegram_id}")

        if "comment" in payload:
            author = payload["comment"]["user"]["login"]
            body = payload["comment"]["body"]
            header = f"💬 <b>Comment on Issue #{issue_num}</b>"
        else:
            author = payload["issue"]["user"]["login"]
            body = payload["issue"]["body"]
            header = f"🚨 <b>New Issue in {repo_name}</b>"
        
        text = f"{header}\n<b>Title:</b> {issue_title}\n<b>By:</b> {author}\n\n{body}"
        
        try:
            sent_msg = await bot.send_message(
                chat_id=user.telegram_id, 
                text=text, 
                parse_mode="HTML",
                reply_markup=get_issue_keyboard()
            )
            issue_map[sent_msg.message_id] = {"owner": owner_name, "repo": repo_name, "issue_number": issue_num}
        except Exception as e:
            print(f"Error sending message to {user.telegram_id}: {e}")
            
    return {"status": "received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
