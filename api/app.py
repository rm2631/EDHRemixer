# Import necessary libraries
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import DeckReshuffleModel, DeckModel
from utils.Remixer import Remixer
from utils.Services.Scryfall import get_card_data
import asyncio

app = FastAPI()


# Define a POST endpoint with a path parameter and request body
@app.post("/reshuffle")
async def reshuffle(deck: DeckReshuffleModel):
    # Create an instance of the Remixer class
    remixer = Remixer()
    # Add the source deck to the remixer
    remixer.add_deck(deck.source, True)
    remixer.add_deck(deck.target, False)
    # Reallocate the cards
    file = remixer.reshuffle()
    headers = {"Content-Disposition": 'attachment; filename="export.xlsx"'}
    return Response(
        content=file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


@app.post("/deck")
async def deck(deck: DeckModel):
    results = await asyncio.gather(*[get_card_data(card) for card in deck.cards])
    return results


if __name__ == "__main__":
    uvicorn.run(app)
