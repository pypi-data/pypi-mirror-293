from typing import List, Optional

from pydantic import BaseModel, Field

from classiq.interface.executor.quantum_code import Arguments


class PrimitivesInput(BaseModel):
    sample: Optional[List[Arguments]] = Field(default=None)
