import discord
import os
from dotenv import load_dotenv
import google.generativeai as genai
from discord.ext import commands

load_dotenv()

# Configure API keys
discord_token = os.getenv("DISCORD_TOKEN")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='~', intents=intents)


# When bot is ready to be used
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='chatbot')
async def chatbot(ctx, *, prompt: str):
    if not prompt:
        await ctx.send("Please provide a prompt")
        return
    try:
        # Call Gemini API
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)

        if prompt and hasattr(response, 'text'):
            response_text = response.text
            # Discord message limit
            for chunk in [response_text[i:i + 1900] for i in range(0, len(response_text), 1900)]:
                await ctx.send(chunk)

    except Exception as e:
        await ctx.send(f"an error occurred while processing your request: {e}")

        #answer = response['choices'][0]['message']['content'].strip()

bot.run(discord_token)
