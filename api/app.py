# Import necessary libraries
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from models import Collection
from services.shuffle_manager import ShuffleManager
import uvicorn

app = FastAPI()


# Define a POST endpoint with a path parameter and request body
@app.post("/reshuffle")
async def reshuffle(deck: Collection):
    pass

    # return Response(
    #     content=file,
    #     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     headers=headers,
    # )


if __name__ == "__main__":
    uvicorn.run(app)
