from fastapi import APIRouter
from viewmodels.products import ProductViewModel
from services.database.dbProducts import DBProducts
from services.database.dbExecute import DBExecute


router = APIRouter()
executionDB = DBExecute()
productDB = DBProducts()


@router.post('/products')
def createProducts(product: ProductViewModel):

    inserted = productDB.insert(product)

    return inserted


@router.get('/products/{uuid}')
def getProductsByUuid(uuid: str):
    response = []
    products = productDB.getByUuid(uuid)
    for product in products:
        response.append(product)

    return response


@router.get('/products/totals/{uuid}')
def getProductTotals(uuid: str):
    response = []
    products = productDB.getTotals(uuid)
    for product in products:
        response.append(product)

    return response
