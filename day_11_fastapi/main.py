from fastapi import FastAPI

from storage import load_json, append_transaction
from transaction import Transaction as t
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
    transaction = t(item.sklep, item.kwota, item.kategoria, item.data)
    data = transaction.to_dict()
    append_transaction(data, TRANSACTIONS_FILE)
    message = f"Dodano: {data['sklep']} | {data['kwota']:.2f} zł | {data['kategoria']}"
    return message