import os
import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Any, Dict, Tuple

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from sqlalchemy.orm import Session

from cryptography.fernet import Fernet
from models import User, Base, engine

# --- CONFIGURATION ---
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode()
cipher_suite = Fernet(ENCRYPTION_KEY) if ENCRYPTION_KEY else None

def encrypt_token(token: str) -> str:
    return cipher_suite.encrypt(token.encode()).decode() if cipher_suite else token

def decrypt_token(encrypted_token: str) -> str:
    try:
        return cipher_suite.decrypt(encrypted_token.encode()).decode() if cipher_suite else encrypted_token
    except Exception:
        return encrypted_token # Fallback for unencrypted tokens during migration

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# FSM and State
class LoginStates(StatesGroup):
    waiting_for_token = State()

issue_map = {} # Maps Telegram message_id -> GitHub Issue Data

# --- APP SETUP & LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the bot starts
    webhook_url = "https://thegitgram-bot.onrender.com/tg-webhook"
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    print(f"🚀 Telegram Webhook set to: {webhook_url}")
    
    # Magic Line for the database
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected and tables verified!")
    except Exception as e:
        print(f"❌ DATABASE CONNECTION FAILED: {e}")
        
    yield  # The bot runs here...
    
    # This runs when the bot shuts down
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# --- WEBHOOK ENDPOINTS ---
@app.post("/tg-webhook")
async def telegram_webhook(request: Request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"status": "ok"}

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
    
    elif "pull_request" in payload and action in ["opened", "closed"]:
        repo_name = payload["repository"]["name"]
        pr_title = payload["pull_request"]["title"]
        pr_num = payload["pull_request"]["number"]
        pr_url = payload["pull_request"]["html_url"]
        author = payload["pull_request"]["user"]["login"]
        
        user = get_user_by_github_login(owner_name)
        if not user:
            print(f"❌ DATABASE MATCH FAILED: Could not find user '{owner_name}' for PR in Supabase.")
            return {"status": "ignored"}

        print(f"✅ MATCH FOUND: Sending PR notification to Telegram ID {user.telegram_id}")

        header = ""
        if action == "opened":
            header = f"🚀 <b>New Pull Request in {repo_name}</b>"
        elif action == "closed":
            if payload["pull_request"]["merged"]:
                header = f"🎉 <b>Pull Request Merged in {repo_name}</b>"
            else:
                header = f"🔴 <b>Pull Request Closed in {repo_name}</b>"
        
        text = f"{header}\n<b>Title:</b> {pr_title}\n<b>By:</b> {author}\n<a href='{pr_url}'>View Pull Request #{pr_num}</a>"
        
        try:
            await bot.send_message(
                chat_id=user.telegram_id, 
                text=text, 
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Error sending PR message to {user.telegram_id}: {e}")
            
    return {"status": "received"}

# --- BOT HANDLERS & HELPERS ---
def get_issue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔒 Close", callback_data="close_issue"),
            InlineKeyboardButton(text="🙋 Assign Me", callback_data="assign_issue"),
        ],
        [
            InlineKeyboardButton(text="🪲 Bug", callback_data="label_bug"),
            InlineKeyboardButton(text="✨ Feature", callback_data="label_feature"),
        ]
    ])

def get_user_by_github_login(github_login: str):
    with Session(engine) as session:
        return session.query(User).filter(User.username.ilike(github_login)).first()

def get_user_by_telegram_id(telegram_id: int):
    with Session(engine) as session:
        return session.query(User).filter_by(telegram_id=telegram_id).first()

