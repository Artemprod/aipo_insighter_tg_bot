from pydantic import BaseModel


class IncomeTranscribedText(BaseModel):
    id_text: str | int
    addressee: str | None = None
    description: str | None = None


class TranscribedTextId(BaseModel):
    id_text: str | int
