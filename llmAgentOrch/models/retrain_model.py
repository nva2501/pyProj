from pydantic import BaseModel

class RetrainInput(BaseModel):
    text: str
    label: str