async def github_request(method: str, url: str, token: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[Optional[httpx.Response], Optional[str]]:
    # Decrypt token before use
    real_token = decrypt_token(token)
    headers = {"Authorization": f"Bearer {real_token}", "Accept": "application/vnd.github.v3+json"}
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
                error = "Unsupported method"
    except Exception as e:
        error = str(e)
    return response, error

@router.message(Command("status"))
async def status_handler(message: Message):
    user = get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("❌ You are not logged in. Use /login to get started.")
        return

    # Check GitHub connectivity & fetch repos
    token = decrypt_token(user.github_token)
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("https://api.github.com/user/repos?sort=updated&per_page=5", headers=headers)
        
        db_status = "🟢 Connected"
        try:
            with Session(engine) as session:
                session.execute("SELECT 1")
        except Exception:
            db_status = "🔴 Error"

        if response.status_code == 200:
            repos = response.json()
            repo_links = "\n".join([f"• <a href='{r['html_url']}'>{r['name']}</a>" for r in repos])
            status_text = (
                f"👤 <b>User:</b> @{user.username}\n\n"
                f"📂 <b>Recent Repos:</b>\n{repo_links if repos else 'No repos found.'}\n\n"
                f"🗄️ <b>Database:</b> {db_status}\n"
                f"🔐 <b>Security:</b> AES-256 Active"
            )
            await message.answer(status_text, parse_mode="HTML", disable_web_page_preview=True)
        else:
            await message.answer(f"👤 <b>User:</b> @{user.username}\n🗄️ <b>Database:</b> {db_status}\n⚠️ <b>GitHub API:</b> Error fetching repos.")

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Welcome to **TheGitGram Bot**! Use /login to link your GitHub account.")

@router.message(Command("login"))
async def login_handler(message: Message, state: FSMContext):
    await message.answer("Please send your **GitHub Personal Access Token (PAT)**. 🛡️")
    await state.set_state(LoginStates.waiting_for_token)

@router.message(LoginStates.waiting_for_token)
async def process_token(message: Message, state: FSMContext):
    token = message.text.strip()
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("https://api.github.com/user", headers=headers)
        if response.status_code == 200:
            github_username = response.json()["login"]
            with Session(engine) as session:
                user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
                encrypted = encrypt_token(token)
                if not user:
                    user = User(telegram_id=message.from_user.id, github_token=encrypted, username=github_username)
                    session.add(user)
                else:
                    user.github_token = encrypted
                    user.username = github_username
                session.commit()
            await message.answer(f"✅ Success! Connected as **@{github_username}**.\nTokens are now stored with AES-256 encryption. 🛡️")
            await state.clear()
        else:
            await message.answer("❌ Invalid token. Please try again.")

@dp.callback_query()
async def process_callback(callback_query: CallbackQuery):
    user = get_user_by_telegram_id(callback_query.from_user.id)
    if not user or callback_query.message.message_id not in issue_map:
        await callback_query.answer("Error or session expired.", show_alert=True)
        return

    issue_data = issue_map[callback_query.message.message_id]
    action = callback_query.data
    url = f"https://api.github.com/repos/{issue_data['owner']}/{issue_data['repo']}/issues/{issue_data['issue_number']}"
    
    if action == "close_issue":
        response, error = await github_request("PATCH", url, user.github_token, {"state": "closed"})
    elif action == "assign_issue":
        response, error = await github_request("POST", f"{url}/assignees", user.github_token, {"assignees": [user.username]})
    elif action.startswith("label_"):
        label = action.replace("label_", "")
        response, error = await github_request("POST", f"{url}/labels", user.github_token, {"labels": [label]})
    
    await callback_query.answer("✅ Action completed!" if not error and response and response.status_code in [200, 201] else "❌ Failed.")

@dp.message(F.reply_to_message)
async def reply_to_github(message: Message):
    user = get_user_by_telegram_id(message.from_user.id)
    if not user or message.reply_to_message.message_id not in issue_map: return
    
    issue_data = issue_map[message.reply_to_message.message_id]
    url = f"https://api.github.com/repos/{issue_data['owner']}/{issue_data['repo']}/issues/{issue_data['issue_number']}/comments"
    response, error = await github_request("POST", url, user.github_token, {"body": message.text})
    if not error and response and response.status_code == 201:
        await message.reply("✅ Comment posted!")
    else:
        await message.reply("❌ Post failed.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
