import discord
import requests
from discord.ext import commands
from discord import app_commands
import json



def run_discord_bot():
    TOKEN = ""
    API_URL = "https://east.albion-online-data.com/api/v2/stats/prices/"
    AUTOCOMPLETE_FILE = 'auto_complete.json'

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    @bot.command()
    async def autocomplete(ctx, item):
        # Load the autocomplete items from JSON file
        with open(AUTOCOMPLETE_FILE, 'r') as file:
            autocomplete_data = json.load(file)

        # Get the matching items and send the suggestions to the Discord channel
        matching_items = [
            key for key in autocomplete_data if item.lower() in key.lower()]
        await ctx.send('\n'.join(matching_items))


    @bot.command()
    async def price(ctx, item):
        # Load the autocomplete items from JSON file
        with open(AUTOCOMPLETE_FILE, 'r') as file:
            autocomplete_data = json.load(file)

        # Find the selected item and get its corresponding value
        selected_item = next((value for key, value in autocomplete_data.items(
        ) if key.lower() == item.lower()), None)

        if selected_item:
            # Call the API with the selected item's value
            response = requests.get(API_URL, params={'item': selected_item})

            # Get the API response message
            api_message = response.json()

            print (api_message)

            # Send the API message to the Discord channel
            await ctx.send(api_message)
        else:
            await ctx.send("Item not found.")

    # Run the Discord bot
    bot.run(TOKEN)


if __name__ == "__main__":
    run_discord_bot()
