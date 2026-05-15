from fastapi import FastAPI, HTTPException

from storage import load_json, append_transaction, delete_transaction
from exceptions import ValidationError
from transaction import Transaction
from models import TransactionIn
from config import TRANSACTIONS_FILE

app = FastAPI()

@app.get("/")
def get_status():
    return {"message": "server running"}

@app.get("/transactions")
def get_transactions(kategoria: str = None):
    transactions = load_json(TRANSACTIONS_FILE) 
    if kategoria is not None:
        temp_list: list = []
        for i in transactions:
             if i["kategoria"] == kategoria:
                  temp_list.append(i)
        return temp_list
    
    return transactions

@app.get("/transactions/{transaction_id}")
def get_transactions_by_id(transaction_id: int):
    transactions = load_json(TRANSACTIONS_FILE)
    if transaction_id >= len(transactions) or transaction_id < 0:
        raise HTTPException(status_code=404, detail=f"Transakcja o id {transaction_id} nie istnieje")
    return transactions[transaction_id]

@app.post("/transactions", status_code=201)
def post_transaction(item: TransactionIn):
    try:
        transaction = Transaction(item.sklep, item.kwota, item.kategoria, item.data)
        data = transaction.to_dict()
        append_transaction(data, TRANSACTIONS_FILE)
        return {"message": "ok", "transaction": data}
    except ValidationError as e:
             raise HTTPException(status_code=422, detail=str(e))

@app.delete("/transactions/{transaction_id}")
def delete_transactions(transaction_id: int):
    transactions = load_json(TRANSACTIONS_FILE)
    
    for id, item in enumerate(transactions, start=1):
        if id == transaction_id:
            print(item)
            delete_transaction(item, TRANSACTIONS_FILE)
            return {"message": f"Usunięto transakcje o id {transaction_id}"}
        
        else:
             return {"message": f"Transakcja od id {transaction_id} nie istnieje"}
