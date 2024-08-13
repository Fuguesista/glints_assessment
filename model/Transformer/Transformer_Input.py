from pydantic import BaseModel
from typing import List

class TransformerInputClass(BaseModel):
    list_1: List[str]
    list_2: List[str]