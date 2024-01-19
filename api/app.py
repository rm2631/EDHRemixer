# Import necessary libraries
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import DeckListModel
from utils.Remixer import Remixer

# Create an instance of the FastAPI class
app = FastAPI()
## Set CORS
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://127.0.0.1:5173/",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Define a POST endpoint with a path parameter and request body
@app.post("/reshuffle")
async def reshuffle(deck: DeckListModel):
    # Create an instance of the Remixer class
    remixer = Remixer()
    # Add the source deck to the remixer
    remixer.add_deck(deck.source, True)
    remixer.add_deck(deck.target, False)
    # Reallocate the cards
    file = remixer.reallocate()
    headers = {"Content-Disposition": 'attachment; filename="export.xlsx"'}
    return Response(
        content=file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


if __name__ == "__main__":
    uvicorn.run(app)
