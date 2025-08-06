import threading
from scraping.chains.CinemaCity import CinemaCity
from scraping.chains.YesPlanet import YesPlanet


def worker(cinema_cls):
    inst = cinema_cls()
    try:
        inst.scrape()
    except Exception as e:
        print(f"[{cinema_cls.__name__}] error:", e)
    finally:
        inst.driver.quit()


def main():
    cinema_classes = [CinemaCity, YesPlanet]
    threads = []

    for cls in cinema_classes:
        t = threading.Thread(target=worker, args=(cls,), name=cls.__name__)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
