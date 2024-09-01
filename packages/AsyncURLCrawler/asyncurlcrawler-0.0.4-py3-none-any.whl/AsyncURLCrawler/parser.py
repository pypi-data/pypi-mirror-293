from httpx import Response, AsyncClient, ConnectTimeout
import asyncio
from typing import List
from bs4 import BeautifulSoup
from AsyncURLCrawler.url_utils import normalize_url, validate_url


class Parser:
    """
    Fetches a URL, parses its HTML content, and extracts URLs from <a> tags.
    Implements exponential backoff for retrying failed requests.

    Args:
        :delay_start (float, optional): Initial delay in the exponential backoff strategy. Defaults to 0.1 seconds.
        :max_retries (int, optional): Maximum number of retry attempts. Defaults to 5.
        :request_timeout (float, optional): Timeout for each HTTP request in seconds. Defaults to 1 second.
        :user_agent (str, optional): User-Agent string for HTTP request headers. Defaults to 'Mozilla/5.0'.
    """
    def __init__(
            self,
            delay_start: float = 0.1,
            max_retries: int = 5,
            request_timeout: float = 1,
            user_agent: str = 'Mozilla/5.0',
    ):
        self._delay_start = delay_start
        self._current_delay = delay_start
        self._max_retries = max_retries
        self._request_timeout = request_timeout
        self._current_retry = 0
        self._user_agent = user_agent

    def reset(self):
        """
        Resets the backoff state for a new URL fetch attempt.
        Must be called before each new URL fetch.
        """
        self._current_retry = 0
        self._current_delay = self._delay_start

    async def _fetch_page(self, url: str) -> [Response, None]:
        """
        Asynchronously fetches a URL with specified headers and timeout.

        Args:
        :url (str): The URL to fetch.

        Returns:
            Response or None: The HTTP response if successful, otherwise None if timed out.
        """
        # TODO Check file format before fetching! ignore jpg, pdf, ...
        async with AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    timeout=self._request_timeout,
                    headers={"User-Agent": self._user_agent},
                )
            except ConnectTimeout:
                return None
            return response

    def _extract_urls(self, response: str, base_url: str) -> List[str]:
        """
        Extracts and normalizes URLs from <a> tags in the HTML content.

        Args:
            :response (str): The HTML content of the fetched page.
            :base_url (str): The base URL for converting relative URLs to absolute.

        Returns:
            List[str]: A list of validated absolute URLs.
        """
        soup = BeautifulSoup(response, 'html.parser')
        urls = list()
        for link in soup.find_all('a', href=True):
            n_link = normalize_url(link.get('href'), base_url)
            if validate_url(n_link):
                urls.append(n_link)
        return urls

    async def probe(self, url: str) -> List[str]:
        """
        Fetches a URL and extracts URLs using an exponential backoff strategy on failures.

        Args:
            :url (str): The URL to probe.

        Returns:
            List[str]: A list of extracted URLs. Returns an empty list if the fetch fails after retries.
        """
        # TODO Check response size!
        response = await self._fetch_page(url)
        status_code = None
        if response:
            status_code = response.status_code
        while status_code is None or status_code == 429 or status_code >= 500:
            if self._current_retry == self._max_retries:
                break
            await asyncio.sleep(self._current_delay)
            self._current_delay *= pow(2, self._current_retry)
            self._current_retry += 1
            response = await self._fetch_page(url)
            if response:
                status_code = response.status_code
        if status_code != 200:
            return []
        urls = self._extract_urls(response.text, url)
        return urls
