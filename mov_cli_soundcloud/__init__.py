from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mov_cli.plugins import PluginHookData

from .scraper import *

plugin: PluginHookData = {
    "version": 1, 
    "package_name": "mov-cli-soundcloud",
    "scrapers": {
        "DEFAULT": SoundCloudScraper, 
        "soundcloud": SoundCloudScraper
    }
}

__version__ = "1.0.0"