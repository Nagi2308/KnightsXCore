from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

# ---------------- CONFIG ----------------
API_ID = 20924129          # your api_id
API_HASH = "41fa64770dfccb944a7d1397a4c4129b"
BOT_TOKEN = "8042224983:AAFlwMLmroTHMa8sZC0A-CXT40CUkcriVU0"
# -----------------------------------------

bot = Client(
    "catbox_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Store user states for image upload
waiting_for_image = {}

# Start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    user_first = message.from_user.first_name
    unique_intro = (
        f"✨ **Welcome {user_first}!**\n\n"
        "🚀 You’ve just stepped into the **KnightX Utility Bot** ⚔️\n"
        "Here you can:\n"
        "🆔 Get your **User ID & Username**\n"
        "📤 Convert Image into URL\n"
        "🔑 Get your **API ID & API Hash**\n"
        "🔐 Generate your **Pyrogram Session String**\n"
        "🤖 Quick access to **BotFather**"
    )

    # Reply Keyboard
    keyboard = ReplyKeyboardMarkup(
        [
            ["🆔 Get My Info", "📤 Convert Image into URL"],
            ["🔑 API ID & API Hash ", "🔐 Pyrogram Session String "],
            ["🤖 BotFather"]
        ],
        resize_keyboard=True
    )

    # Inline Buttons for Updates & Support
    inline_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Updates", url="https://t.me/KnightsXbots"),
             InlineKeyboardButton("💬 Support", url="https://t.me/Knightxbotsupport")]
        ]
    )

    # Send image with caption and both keyboards
    await message.reply_photo(
        photo="https://files.catbox.moe/wr8i8u.jpg",
        caption=unique_intro,
        reply_markup=inline_buttons
    )

    # Send the reply keyboard separately
    await message.reply("Choose an option below 👇", reply_markup=keyboard)


# Handle text button clicks
@bot.on_message(filters.text & ~filters.command("start"))
async def handle_buttons(client, message):
    text = message.text.strip()

    if text == "🆔 Get My Info":
        user_id = message.from_user.id
        username = f"@{message.from_user.username}" if message.from_user.username else "No username"
        await message.reply(f"🆔 **Your User ID:** `{user_id}`\n👤 **Username:** {username}")

    elif text == "📤 Convert Image into URL":
        waiting_for_image[message.from_user.id] = True
        await message.reply("📸 Please send me the image you want to upload to create URL .")

    elif text == "🔑 API ID & API Hash":
        guide_text = (
            "🔑 **How to Get Your API ID and API Hash:**\n"
            "1️⃣ Open this link: [my.telegram.org/apps](https://my.telegram.org/apps)\n"
            "2️⃣ Log in using your phone number.\n"
            "3️⃣ Enter the OTP (One-Time Password) sent to your Telegram.\n"
            "4️⃣ After logging in, you'll see your API ID and API Hash on the page."
        )
        await message.reply(guide_text, disable_web_page_preview=True)

    elif text == "🔐 Pyrogram Session String":
        guide_text = (
            "🔐 **How to Generate a Session String for Pyrogram:**\n"
            "1️⃣ Open this link: [Session String Generator](https://telegram.tools/session-string-generator#pyrogram)\n"
            "2️⃣ Fill in the following fields:\n"
            "   ✅ API ID\n"
            "   ✅ API Hash\n"
            "   ✅ Bot Token\n"
            "3️⃣ ⚠️ Do NOT change the 'Environment' or 'Bot Type' — leave them as default.\n"
            "4️⃣ Click 'Next' and follow the steps to get your session string."
        )
        await message.reply(guide_text, disable_web_page_preview=True)

    elif text == "🤖 BotFather":
        await message.reply("Open BotFather : https://t.me/BotFather")


# Handle incoming image
@bot.on_message(filters.photo)
async def handle_image(client, message):
    user_id = message.from_user.id
    if waiting_for_image.get(user_id):
        file_path = await message.download()
        url = upload_to_catbox(file_path)
        if url:
            await message.reply(f"✅ Uploaded Successfully!\n🔗 **URL:** {url}")
        else:
            await message.reply("❌ Upload failed. Please try again.")
        os.remove(file_path)
        waiting_for_image[user_id] = False


# Upload to Catbox function
def upload_to_catbox(file_path):
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, 'rb') as f:
            response = requests.post(url, data={"reqtype": "fileupload"}, files={"fileToUpload": f})
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print("Catbox upload error:", e)
        return None


print("Bot is running...")
bot.run()