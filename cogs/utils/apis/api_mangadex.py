import requests
import json
import logging
from cogs.utils.config import APIS
from cogs.system.logger import LoggingFormatter


logger = logging.getLogger("MiK:API[mangadex]")
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

def __init__():
    """
    Initialize the module by setting up the base URL and endpoints for the MangaDex API.
    """
    global ENDPOINTS
    ENDPOINTS = APIS['mangadex']['endpoints']

def search_manga_by_title(title):
    """
    Search for a manga by its title using the MangaDex API.

    :param endpoint_url: The base URL for the MangaDex API.
    :param title: The title of the manga to search for.
    :return: A list of manga titles that match the search query.
    """
    req = requests.get(f"{ENDPOINTS['get_manga_by_title']}",
                    params={"title": title})
    # Create a function to extract the title from the response
    # and return a list of titles
    # logger.debug(f"req: {req.json()}")

    return req.json()

def get_cover_art(cover_art_id):
    cover_art_data = requests.get(ENDPOINTS["get_cover"].format(cover_art_id)).json()

    return cover_art_data["data"]["attributes"]["fileName"] if cover_art_data["result"] == "ok" else None

def get_last_chapters(title, language):
    manga_data = search_manga_by_title(title)["data"]
    # logger.debug(f"manga_data: {manga_data}")

    manga_id = manga_data[0]["id"]  # Assuming the first manga in the list TODO> handle multiple results
    # logger.debug(f"manga_id: {manga_id}")

    cover_art_id = [item["id"] for item in manga_data[0]["relationships"] if item["type"] == "cover_art"][0]
    cover_art_name = get_cover_art(cover_art_id) if cover_art_id is not None else 'N/A'
    manga_string = ENDPOINTS["get_chapter_feed"]
    # logger.debug(f"manga_string: {manga_string}")
    # logger.debug(f"manga_string_format: {manga_string.format(manga_id)}")

    manga_raw_data = requests.get(
        manga_string.format(manga_id),
        params={"limit": 5, "translatedLanguage[]": language, "order[chapter]": "desc"}
    )

    if manga_raw_data.status_code == 200:
        chapters = manga_raw_data.json()["data"]

        with open("raw_chapters.json", "w", encoding="utf-8") as file:
            json.dump(chapters, file, ensure_ascii=False, indent=4)

        details = {
            "cover_art_url": f"https://mangadex.org/covers/{manga_id}/{cover_art_name}" if cover_art_name is not None else 'N/A',
        }

        return details["cover_art_url"], [
            {
                "chapter": chapter["attributes"]["chapter"] if chapter["attributes"]["chapter"] is not None else " No chapter",
                "title": chapter["attributes"]["title"],
                "language": language,
                "chapter_id": chapter["id"],
                "chapter_url": f"https://mangadex.org/chapter/{chapter['id']}/1",
                "publisher_url": f"https://mangadex.org/group/{chapter['relationships'][0]['id']}",
                "publisher_id": chapter["relationships"][0]["id"],
                "dates": {
                    "publish_at": chapter["attributes"]["publishAt"],
                    "created_at": chapter["attributes"]["createdAt"],
                    "updated_at": chapter["attributes"]["updatedAt"],
                    "readable_at": chapter["attributes"]["readableAt"]
                }
            }
            for chapter in chapters
        ]
    else:
        print(f"Error: {manga_raw_data.status_code}")
        return None

__init__()