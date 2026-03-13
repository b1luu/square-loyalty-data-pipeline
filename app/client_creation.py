import os

from dotenv import load_dotenv
from square import Square
from square.environment import SquareEnvironment

load_dotenv()

client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=os.getenv("SQUARE_ACCESS_TOKEN"),
)
