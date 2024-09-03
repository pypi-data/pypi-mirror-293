from fastapi import FastAPI
import koco_product_sqlmodel.fastapi.routes.catalog as rcat

app = FastAPI()
app.include_router(rcat.router, prefix="/catalogs")

@app.get("/")
def read_root():
    return {"Hello": "World"}

def main():
    pass

if __name__=="__main__":
    main()