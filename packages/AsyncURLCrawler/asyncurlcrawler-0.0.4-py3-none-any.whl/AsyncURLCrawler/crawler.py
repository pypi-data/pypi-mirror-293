from typing import List, Dict
from AsyncURLCrawler.url_utils import (
    validate_urls,
    have_exact_subdomain,
    have_exact_domain,
)
from collections import deque
from AsyncURLCrawler.parser import Parser
import asyncio


class Crawler:
    """
    Extracts URLs from target websites using a Breadth-First Search (BFS) algorithm.

    Args:
        :seed_urls (List[str]): Initial URLs to start crawling. Must follow a valid URL pattern, e.g., 'https://example.com'.
        :parser (Parser): Instance of the Parser class, responsible for fetching and extracting URLs from a given URL.
        :deep (bool, optional): If True, crawls all discovered URLs recursively. Defaults to False. Not recommended due to high resource usage.
        :exact (bool, optional): If True, restricts crawling to URLs with the same subdomain as the seed URL. Ignored if 'deep' is True. Defaults to True.
        :delay (float, optional): Time delay (in seconds) between requests to prevent overwhelming the target server. Defaults to 0.
    """

    def __init__(
            self,
            seed_urls: List[str],
            parser: Parser,
            deep: bool = False,
            exact: bool = True,
            delay: float = 0,
    ):
        self._set_seed_urls(seed_urls)
        self._parser = parser
        self._deep = deep
        self._exact = exact
        self._delay = delay

    def _set_seed_urls(self, seed_urls: List[str]) -> None:
        """Validates and sets the initial seed URLs."""
        validate_urls(seed_urls)
        self._seed_urls = seed_urls
        self._visited_urls = dict.fromkeys(seed_urls, set())

    def _update_queue(self, extracted_url: str, root_url: str) -> None:
        """Updates the queue based on crawling rules."""
        if self._deep:
            self._queue.append(extracted_url)
        else:
            if self._exact:
                if have_exact_domain(extracted_url, root_url):
                    self._queue.append(extracted_url)
            else:
                if have_exact_subdomain(extracted_url, root_url):
                    self._queue.append(extracted_url)

    def _reset_queue(self) -> None:
        """Resets the BFS queue."""
        self._queue = deque()

    async def crawl(self) -> Dict:
        """
        Asynchronously crawls all seed URLs using BFS.

        Returns:
            Dict: A dictionary where each key is a seed URL and each value is a set of visited URLs for that seed.
        """
        for root_url in self._seed_urls:
            self._reset_queue()
            self._queue.append(root_url)
            while self._queue:
                current_url = self._queue.popleft()
                self._parser.reset()
                extracted_urls = await self._parser.probe(current_url)
                for extracted_url in extracted_urls:
                    if extracted_url not in self._visited_urls[root_url]:
                        self._visited_urls[root_url].add(extracted_url)
                        self._update_queue(extracted_url, root_url)
                await asyncio.sleep(self._delay)
        return self._visited_urls

    async def yielded_crawl(self) -> str:
        """
        Asynchronously crawls seed URLs using BFS and yields each visited URL.

        Yields:
            str: Each URL as it is visited.
        """
        for root_url in self._seed_urls:
            self._reset_queue()
            self._queue.append(root_url)
            while self._queue:
                current_url = self._queue.popleft()
                self._parser.reset()
                extracted_urls = await self._parser.probe(current_url)
                for extracted_url in extracted_urls:
                    if extracted_url not in self._visited_urls[root_url]:
                        self._visited_urls[root_url].add(extracted_url)
                        self._update_queue(extracted_url, root_url)
                        yield extracted_url
                await asyncio.sleep(self._delay)
        return

    def get_visited_urls(self) -> Dict:
        """
        Returns the visited URLs.

        Returns:
            Dict: A dictionary where each key is a seed URL and each value is a set of visited URLs for that seed.
        """
        return self._visited_urls
