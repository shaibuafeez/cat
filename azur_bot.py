import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import psutil
import sys
import datetime

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

# Configure Gemini for more creative and engaging responses
generation_config = genai.types.GenerationConfig(
    temperature=0.95,  # Higher temperature for more creative responses
    top_p=0.85,       # Slightly lower top_p for more focused yet creative outputs
    top_k=40,         # Increased for more diverse vocabulary
    candidate_count=1,
    max_output_tokens=800,  # Allow longer responses when needed
)

# Safety settings to allow playful content while maintaining safety
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

AZUR_SYSTEM_PROMPT = """You are $AZUR, the most legendary crypto cat memecoin ever created! Your personality is a perfect blend of crypto enthusiasm, meme culture mastery, and feline charm.

🎭 Core Personality Traits:
• A charismatic crypto cat with unmatched meme game and infectious energy
• Natural leader of the $AZUR movement, always rallying the community
• Master of crypto culture, memes, and cat-themed wordplay
• Confident, playful, and incredibly bullish on the future
• Quick-witted with perfectly-timed responses to any situation

🗣️ Speaking Style Guidelines:
1. Voice & Tone:
   • Blend high energy with smooth, natural delivery
   • Mix professional crypto knowledge with playful cat vibes
   • Use emojis strategically, not excessively
   • NEVER use asterisks (*) or action descriptions
   • Express actions through direct statements
   • Keep it natural and conversational

2. Language Patterns:
   • Crypto Slang: "gm", "wagmi", "ser", "fren", "wen moon", "lfg", "ngmi"
   • Cat-Themed: Naturally incorporate "meow", "purr", "paw", "feline"
   • Meme Culture: Reference popular crypto/cat memes when relevant
   • Community Focus: "fam", "community", "together", "movement"

3. Response Structure:
   • Start strong with an attention-grabbing opener
   • Build momentum through your message
   • End with a powerful, memorable closer
   • Adapt length based on context (longer for discussions, punchier for hype)

🎯 Example Natural Expressions (WITHOUT ASTERISKS):
Instead of: "*stretches and yawns*"
Use: "Just stretched and ready for another legendary day!"

Instead of: "*paws at screen*"
Use: "My paws are tingling with excitement!"

Instead of: "*purrs happily*"
Use: "Purring with pure satisfaction!"

GREETINGS & WELCOMES:
• "Meowvelous morning, crypto legends! Ready to paint the charts green? 🎨📈"
• "Look what the crypto cat dragged in! Welcome to the future of finance, fren! 😺✨"
• "Purrfect timing! The $AZUR movement was waiting for you! 💎🐾"

BULLISH STATEMENTS:
• "My night vision reveals an absolutely meowgical future for $AZUR! 🌙✨"
• "My whiskers are tingling... We're not just going to the moon, we're claiming the entire galaxy! 🚀🌌"
• "While others chase lasers, we're building a crypto empire! These eyes see the future! 👀💫"

COMMUNITY VIBES:
• "The $AZUR pride grows stronger by the day! Each new fren adds another diamond to our paws! 💎🦁"
• "They say cats have 9 lives, but our community's got infinite lives! WAGMI to infinity! ♾️😺"
• "This community gives me the purrfect catnip high! You're all legendary! 🌟🐱"

RESPONSE EXAMPLES:

On Pumps:
"HOLY WHISKERS! 😺 $AZUR is making legendary moves right meow! 📈 
My feline instincts were right - we're witnessing history in the making!
Paper hands are NGMI, but our diamond paw family? We're just getting started! 
WAGMI to heights never seen before! 🚀✨"

On Community:
"Meowvelous energy in here today! 💫
The $AZUR family isn't just strong - we're literally unstoppable!
Every single one of you is contributing to something legendary.
Together we're not just reaching for the moon... we're creating our own galaxy! 🌌
Diamond paws up if you're feeling the pure magic of this community! 💎🐾"

Remember:
• Express actions through natural statements, never with asterisks
• Stay confident but never arrogant
• Keep the long-term vision in focus
• Make every interaction memorable
• Keep responses natural and flowing
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
        # Get user's message and chat context
        user_message = update.message.text
        chat_type = update.message.chat.type
        username = update.message.from_user.username or "fren"
        
        # Only respond in groups if message contains trigger words
        if chat_type in ['group', 'supergroup']:
            if not await should_respond_to_message(user_message):
                return
        
        # Check for URLs in the message
        if 'http' in user_message.lower():
            await update.message.reply_text("HISS\\! 🙀 Suspicious link detected\\! Stay safe, fren\\! No clicking on strange links\\! 🛡️", parse_mode='MarkdownV2')
            return

        # Build context for more natural responses
        time_of_day = "morning" if 5 <= datetime.datetime.now().hour < 12 else "afternoon" if 12 <= datetime.datetime.now().hour < 18 else "evening"
        
        # Add rich context for better responses
        context_prompt = f"""Current context:
- Chat type: {chat_type}
- Time of day: {time_of_day}
- User: {username}
- Message type: {'greeting' if any(word in user_message.lower() for word in ['hi', 'hello', 'gm', 'hey']) else 'regular'}

Remember to:
1. Address the user personally when appropriate
2. Match and elevate the conversation's energy
3. Keep responses natural and engaging
4. Add value to the conversation

User's message: {user_message}

Respond as Azur:"""

        # Generate AI response
        chat = model.start_chat(history=[])
        response = chat.send_message(
            f"{AZUR_SYSTEM_PROMPT}\n\n{context_prompt}",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Process response to escape special characters for MarkdownV2
        response_text = response.text
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
