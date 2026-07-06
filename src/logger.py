import logging
import os
from datetime import datetime

FILE_PATH = os.path.join(os.getcwd(), f"{datetime.now().strftime("%d-%m-%Y")}.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s: %(name)s - %(message)s",
    filename=FILE_PATH,
)
