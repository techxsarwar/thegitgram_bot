import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import httpx
from dotenv import load_dotenv

# Load environment variables securely from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GITHUB_PAT = os.getenv("GITHUB_PAT", "").strip()
YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID", "").strip()

# Ensure YOUR_CHAT_ID is an integer
if YOUR_CHAT_ID:
    try:
        YOUR_CHAT_ID = int(YOUR_CHAT_ID)
    except ValueError:
        print("Warning: YOUR_CHAT_ID is not a valid integer.")
        YOUR_CHAT_ID = 0
else:
    YOUR_CHAT_ID = 0

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# The State Map: Maps Telegram message_id -> GitHub Issue Data
issue_map = {} 

# GitHub API Headers
GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json"
}

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

# --- OUTGOING: Telegram to GitHub ---
@dp.message(F.reply_to_message)
async def reply_to_github(message: Message):
    # Ensure this command only works for you
    if message.chat.id != YOUR_CHAT_ID:
        return

    original_msg_id = message.reply_to_message.message_id
    
    if original_msg_id in issue_map:
        issue_data = issue_map[original_msg_id]
        
        url = f"https://api.github.com/repos/{issue_data['owner']}/{issue_data['repo']}/issues/{issue_data['issue_number']}/comments"
        payload = {"body": message.text}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=GITHUB_HEADERS, json=payload)
            
        if response.status_code == 201:
            await message.reply("✅ Reply successfully posted to GitHub!")
        else:
            await message.reply(f"❌ Failed to post. GitHub returned: {response.status_code}")

# --- CALLBACK HANDLERS: Inline Buttons ---
@dp.callback_query()
async def process_callback(callback_query: CallbackQuery):
    if callback_query.message.chat.id != YOUR_CHAT_ID:
        await callback_query.answer("Unauthorized", show_alert=True)
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
    
    async with httpx.AsyncClient() as client:
        if action == "close_issue":
            res = await client.patch(url, headers=GITHUB_HEADERS, json={"state": "closed"})
            msg = "Issue closed!" if res.status_code == 200 else "Failed to close."
        
        elif action == "assign_issue":
            # Get current user's login first
            user_res = await client.get("https://api.github.com/user", headers=GITHUB_HEADERS)
            if user_res.status_code == 200:
                username = user_res.json()["login"]
                assign_url = f"{url}/assignees"
                res = await client.post(assign_url, headers=GITHUB_HEADERS, json={"assignees": [username]})
                msg = "Assigned to you!" if res.status_code == 201 else "Assignment failed."
            else:
                msg = "Could not fetch user info."
        
        elif action.startswith("label_"):
            label = action.replace("label_", "")
            label_url = f"{url}/labels"
            res = await client.post(label_url, headers=GITHUB_HEADERS, json={"labels": [label]})
            msg = f"Label '{label}' added!" if res.status_code == 200 else "Failed to add label."

    await callback_query.answer(msg)
    if "failed" not in msg.lower():
        # Update the message to show the action was taken? 
        # (Optional: we could edit the text or keyboard, but for now just a toast is fine)
        pass

# --- INCOMING: GitHub to Telegram ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Telegram polling...", flush=True)
    # Start the Telegram polling loop when FastAPI starts
    task = asyncio.create_task(dp.start_polling(bot))
    print("Telegram polling started in background.", flush=True)
    yield
    # Clean up when FastAPI shuts down
    print("Stopping Telegram polling...", flush=True)
    task.cancel()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/github-webhook")
async def handle_github_webhook(request: Request):
    payload = await request.json()
    
    # We only care when an issue is opened or a new comment is added
    action = payload.get("action")
    if "issue" in payload and action in ["opened", "created"]:
        repo_name = payload["repository"]["name"]
        owner_name = payload["repository"]["owner"]["login"]
        issue_title = payload["issue"]["title"]
        issue_num = payload["issue"]["number"]
        
        # Differentiate between a new issue and a new comment
        if "comment" in payload:
            author = payload["comment"]["user"]["login"]
            body = payload["comment"]["body"]
            header = f"💬 <b>New Comment on Issue #{issue_num} in {repo_name}</b>"
        else:
            author = payload["issue"]["user"]["login"]
            body = payload["issue"]["body"]
            header = f"🚨 <b>New Issue in {repo_name}</b>"
        
        text = (
            f"{header}\n"
            f"<b>Title:</b> {issue_title}\n"
            f"<b>By:</b> {author}\n\n"
            f"{body}"
        )
        
        sent_msg = await bot.send_message(
            chat_id=YOUR_CHAT_ID, 
            text=text, 
            parse_mode="HTML",
            reply_markup=get_issue_keyboard()
        )
        
        issue_map[sent_msg.message_id] = {
            "owner": owner_name,
            "repo": repo_name,
            "issue_number": issue_num
        }
        
    return {"status": "received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
