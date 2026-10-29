import logging
import random
import cloudscraper
from time import sleep

from services.http_logging import logged_get

logger = logging.getLogger(__name__)
SERVICE = "Moxfield"


class MoxfieldConnector:

    RETRIES = 5

    @staticmethod
    def _new_scraper():
        # Fresh session + rotating browser fingerprint per attempt; Cloudflare
        # intermittently 403s a given fingerprint/session.
        return cloudscraper.create_scraper(
            browser={
                "browser": random.choice(["chrome", "firefox"]),
                "platform": "windows",
                "mobile": False,
            },
            delay=10,
        )

    @staticmethod
    def _get(url: str, what: str, id: str, params: dict | None = None):
        retries = MoxfieldConnector.RETRIES
        for attempt in range(1, retries + 1):
            try:
                response = logged_get(
                    MoxfieldConnector._new_scraper(),
                    url,
                    logger=logger,
                    service=SERVICE,
                    attempt=attempt,
                    max_attempts=retries,
                    params=params,
                )
                if response.status_code == 200:
                    return response
            except Exception:
                if attempt == retries:
                    raise
            if attempt < retries:
                delay = 2 * attempt + random.uniform(0, 1.5)
                logger.warning("Retrying %s fetch in %.1fs (id=%s)", what, delay, id)
                sleep(delay)
        logger.error("Giving up fetching %s (id=%s)", what, id)
        raise Exception(f"Failed to fetch {what}")

    @staticmethod
    def _unpack_response(cards) -> list:
        return [v for k, v in cards.items()]

    @staticmethod
    def get_deck_name(id: str, is_binder: bool = False) -> str:
        if is_binder:
            # For binders, use the search endpoint to get tradeBinder object
            response = MoxfieldConnector._get(
                f"https://api2.moxfield.com/v1/trade-binders/{id}/search",
                "binder name",
                id,
                params={
                    "pageNumber": 1,
                    "pageSize": 100,
                    "playStyle": "paperDollars",
                    "sortType": "cardName",
                    "sortDirection": "ascending",
                },
            )
            return response.json()["tradeBinder"]["name"]

        response = MoxfieldConnector._get(
            "https://api2.moxfield.com/v3/decks/all/" + id, "deck name", id
        )
        return response.json()["name"]

    @staticmethod
    def get_deck_content(id: str, include_sideboard: bool = False) -> list[dict]:
        response = MoxfieldConnector._get(
            "https://api2.moxfield.com/v3/decks/all/" + id, "deck content", id
        )

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
        while True:
            response = MoxfieldConnector._get(
                base_url.format(id=id), "binder content", id, params=dict(params)
            )

            new_cards = response.json()["data"]
            cards.extend(new_cards)

            if response.json()["totalPages"] == pageNumber or not new_cards:
                break
            pageNumber += 1
            params["pageNumber"] = pageNumber
        return cards
