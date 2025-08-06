from .BaseCinema import BaseCinema


class CinemaCity(BaseCinema):
    NAME = "Cinema City"
    URL = "https://www.cinema-city.co.il/"

    def logic(self, items):
        print(f"scraping cinema city")
        a = self.elementCSS(
            "body > div.container-fluid.footer > div > p > span:nth-child(3) > strong > a"
        )
        print(a.text)