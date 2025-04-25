# -*- coding: utf-8 -*-
# Developer: Carlos Andrade
# Date: 2023-10-01
# Description: This file contains the configuration for the bot, including default values and API configurations.
# This file is part of Manga-chan, a Discord bot for manga enthusiasts.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
"""
# Configuration file for the bot
This file contains the default values and API configurations for the bot.
"""

_MANGADEX_BASE_URL = "https://api.mangadex.org"

DEFAULTS = {
  "prefix": "mc!",
  "invite_link": "YOUR_BOT_INVITE_LINK_HERE"
}

APIS =  {
  "mangadex": {
    "endpoints": {
      "get_manga_by_id": _MANGADEX_BASE_URL+"/manga/{}",
      "get_manga_by_title": _MANGADEX_BASE_URL+"/manga",
      "get_cover": _MANGADEX_BASE_URL+"/cover/{}",
      "get_chapter_feed": _MANGADEX_BASE_URL+"/manga/{}/feed",
      },
    },
  "mangafox": {
    "base_url": "https://mangafox.me",
    "version": "v1"
  },
  "mangaplus": {
    "base_url": "https://mangaplus.shueisha.co.jp",
    "version": "v1"
  }
}


