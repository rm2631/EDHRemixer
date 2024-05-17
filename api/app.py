# Import necessary libraries
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from models import Collection
from services.shuffle_manager import ShuffleManager
import uvicorn
from typing import List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define a POST endpoint with a path parameter and request body
@app.post("/reshuffle")
async def reshuffle(inputs: List[Collection]):
    manager = ShuffleManager(inputs)
    file = manager.reshuffle()
    headers = {"Content-Disposition": "attachment; filename=reshuffled_deck.xlsx"}
    return Response(
        content=file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


if __name__ == "__main__":
    uvicorn.run(app)
