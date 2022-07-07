from database import db
from fastapi import FastAPI


from routes import outlets, transactions


app = FastAPI()

app.include_router(outlets.router)
app.include_router(transactions.router)


@app.on_event("shutdown")
def shutdown():
    db.close()
