from dotenv.main import load_dotenv
from cogs.utils.fuctions import get_env_variable
import sys


def initialize():
    """
    Initialize the bot by loading environment variables and checking for required configurations.
    """
    # Load environment variables from .env file
    load_dotenv()
    # Check if the .env file exists
    if get_env_variable('DISCORD_TOKEN') is None:
        sys.exit("'DISCORD_TOKEN' not found! Please add it and try again.")

    DISCORD_TOKEN =  get_env_variable("DISCORD_TOKEN")
    return DISCORD_TOKEN
    