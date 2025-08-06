from .BaseCinema import BaseCinema


class YesPlanet(BaseCinema):
    NAME = "Yes Planet"
    URL = "https://www.planetcinema.co.il/?lang=en_GB#/"

    def logic(self, items):
        print(f"scraping yes planet")
        a = self.elementCSS(
            "body > section.dark.footer.noprint > div > div.row.hidden-xs > div:nth-child(1) > p:nth-child(3) > a"
        )
        print(a.text)
