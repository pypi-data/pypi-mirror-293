import re
from typing import List
import tldextract
from urllib.parse import urlsplit, urljoin

URL_REGEX = re.compile(
    r'^(https?):\/\/'       # Protocol (http, https)
    r'([a-zA-Z0-9._-]+)'    # Domain (may include subdomains)
    r'(\.[a-zA-Z]{2,})'     # Top-level domain (at least 2 characters)
    r'([\/\w._%-]*)*\/?'    # Path (optional)
    r'(\?\S*)?$'            # QueryParam (optional)
)


class InvalidURL(Exception):
    """
    Raised when a URL does not match the expected pattern.

    Args:
        url (str): The invalid URL.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, url):
        self.message = f"{url} is invalid URL! Valid pattern is: http(s)://..."
        super().__init__(self.message)


def validate_urls(urls: List[str]) -> None:
    """
    Validates a list of URLs against a predefined regex pattern.

    Args:
        urls (List[str]): A list of URLs to validate.

    Raises:
        InvalidURL: If any URL does not match the pattern.
    """
    for url in urls:
        matched = URL_REGEX.match(url)
        if not matched:
            raise InvalidURL(url)


def validate_url(url: str) -> bool:
    """
    Validates a single URL against a predefined regex pattern.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL matches the pattern, otherwise False.
    """
    matched = URL_REGEX.match(url)
    if matched:
        return True
    else:
        return False


def normalize_url(url: str, base_url: str) -> str:
    """
    Converts a relative URL to an absolute URL based on a base URL.

    Args:
        url (str): The URL to normalize, which may be relative.
        base_url (str): The base URL to resolve relative URLs against.

    Returns:
        str: The absolute URL.
    """
    url = url.strip()
    split_url = urlsplit(url)
    if not split_url.scheme and not split_url.netloc:
        # URL is relative
        return urljoin(base_url, url)
    return url


def have_exact_subdomain(url1: str, url2: str) -> bool:
    """
    Checks if two URLs share the same subdomain.

    Args:
        url1 (str): The first URL.
        url2 (str): The second URL.

    Returns:
        bool: True if both URLs have the same subdomain, domain, and suffix.
    """
    extract_url1 = tldextract.extract(url1)
    extract_url2 = tldextract.extract(url2)
    return extract_url1.domain == extract_url2.domain and\
        extract_url1.suffix == extract_url2.suffix


def have_exact_domain(url1: str, url2: str) -> bool:
    """
    Checks if two URLs share the exact same domain.

    Args:
        url1 (str): The first URL.
        url2 (str): The second URL.

    Returns:
        bool: True if both URLs have the exact same domain including subdomains.
    """
    split_url1 = urlsplit(url1)
    split_url2 = urlsplit(url2)
    return split_url1.netloc == split_url2.netloc
