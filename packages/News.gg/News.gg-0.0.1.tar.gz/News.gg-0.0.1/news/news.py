import aiohttp
import asyncio

class NewsAPIError(Exception):
    """Custom exception for handling News API errors."""
    pass

class News:
    BASE_URL = "http://46165.site.bot-hosting.net/news/"

    def __init__(self, api_key: str):
        """
        Initializes the News class with an API key.

        :param api_key: Your API key for authentication.
        """
        self.api_key = api_key

    def fetch(self, url: str):
        """
        Helper method to perform an HTTP GET request synchronously.

        :param url: The URL to fetch.
        :return: The JSON response data.
        :raises NewsAPIError: If there is an issue with the API request.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._async_fetch(url))

    async def _async_fetch(self, url: str):
        """
        Asynchronous method to perform an HTTP GET request.

        :param url: The URL to fetch.
        :return: The JSON response data.
        :raises NewsAPIError: If there is an issue with the API request.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:  # Corrected from status_code to status
                    raise NewsAPIError(f"Failed to retrieve news: {response.status} - {await response.text()}")

                data = await response.json()

                if "articles" not in data:
                    raise NewsAPIError("Unexpected response format: 'articles' key not found.")

                return data

    def get_news_by_country(self, country_code: str, lang: str = None):
        """
        Retrieves news articles for a specified country with optional language translation.

        :param country_code: The ISO 3166-1 alpha-2 country code.
        :param lang: Optional two-letter language code for translation (ISO 639-1 standard).
        :return: A list of articles, each article is represented as a dictionary.
        :raises NewsAPIError: If there is an issue with the API request.
        """
        url = f"{self.BASE_URL}{country_code}?api_key={self.api_key}"
        
        if lang:
            url += f"&lang={lang}"

        data = self.fetch(url)
        return data["articles"]
