import cloudscraper
from time import sleep


class MoxfieldConnector:

    @staticmethod
    def _build_headers() -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    @staticmethod
    def _unpack_response(cards) -> list:
        return [v for k, v in cards.items()]

    @staticmethod
    def get_deck_name(id: str) -> str:
        base_url = "https://api2.moxfield.com/v3/decks/all/"
        scraper = cloudscraper.create_scraper()
        retries = 3
        for _ in range(retries):
            response = scraper.get(
                url=base_url + id,
                headers=MoxfieldConnector._build_headers(),
            )
            if response.status_code == 200:
                break
            sleep(5)  # Wait for 5 seconds before retrying
        else:
            raise Exception("Failed to fetch deck name")

        return response.json()["name"]

    @staticmethod
    def get_deck_content(id: str) -> list[dict]:
        base_url = "https://api2.moxfield.com/v3/decks/all/"
        scraper = cloudscraper.create_scraper()
        retries = 3
        for _ in range(retries):
            response = scraper.get(
                url=base_url + id,
                headers=MoxfieldConnector._build_headers(),
            )
            if response.status_code == 200:
                break
            sleep(5)  # Wait for 5 seconds before retrying
        else:
            raise Exception("Failed to fetch deck content")

        mainboard = MoxfieldConnector._unpack_response(
            response.json()["boards"]["mainboard"]["cards"]
        )
        commanders = MoxfieldConnector._unpack_response(
            response.json()["boards"]["commanders"]["cards"]
        )
        companions = MoxfieldConnector._unpack_response(
            response.json()["boards"]["companions"]["cards"]
        )

        return mainboard + commanders + companions

    @staticmethod
    def get_binder_content(id: str) -> list[dict]:
        cards = []
        pageNumber = 1
        base_url = "https://api2.moxfield.com/v1/trade-binders/{id}/search"
        params = {
            "pageNumber": pageNumber,
            "pageSize": 100,
            "playStyle": "paperDollars",
            "sortType": "cardName",
            "sortDirection": "ascending",
        }
        scraper = cloudscraper.create_scraper()

        while True:
            response = scraper.get(
                url=base_url.format(id=id),
                headers=MoxfieldConnector._build_headers(),
                params=params,
            )
            if response.status_code != 200:
                raise Exception("Failed to fetch binder content")

            new_cards = response.json()["data"]
            cards.extend(new_cards)

            if response.json()["totalPages"] == pageNumber or not new_cards:
                break
            pageNumber += 1
            params["pageNumber"] = pageNumber
        return cards


if __name__ == "__main__":
    moxfield_connector = MoxfieldConnector()
    # print(moxfield_connector.get_deck_content("c78MLCfSKEifjtEGU-Ty5A"))
    print(moxfield_connector.get_binder_content("Zfx1zY2E8Eid4MbARdh6Gw"))
