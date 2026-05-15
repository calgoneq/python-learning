from fastapi import FastAPI, HTTPException

from storage import load_json, append_transaction
from exceptions import ValidationError
from transaction import Transaction
from models import TransactionIn
from config import TRANSACTIONS_FILE

app = FastAPI()

@app.get("/")
def get_status():
    return {"message": "server running"}

@app.get("/transactions")
def get_transactions():
    all_transactions = load_json(TRANSACTIONS_FILE) 
    return all_transactions

@app.post("/transactions", status_code=201)
def post_transactions(item: TransactionIn):
    try:
        transaction = Transaction(item.sklep, item.kwota, item.kategoria, item.data)
        data = transaction.to_dict()
        append_transaction(data, TRANSACTIONS_FILE)
        return {"message": "ok", "transaction": data}
    except ValidationError as e:
             raise HTTPException(status_code=422, detail=str(e))