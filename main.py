import discord
import os
import openai
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# Configure API keys
discord_token = os.getenv("DISCORD_TOKEN")
genai_api_key = os.getenv("GEMINI_API_KEY")

"""client = discord.Client()
client.run(TOKEN)"""

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='~', intents=intents)

# When bot is ready to be used
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='chatbot')
async def chatbot(ctx, *, prompt):
    if not prompt:
        await ctx.send("what's up?")
        return
    try:
        # Call OpenAI API
        response = openai.Completion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful bot"},
                {"role": "user", "content": "Can you show me an example?"},
                {"role": "system", "content": prompt}
            ],
            max_tokens=160
        )
        answer = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        await ctx.send(f"an error occurred while processing your request: {e}")

bot.run(discord_token)