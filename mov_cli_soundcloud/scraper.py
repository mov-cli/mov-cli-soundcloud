from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from mov_cli.config import Config
from mov_cli.http_client import HTTPClient

if TYPE_CHECKING:
    from typing import Optional, Generator, Any

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient
    from mov_cli.scraper import ScraperOptionsT

from dataclasses import dataclass, field

from mov_cli import utils
from mov_cli.scraper import Scraper
from mov_cli import Single, Metadata, MetadataType
from mov_cli import ExtraMetadata

import yt_dlp

__all__ = ("SoundCloudScraper", "SoundCloudMetadata",)

@dataclass
class SoundCloudMetadata(Metadata):
    id: int
    info: dict = field(default = None)

class SoundCloudScraper(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient, options: Optional[ScraperOptionsT] | None = None) -> None:
        self.base_url = "https://soundcloud.com"

        super().__init__(config, http_client, options)

    def search(self, query: str, limit: Optional[int]) -> Iterable[Metadata]:
        search_page = self.http_client.get(f"{self.base_url}/search?q={query}")

        soup = self.soup(search_page)

        noscript = soup.find_all("noscript")[-1]

        items = noscript.select("h2 > a")

        if limit is not None:
            items = items[:limit]

        yt_options = {"skip_download": True, "quiet": not self.config.debug}

        for _, item in enumerate(items):
            if item["href"].count("/") == 2: # NOTE: only get music
                with yt_dlp.YoutubeDL(yt_options) as f:
                    info = f.extract_info(self.base_url + item["href"])
                    
                yield SoundCloudMetadata(
                    id = _,
                    title = info.get("title") + " ~ " + info.get("uploader"),
                    type = MetadataType.SINGLE,
                    year = info.get("upload_date", "")[:4],
                    info = info,

                    extra_func = lambda: ExtraMetadata(
                        description = info.get("description"),
                        image_url = info.get("thumbnails")[-1]["url"],
                        genres = info.get("genres")
                    )
                )

    def scrape(self, metadata: SoundCloudScraper, episode: utils.EpisodeSelector) -> Single:
        return Single(
            url = metadata.info.get("formats")[-1]["url"],
            title = metadata.title,
            year = metadata.year
        )