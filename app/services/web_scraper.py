import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
import time

logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_url(self, url: str, max_length: int = 10000) -> str:
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return f"Invalid URL: {url}"

            print(f"Scraping URL: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            text_parts = []
            content_selectors = [
                'main', 'article', '.content', '.main-content',
                '#content', '#main', '.post-content', '.entry-content'
            ]

            main_content = None
            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            content_element = main_content if main_content else soup.find('body')

            if content_element:
                text_elements = content_element.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td'])

                for element in text_elements:
                    text = element.get_text().strip()
                    if text and len(text) > 10:
                        text_parts.append(text)

            if not text_parts:
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text_parts = [chunk for chunk in chunks if chunk and len(chunk) > 10]

            combined_text = "\n".join(text_parts)
            if len(combined_text) > max_length:
                combined_text = combined_text[:max_length] + "..."

            print(f"Scraped {len(combined_text)} characters from {url}")
            return combined_text

        except Exception as e:
            logger.error(f"Web scraping failed for {url}: {e}")
            return f"Could not retrieve content from {url}: {str(e)}"

    def scrape_multiple_urls(self, urls: list, max_length: int = 15000) -> str:
        all_content = []

        for url in urls:
            content = self.scrape_url(url, max_length // len(urls))
            if content and not content.startswith("Could not retrieve"):
                all_content.append(f"Content from {url}:\n{content}")

            time.sleep(1)

        return "\n\n".join(all_content) if all_content else "No web content available."