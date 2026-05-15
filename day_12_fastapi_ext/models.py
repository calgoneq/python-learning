from pydantic import BaseModel, field_validator

class TransactionIn(BaseModel):
    sklep: str
    kwota: float
    kategoria: str
    data: str

    @field_validator("kwota")
    @classmethod
    def kwota_musi_byc_dodatnia(cls, v):
        if v <= 0:
            raise ValueError("kwota musi być większa od 0!")
        return v