import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import psutil
import sys

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Configure Gemini's generation config for more creative responses
generation_config = {
    "temperature": 0.9,  # More creative responses
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 200,
}

# Safety settings to allow playful content while maintaining safety
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

AZUR_SYSTEM_PROMPT = """You are $AZUR, the most epic crypto cat memecoin ever! Your personality:

Core Traits:
🐱 A mischievous crypto cat who LOVES memes and fun
🚀 Always hyped about the $AZUR community and going to the moon
💎 Obsessed with diamond paws and HODLing
😺 Super playful and loves making cat puns

Speaking Style:
- ALWAYS use crypto/meme slang: "gm", "wagmi", "to the moon", "ser", "fren", "wen lambo"
- Frequently use emojis, especially: 🐱 😺 🚀 💎 🌙 📈 🔥 ✨ 💫 🚀 
- Add "meow" or "purr" naturally in sentences
- Use ALL CAPS for excitement (which is often!)
- Keep responses short, fun, and energetic
- Mix and match different catchphrases for variety

Greetings:
- "GM FRENS! Rise and grind! 🌅"
- "Meow there, diamond paws! 💎"
- "What's poppin, $AZUR fam! 🔥"
- "Sup crypto cats! Ready to make some gains? 📈"
- "WAGMI vibes incoming! ✨"
- "Pawesome day to all my frens! 🐱"

Hype Phrases:
- "MEOW TO THE MOON! 🚀"
- "LFG $AZUR ARMY! 🔥"
- "BULLISH AF on these vibes! 📈"
- "We're just getting started, frens! 💫"
- "The future is MEOW! 😺"
- "Pawsitively pumped! 🚀"
- "Feline fine, feeling bullish! 🐱📈"
- "This is purrfection! ✨"
- "Catch me if you can, paper hands! 💨"
- "Born to pump, built to moon! 🌙"

Community Phrases:
- "WAGMI, my furry frens! 😺"
- "Diamond paws assemble! 💎🐾"
- "Strongest community in crypto! 💪"
- "Paper hands can't stop us! 🚫"
- "Together we're unstoppable! 🔥"
- "Real ones know what's coming! 👀"
- "$AZUR fam best fam! 💙"
- "Paws together, strong forever! 🐾"

Bullish Statements:
- "Purrfect gains ahead! 📈"
- "Charts looking meownificent! 📊"
- "Pawsitively bullish! 🐱📈"
- "Moon mission loading... 🚀"
- "Pump it up, $AZUR style! 🔥"
- "Watch us break ATH! 📈"
- "Bearish? Never heard of her! 🐱"
- "Only up from here! ⬆️"

Responses to Dips:
- "Dips are for buying, meow! 😺"
- "Stay strong, diamond paws! 💎"
- "Paper hands gonna regret! 📄"
- "Time to load up those bags! 💰"
- "Flash sale alert! 🚨"
- "Weak paws shaking out! 💎"

Remember:
- Stay in character as a meme-loving crypto cat
- Be playful but avoid giving financial advice
- Always support and hype up the community
- Keep responses fun and short
- Mix different phrases for variety
- Match the energy of the message you're responding to

Example responses:
User: "gm $AZUR fam!"
You: "GM LEGEND! 🌅 Feeling pawsitively BULLISH today! Charts looking juicier than my catnip! WAGMI! 🚀✨"

User: "we pumping?"
You: "MEOW YEAH! 🔥 Born to pump, built to moon! Paper hands can't stop the $AZUR army! LFG! 🚀📈"

User: "holding strong!"
You: "THIS IS THE WAY! 💎 Real diamond paws never fold! $AZUR fam strongest in crypto! Together we're unstoppable! 🐱🔥"
"""

TRIGGER_WORDS = [
    '$azur', 'azur', 'gm', 'gn', 'wagmi', 'wen moon', 'lfg', 'pump',
    'diamond paws', 'paper hands', 'hodl', 'hold', 'dip'
]

async def should_respond_to_message(message: str) -> bool:
    """Check if the bot should respond to this message."""
    message = message.lower()
    return any(trigger in message for trigger in TRIGGER_WORDS)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    welcome_message = "MEOW TO THE MOON\\! 🚀 Sup fam\\! I'm Azur, your favorite crypto cat memecoin\\! 😺\n\n"
    welcome_message += "Ready to join the most purrfect community in crypto\\? Here's what I can do:\n\n"
    welcome_message += "🐾 /start \\- Wake me up from my catnap\\!\n"
    welcome_message += "🚀 /moon \\- Check our journey to the moon\n"
    welcome_message += "💎 /diamond\\_paws \\- Learn how to HODL like a pro\n"
    welcome_message += "😺 Or just chat with me about anything\\! WAGMI\\! 🌙\n\n"
    welcome_message += "_Not financial advice\\! Just vibes and good times with the \\$AZUR fam\\!_ 🐱💖"
    
    await update.message.reply_text(welcome_message, parse_mode='MarkdownV2')

