from pydantic import BaseModel
from typing import List

class SeatingCreateRequest(BaseModel):
    rows: int
    cols: int
    row_allocation: List[str]
