import requests
from bs4 import BeautifulSoup

class ProductionCompany:
    def __init__(self, name="", url="", id=""):
        self._name = name
        self._company_url = url
        self._company_id = id

    def search_by_keyword(self, keyword):
        # Construct the search URL
        search_url = f"https://www.imdb.com/find?q={keyword}&s=co"

        # Send a GET request to the search URL
        response = requests.get(search_url)

        # Use Beautiful Soup to parse the HTML content of the search results page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the first search result that matches the keyword and extract its unique identifier
        result = soup.find("td", {"class": "result_text"})
        if result is not None:
            self._name = result.text.strip()
            company_url = result.a["href"]
            self._company_url = "https://www.imdb.com" + company_url
            self._company_id = company_url.split("/")[-2]

        return self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def company_url(self):
        return self._company_url

    @company_url.setter
    def company_url(self, value):
        self._company_url = value

    @property
    def company_id(self):
        return self._company_id

    @company_id.setter
    def company_id(self, value):
        self._company_id = value
