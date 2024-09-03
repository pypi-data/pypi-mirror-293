from fastapi import APIRouter
import koco_product_sqlmodel.definition_reduced as sqmr
import koco_product_sqlmodel.mdb_connect.catalogs as mdb_cat

router = APIRouter()

@router.get("/")
def get_catalogs():
    catalogs = mdb_cat.collect_catalogs_db_items()
    return catalogs

@router.get("/{id}/")
def get_catalog_by_id(id):
    catalog = mdb_cat.collect_catalog_by_id(id)
    return catalog

@router.post("/")
def create_catalog(catalog: sqmr.CCatalog):
    print(catalog)

def main():
    pass

if __name__=="__main__":
    main()