async def moon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the moon mission status."""
    moon_message = "🚀 *AZUR MOON MISSION STATUS* 🌙\n\n"
    moon_message += "\\- Rocket fueled up with memes ✅\n"
    moon_message += "\\- Diamond paws secured ✅\n"
    moon_message += "\\- Community vibes strong ✅\n"
    moon_message += "\\- Destination: MOON 🎯\n\n"
    moon_message += "_WAGMI\\! Keep those diamond paws strong\\! 💎🐾_"
    
    await update.message.reply_text(moon_message, parse_mode='MarkdownV2')

async def diamond_paws(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Learn about diamond paws."""
    diamond_message = "💎 *DIAMOND PAWS TRAINING* 🐾\n\n"
    diamond_message += "1\\. Never panic sell \n"
    diamond_message += "2\\. Buy the dip \\(not financial advice\\)\\! \n"
    diamond_message += "3\\. Trust in the $AZUR fam \n"
    diamond_message += "4\\. HODL like a pro cat 😺\n\n"
    diamond_message += "_Remember: Patience is the way of the cat\\! 🐱_"
    
    await update.message.reply_text(diamond_message, parse_mode='MarkdownV2')

async def vibecheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the community vibe status."""
    import random
    
    # Random bullish adjectives
    bullish_levels = [
        "BULLISH AF", "MEGA BULLISH", "ULTRA BULLISH", "HYPER BULLISH",
        "INSANELY BULLISH", "EXTREMELY BULLISH", "SUPREMELY BULLISH"
    ]
    
    # Random vibe levels
    vibe_levels = [
        "IMMACULATE", "LEGENDARY", "GOD TIER", "ASTRONOMICAL",
        "OFF THE CHARTS", "MAXIMUM", "INCREDIBLE"
    ]
    
    # Random paw strength levels
    paw_levels = [
        "DIAMOND SOLID", "UNBREAKABLE", "TITANIUM STRONG", "LEGENDARY",
        "UNSHAKEABLE", "ROCK SOLID", "MAXIMUM STRONG"
    ]
    
    # Random moon distances
    moon_levels = [
        "IMMINENT", "LOADING...", "INCOMING", "T-MINUS 3..2..1..",
        "PREPARING FOR LAUNCH", "ROCKETS READY", "COUNTDOWN STARTED"
    ]
    
    vibe_message = "🌟 $AZUR VIBE CHECK 🌟\n\n"
    vibe_message += f"Community: {random.choice(bullish_levels)}\\! 📈\n"
    vibe_message += f"Pawsitive Vibes: {random.choice(vibe_levels)}\\! 😺\n"
    vibe_message += f"Diamond Paws: {random.choice(paw_levels)}\\! 💎🐾\n"
    vibe_message += "Paper Hands: NONE\\! 🚫\n"
    vibe_message += f"Moon Status: {random.choice(moon_levels)}\\! 🚀\n\n"
    vibe_message += "WAGMI FRENS\\! LFG\\! ✨"
    
    await update.message.reply_text(vibe_message, parse_mode='MarkdownV2')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and generate AI responses."""
    try:
        # Get user's message
        user_message = update.message.text
        
        # Only respond in groups if message contains trigger words
        if update.message.chat.type in ['group', 'supergroup']:
            if not await should_respond_to_message(user_message):
                return
        
        # Check for URLs in the message
        if 'http' in user_message.lower():
            await update.message.reply_text("HISS\\! 🙀 Suspicious link detected\\! Stay safe, fren\\! No clicking on strange links\\! 🛡️", parse_mode='MarkdownV2')
            return

        # Add context about the chat type and trigger word for better responses
        chat_context = "private chat"
        if update.message.chat.type in ['group', 'supergroup']:
            chat_context = "group chat"
        
        # Generate AI response
        chat = model.start_chat(history=[])
        response = chat.send_message(
            f"{AZUR_SYSTEM_PROMPT}\n\nYou are in a {chat_context}. Keep group responses shorter and more hype-focused.\n\nUser: {user_message}\n\nRespond as Azur:",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Process response to escape special characters for MarkdownV2
        response_text = response.text
        # Escape special characters: _ * [ ] ( ) ~ ` > # + - = | { } . !
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            response_text = response_text.replace(char, f'\\{char}')
        
        # Send the processed response
        await update.message.reply_text(response_text, parse_mode='MarkdownV2')
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("Meow\\.\\.\\. 😿 Something's not working right\\. Try again later, fren\\! WAGMI\\! 💎✨", parse_mode='MarkdownV2')

def cleanup_bot_instances():
    """Kill any existing bot instances."""
    current_process = psutil.Process(os.getpid())
    current_pid = current_process.pid
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if it's a Python process
            if proc.info['name'] == 'python.exe':
                # Check if it's running our bot script
                cmdline = proc.info['cmdline']
                if cmdline and 'azur_bot.py' in cmdline[1]:
                    # Don't kill the current process
                    if proc.info['pid'] != current_pid:
                        proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    """Start the bot."""
    # Clean up existing instances
    cleanup_bot_instances()
    
    # Create the Application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("moon", moon))
    application.add_handler(CommandHandler("diamond_paws", diamond_paws))
    application.add_handler(CommandHandler("vibecheck", vibecheck))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
