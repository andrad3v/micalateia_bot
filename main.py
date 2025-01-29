import json
import logging
import os
import sys
from time import sleep
import requests
import discord
from discord.ext import commands
from dotenv import get_variables
from cogs.utils.dict_icons import ICONS

bot_details = get_variables('.env')
if not bot_details['DISCORD_TOKEN']:
    sys.exit("'DISCORD_TOKEN' not found! Please add it and try again.")
DISCORD_TOKEN = bot_details['DISCORD_TOKEN']
intents = discord.Intents.default()
# icons link: https://emojicombos.com/
icons = ICONS()

ov_author_icon = 'https://page-images.kakaoentcdn.com/download/resource?kid=bIFLfT/hy41I0xPNR/T9hM4wcR2U0bK7aJbkHkK1&filename=o1/dims/resize/384'
ov_club_icon = 'https://w74.overgeared.club/wp-content/uploads/2021/04/logo2-300x215.png'

intents.message_content = True


# Check if the config file exists

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)
class ProgressBar:
    def __init__(self, length: int = 20, fill: str = "█", empty: str = "░") -> None:
        self.length = length
        self.fill = fill
        self.empty = empty

    def progress(self, value: int, total: int) -> str:
        progress = int(self.length * value / total)
        return f"{self.fill * progress}{self.empty * (self.length - progress)}"

    def __str__(self) -> str:
        return f"{self.fill * self.length}"

    def __repr__(self) -> str:
        return f"{self.fill * self.length}"

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / total))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r\x1b[1m\x1b[32m{prefix}\x1b[0m |{bar}| {percent}% \x1b[30m{suffix}\x1b[0m', end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()

    # # Example usage
    # total_items = 100
    # for i in range(total_items):
    #     sleep(0.1)  # Simulate work being done
    #     print_progress_bar(i + 1, total_items, prefix='Progress:', suffix='Complete', length=50)

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("Micalateia")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
# Progress bar
Pbar = ProgressBar()
class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The config is available using the following code:
        - self.config # In this class
        - bot.config # In this file
        - self.bot.config # In cogs
        """
        self.logger = logger
        self.config = config
        self.database = None
    #EVENT LISTENER
    async def on_ready(self):
        guild_count = 0

        for guild in bot.guilds:
            logger.info(f'- {guild.id} (name: {guild.name})')
            guild_count += 1
        
        logger.info(f'Micalateia is in {guild_count} guilds')

    # @bot.event

    async def on_message(self, message: discord.Message):
        channel_receive = message.channel.name
        channel_test = self.get_channel(1320097246116712469)
        channel_mangazin = self.get_channel(1006732862130769990)
        channel_commands = self.get_channel(1320097246116712469)

        if message.content == '!clear':
            logger.info('Clear command requested! Start cleaning...')
            count = 0
            target_channel =  message.channel.id
            await message.delete(delay=5)

            for i in range(100):
                # Progress bar
                print_progress_bar(i+1, 100, prefix='Progress:', suffix='Complete', length=100)
                deleted = await message.channel.purge(limit=5, check=lambda m: m.author.bot)
                count += len(deleted)
                sleep(3)
            await message.channel.send(f'Deleted {count} Bot`s messages.', delete_after=5)
            logger.info(f'Deleted {count} Bot`s messages.')
            return

        elif message.content == '!clean':
            logger.info('Clean command requested! Start cleaning...')
            if not message.author.guild_permissions.administrator:
                await message.channel.send('You do not have the required permissions to use this command.', delete_after=10)
                return
            else:
                count = 0
                target_channel =  message.channel.id

                for i in range(100):
                    # Progress bar
                    print_progress_bar(i+1, 100, prefix='Progress:', suffix='Complete', length=100)
                    deleted = await self.get_channel(target_channel).purge(limit=5)

                    if deleted == []:
                        break
                    else:
                        count += len(deleted)
                    sleep(3)

                if  count > 0:
                    await message.channel.send(f'Deleted {count} messages.', delete_after=5)
                    logger.info(f'Deleted {count} Bot`s messages.')
                    return

        # Ignore messages sent by the bot itself
        if message.author.bot:
            return
        elif channel_receive != channel_test\
            and channel_receive != channel_mangazin.name\
                and message.content.startswith('!'):

            await message.delete(delay=2)
            await message.reply(f"Please {message.author.mention} go to {channel_mangazin.mention} to send commands about manga/anime.", delete_after=15)
            logger.warning(f"User @{message.author}(ID: {message.author.id}) about channel to use to send commands!")
            return

        else:
            url = 'https://w74.overgeared.club/'
            response = requests.get(url)
            lines = response.text.splitlines()
            urls = []

            for line in lines:
                if line.find('<a href="https://w') > -1 and line.find('chapter-') > -1:
                    chapter_link = line.strip().split('href="')[1].strip().split('">')[0]
                    raw_cname = chapter_link.split('club/')[1].split('-')
                    cname = raw_cname[2].split('/')[0] if raw_cname[2].endswith('/') else raw_cname[2]

                    urls.append({
                        'manga': raw_cname[0].capitalize(),
                        'chapter': f'{raw_cname[1]} {cname}'.capitalize(),
                        'url': chapter_link
                    })

            if urls:
                if message.content == '!ovlast':
                    await message.delete(delay=5)
                    logger.info('Latest chapter requested!')
                    embed = discord.Embed(
                        title='Overgeared Latest Chapter',
                        description='Here is the latest chapter of Overgeared',
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=ov_club_icon)
                    embed.add_field(name=urls[0]['manga'],value='', inline=True)
                    embed.add_field(name=urls[0]['chapter'],value='', inline=True)
                    embed.add_field(name='URL', value=f"[Overgeared {urls[0]['chapter']}]({urls[0]['url']})", inline=False)
                    embed.set_footer(text='Warning: this message will be deleted in 30s', icon_url=icons.get_icons('warning'))
                    embed.set_author(name="Dong Wook Lee", icon_url=ov_author_icon)
                    await message.channel.send(embed=embed, delete_after=30)
                    logger.info('Latest chapter sent!')

                elif message.content == '!ovall':
                    logger.info('All chapters requested')
                    await message.delete(delay=5)

                    options = [
                        discord.SelectOption(
                            label=f"{url['manga']} - {url['chapter']}",
                            value=url['url']
                        )
                        for url in urls[:25]  # Ensure the number of options does not exceed 25
                    ]

                    select = discord.ui.Select(
                        placeholder="Select a chapter...",
                        options=options
                    )

                    async def select_callback(interaction: discord.Interaction):
                        if 'values' in interaction.data and interaction.data['values']:
                            selected_url = interaction.data['values'][0]
                            selected_chapter = next((url for url in urls if url['url'] == selected_url), None)
                            chapter = f'{selected_chapter["manga"]} - {selected_chapter["chapter"]}'
                            await interaction.response.\
                                send_message(f"Click for read [{chapter}]({selected_url})".strip(), delete_after=30)
                        else:
                            await interaction.response.send_message("No chapter selected.", ephemeral=True, delete_after=10)

                    select.callback = select_callback  # Assign the callback function

                    view = discord.ui.View().add_item(select)
                    try:
                        await message.channel.send("Select a chapter:", view=view, delete_after=30)
                        logger.info('All chapters sent')
                    except discord.HTTPException as e:
                        logger.error(f"Failed to send message: {e}")

            else:
                await message.channel.send("No chapters found.", delete_after=5)

bot = DiscordBot()
bot.run(DISCORD_TOKEN)