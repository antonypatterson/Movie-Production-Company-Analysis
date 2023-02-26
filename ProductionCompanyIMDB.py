import requests
from bs4 import BeautifulSoup
import pandas as pd

class ProductionCompanyIMDB:
    def __init__(self, name="", url="", id="", average_weighting=""):
        self._name = name
        self._company_url = url
        self._company_id = id
        self._average_rating = average_weighting

    def get_average_rating(self, export_csv=False):
        #only calls "private" method if company id not already assigned and self._name is already assigned
        if not self._company_id and self._name:
            self.__search_by_keyword(self._name)

        if not self._average_rating and self._company_id:

            # Construct the URL for the company's IMDB page and headers            
            base_url = "https://www.imdb.com/search/title/"          

            headers = {
                "Accept-Language": "en-US,en;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }

            # create empty dataframe
            df = pd.DataFrame(columns=["title", "rating"])

            #set starting index and number of movies to retrieve
            start = 1
            num_movies_tag = soup.find('span', class_='desc').text
            num_movies = num_movies_tag.split(' of ')[-1].split(' titles')[0].replace(',', '')
            print("num movies are " + num_movies)
            num_movies_testDummy = 50
            
            while start <= num_movies_testDummy:  
                query_string = f"?companies={self._company_id}&start={start}"
                response = requests.get(base_url + query_string, headers=headers)

                # Use Beautiful Soup to parse the HTML content of the company's IMDB page
                soup = BeautifulSoup(response.text, "html.parser")

                 # find all the movie titles and ratings on the page
                titles = soup.find_all('h3', class_='lister-item-header')
                #ratings = soup.find_all('div', class_='inline-block ratings-imdb-rating')

                # loop through title elements and extract title and rating
                for title in titles:
                    # extract title text
                    title_text = title.find("a").text.strip()
                    
                    # extract rating value from data-value attribute
                    rating_value = title.find("div", class_="inline-block ratings-imdb-rating")["data-value"]
                    
                    # add title and rating to dataframe
                    df = df.append({"title": title_text, "rating": rating_value}, ignore_index=True)
                
                # increase start index by 50 for the next page
                start += 50

            self._average_rating = df["title"].mean()

            if export_csv:
                df.to_csv(f"{self._name}_titles_1_to_{start+49}.csv", index=False)

        elif export_csv:
            print("You have defined export_csv as true, but the get_average loops were not run as this object instance already has been run. \n "
                  "Please use the clear_average_weighting() then get_average_rating() methods to re-run the calculation and export")

        # whether run for first time or already set and re-running, still returns the average rating
        return self._average_rating

    def __search_by_keyword(self, keyword):
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
    
    
    def clear_average_weighting(self):
        self._average_rating = ""  

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
