from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import Session, select
from koco_product_sqlmodel.definition import (
    CCatalog,
)


def collect_catalogs():
    with Session(mdb_engine) as session:
        statement = select(CCatalog)
        results = session.exec(statement)
        res = []
        for r in results:
            res.append({"id": r.id, "supplier": r.supplier, "year": r.year})
    return res


def create_catalog(catalog: CCatalog):
    with Session(mdb_engine) as session:
        session.add(catalog)
        session.commit()
        statement = select(CCatalog).where(CCatalog.id == catalog.id)
    return session.exec(statement=statement).one_or_none()


def main()->None:
    pass

if __name__=="__main__":
    main()