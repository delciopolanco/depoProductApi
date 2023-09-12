from pydantic import BaseModel
from typing import List, Optional


class ExecutionViewModel(BaseModel):
    id: Optional[str]
    searchText: str
    uuid: str
    webs: List[str]
