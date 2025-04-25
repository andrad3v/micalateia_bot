import json
import os
import sys
from tkinter import NO
import requests
import discord
import logging
from time import sleep
from discord.ext import commands
from cogs.starter import initialize
from cogs.api_callers import call_api
from cogs.utils.dict_icons import ICONS
from cogs.system.logger import LoggingFormatter
from cogs.system.progress_bar import ProgressBar
from cogs.utils.apis.api_mangadex import get_last_chapters


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

logger = logging.getLogger("MiK:main")
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
                # print_progress_bar(i+1, 100, prefix='Progress:', suffix='Complete', length=100)
                deleted = await message.channel.purge(limit=5, check=lambda m: m.author.bot)
                count += len(deleted)
                sleep(3)
            await message.channel.send(f'Deleted {count} Bot`s messages.', delete_after=5)
            logger.info(f'Deleted {count} Bot`s messages.')
            return

        elif message.content == '!hp':
            logger.info('Help command requested!')
            await message.delete(delay=5)
            embed = discord.Embed(
                title='Micalateia Help',
                description='Here is the help for Micalateia',
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=ov_club_icon)
            embed.add_field(name='!ovlast', value='Get the latest chapter of Overgeared', inline=False)
            embed.add_field(name='!ovall', value='Get all chapters of Overgeared', inline=False)
            embed.add_field(name='!s [manga_name] [pt-br/en]', value='Get the last 5 chapter of manga you want in the language selected by default return in pt-br', inline=False)
            embed.set_footer(text='Warning: this message will be deleted in 2min', icon_url=icons.get_icons('warning'))
            embed.set_author(name="Cereal_3D", icon_url=ov_author_icon)
            await message.channel.send(embed=embed, delete_after=120)
            logger.info('Help sent!')

        elif message.content == '!ping':
            logger.info('Ping command requested!')
            await message.delete(delay=5)
            embed = discord.Embed(
                title='Pong!',
                description='Micalateia is online!',
                color=discord.Color.green()
            )
            logger.info('Ping sent!')

        elif message.content.startswith('!ms'):
            logger.info('Manga Search command requested!')
            await message.delete(delay=5)
            embed = discord.Embed(
                title='Micalateia Manga Search',
                description='This is a test for the manga search command',
                color=discord.Color.blue()
            )

            title = message.content.split('!ms ')[1] if len(message.content.split(' ')) > 1 else 'Overgeared'

            chapters = call_api("mangadex", "search", [title])
            logger.debug(chapters)

            if chapters is None or len(chapters) == 0:
                await message.channel.send(f"No chapters found for {title}.", delete_after=5)
                return

            embed.add_field(name='Manga:', value=title, inline=True)
            embed.set_thumbnail(url=ov_club_icon)
            embed.set_footer(text='Warning: this message will be deleted in 2min', icon_url=icons.get_icons('warning'))
            embed.set_author(name="Cereal_3D", icon_url=ov_author_icon)

            await message.channel.send(embed=embed, delete_after=120)

            logger.info('Manga Search sent!')

        elif message.content.startswith('!s'):
            logger.info('Search command requested!')
            args = message.content.split("!s ")

            await message.delete(delay=5)

            if len(args) < 2:
                await message.channel.send("Please provide a manga name.", delete_after=5)
                return

            manga_name = args[1]
            language = args[2] if len(args) > 2 else 'pt-br'

            logger.info(f'Searching for manga: {manga_name} in {language}')

            chapters = call_api("mangadex", "list_chapters", [manga_name, language])


            if chapters is not None and len(chapters) > 0:
                embed = discord.Embed(
                    title='Manga Search Result:',
                    description=f"Here are the last 5 chapters of {manga_name}",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=chapters[0])
                embed.set_footer(text='Warning: this message will be deleted in 2min', icon_url=icons.get_icons('warning'))
                embed.set_author(name="Micalateia", icon_url=ov_author_icon)

                chapters_data = get_last_chapters(args[1], language)[1]

                # logger.debug(chapters_data)
                if chapters_data is None or len(chapters_data) == 0:
                    await message.channel.send(f"No chapters found for {args[0]}.", delete_after=5)
                    return

                for chapter in chapters_data:
                    title = chapter['title'] if len(chapter['title']) > 0 else 'No title available'

                    embed.add_field(
                        name=f"Chapter {chapter['chapter']}:",
                        value=f"[{ title }]({chapter['chapter_url']})",
                        inline=False
                    )

                await message.channel.send(embed=embed, delete_after=120)
                logger.info('Search result sent!')
            else:
                await message.channel.send("Manga not found.", delete_after=5)
                logger.warning(f"Manga '{manga_name}' not found.")

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
                    # print_progress_bar(i+1, 100, prefix='Progress:', suffix='Complete', length=100)
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
        elif channel_receive != channel_test.name\
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
bot.run(initialize())