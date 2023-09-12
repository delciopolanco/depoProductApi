from typing import List
from fastapi import APIRouter, BackgroundTasks
from models.webTypes import WebTypes
from viewmodels.executions import ExecutionViewModel
from services.database.dbProducts import DBProducts
from services.database.dbExecute import DBExecute


router = APIRouter()


@router.delete('/execute/{uuid}')
def deleteProducts(uuid: str):
    productDB = DBProducts()
    productDB.delete(uuid)
    executionDB = DBExecute()
    executionDB.delete(uuid)

    return 'OK'


@router.get('/execute')
def getExecutions():
    response = []
    executionDB = DBExecute()
    executions = executionDB.getExecutions()
    for uuid in executions:
        response.append({'uuid': uuid})

    return response


def execute(scrapp: ExecutionViewModel):
    executionDB = DBExecute()

    if (WebTypes.ALL.value in scrapp.webs):
        webInsertions = [WebTypes.COROTOS.value, WebTypes.EMARKET.value,
                         WebTypes.LAPULGA.value, WebTypes.MARKETPLACE.value,  WebTypes.MERCADOLIBRE.value]
    else:
        webInsertions = scrapp.webs

    for web in webInsertions:
        executionDB.insertUpdateExecution(scrapp.uuid, web)

    executionDB.execute(scrapp.webs,
                        scrapp.searchText, scrapp.uuid)


@router.post('/execute')
async def executeTask(scrapp: ExecutionViewModel, bgTask: BackgroundTasks):

    bgTask.add_task(execute, scrapp)

    return 'OK'
