import logging
import cloudscraper
from time import sleep

from services.http_logging import logged_get

logger = logging.getLogger(__name__)
SERVICE = "Moxfield"


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
    def get_deck_name(id: str, is_binder: bool = False) -> str:
        scraper = cloudscraper.create_scraper()
        retries = 3

        if is_binder:
            # For binders, use the search endpoint to get tradeBinder object
            base_url = "https://api2.moxfield.com/v1/trade-binders/{id}/search"
            params = {
                "pageNumber": 1,
                "pageSize": 100,
                "playStyle": "paperDollars",
                "sortType": "cardName",
                "sortDirection": "ascending",
            }
            for attempt in range(1, retries + 1):
                response = logged_get(
                    scraper,
                    base_url.format(id=id),
                    logger=logger,
                    service=SERVICE,
                    attempt=attempt,
                    max_attempts=retries,
                    headers=MoxfieldConnector._build_headers(),
                    params=params,
                )
                if response.status_code == 200:
                    break
                logger.warning("Retrying binder name fetch in 5s (id=%s)", id)
                sleep(5)  # Wait for 5 seconds before retrying
            else:
                logger.error("Giving up fetching binder name (id=%s)", id)
                raise Exception("Failed to fetch binder name")

            return response.json()["tradeBinder"]["name"]
        else:
            # For decks, use the existing endpoint
            base_url = "https://api2.moxfield.com/v3/decks/all/" + id
            for attempt in range(1, retries + 1):
                response = logged_get(
                    scraper,
                    base_url,
                    logger=logger,
                    service=SERVICE,
                    attempt=attempt,
                    max_attempts=retries,
                    headers=MoxfieldConnector._build_headers(),
                )
                if response.status_code == 200:
                    break
                logger.warning("Retrying deck name fetch in 5s (id=%s)", id)
                sleep(5)  # Wait for 5 seconds before retrying
            else:
                logger.error("Giving up fetching deck name (id=%s)", id)
                raise Exception("Failed to fetch deck name")

            return response.json()["name"]

    @staticmethod
    def get_deck_content(id: str, include_sideboard: bool = False) -> list[dict]:
        base_url = "https://api2.moxfield.com/v3/decks/all/"
        scraper = cloudscraper.create_scraper()
        retries = 3
        for attempt in range(1, retries + 1):
            response = logged_get(
                scraper,
                base_url + id,
                logger=logger,
                service=SERVICE,
                attempt=attempt,
                max_attempts=retries,
                headers=MoxfieldConnector._build_headers(),
            )
            if response.status_code == 200:
                break
            logger.warning("Retrying deck content fetch in 5s (id=%s)", id)
            sleep(5)  # Wait for 5 seconds before retrying
        else:
            logger.error("Giving up fetching deck content (id=%s)", id)
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
        
        cards = mainboard + commanders + companions
        
        if include_sideboard:
            sideboard = MoxfieldConnector._unpack_response(
                response.json()["boards"]["sideboard"]["cards"]
            )
            cards = cards + sideboard

        return cards

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
            response = logged_get(
                scraper,
                base_url.format(id=id),
                logger=logger,
                service=SERVICE,
                headers=MoxfieldConnector._build_headers(),
                params=params,
            )
            if response.status_code != 200:
                logger.error(
                    "Failed to fetch binder content (id=%s, page=%s)", id, pageNumber
                )
                raise Exception("Failed to fetch binder content")

            new_cards = response.json()["data"]
            cards.extend(new_cards)

            if response.json()["totalPages"] == pageNumber or not new_cards:
                break
            pageNumber += 1
            params["pageNumber"] = pageNumber
        return cards
