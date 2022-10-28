import requests
from datetime import date
today = date.today()


api_key = "364f5f42600246c2926ff33d40ad89af"
base_url = "https://newsapi.org/v2/everything"

class SearchNews():
    def __init__(self, search_text, sort_text, from_date=None, to_date=None):
        self.search_text = search_text
        self.sort_text = sort_text
        self.from_date = from_date
        # self.to_date = to_date

    def search(self):
        date = ""
        if self.from_date:
            date = "from=%s" % self.from_date
        else:
            date = today.strftime("%Y-%m-%d")

        url = "%s?q=%s&sortBy=%s&%s&apiKey=%s " % (base_url, self.search_text, self.sort_text, date, api_key)
        print(url)
        r = requests.get(url)
    
        return r.json()