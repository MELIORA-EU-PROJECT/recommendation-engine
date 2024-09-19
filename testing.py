import random

import json5
import numpy as np
import matplotlib.pyplot as plt

from fastapi import FastAPI, Body, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()


# class Item(BaseModel):
#     onoma: str
#

@app.post("/")
async def root(my_item_param: Request):
    # async def root(my_item_param: Item):
    print(f"{await my_item_param.json()=}")
    # print(f"{my_item_param=}")
    to_json = await my_item_param.json()
    return f"Hello {to_json}"

# plt.hist(distribution, bins=100)
# plt.show()