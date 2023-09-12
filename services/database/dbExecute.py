import certifi
from pymongo import MongoClient
from models.webTypes import WebTypesStatus
from models.webTypes import WebTypes
from services.scrappers.corotos import Corotos
from services.scrappers.emarket import Emarket
from services.scrappers.laPulga import LaPulga
from services.scrappers.marketPlace import MarketPlace
from services.scrappers.mercadoLibre import MercadoLibre


class DBExecute:

    client = MongoClient(
        'mongodb+srv://admin:QLA3JHG57paGlsnT@cluster0.gjhy2xk.mongodb.net/', tlsCAFile=certifi.where())
    db = client.depoProducts

    searchText = ''
    uuid = ''

    def execute(self, webs, searchtext, uuid):
        self.searchText = searchtext
        self.uuid = uuid

        for web in webs:
            self.executeTaskByWeb(web, self.searchText, self.uuid)

    def executeTaskByWeb(self, web, searchtext, uuid):
        self.searchText = searchtext
        self.uuid = uuid

        match web:
            case WebTypes.COROTOS.value:
                self.corotos()
            case WebTypes.LAPULGA.value:
                self.laPulga()
            case WebTypes.EMARKET.value:
                self.emarket()
            case WebTypes.MERCADOLIBRE.value:
                self.mercadoLibre()
            case WebTypes.MARKETPLACE.value:
                self.marketPlace()
            case WebTypes.ALL.value:
                self.runAll()

    def corotos(self):
        print('Corotos...', self.uuid)
        Corotos(self.searchText, self.uuid)
        self.insertUpdateExecution(
            self.uuid, WebTypes.COROTOS.value, WebTypesStatus.COMPLETED.value)

    def laPulga(self):
        print('La Pulga...', self.uuid)
        LaPulga(self.searchText, self.uuid)
        self.insertUpdateExecution(
            self.uuid, WebTypes.LAPULGA.value, WebTypesStatus.COMPLETED.value)

    def emarket(self):
        print('Emarket...', self.uuid)
        Emarket(self.searchText, self.uuid)
        self.insertUpdateExecution(
            self.uuid, WebTypes.EMARKET.value, WebTypesStatus.COMPLETED.value)

    def mercadoLibre(self):
        print('Mercado Libre...', self.uuid)
        MercadoLibre(self.searchText, self.uuid)
        self.insertUpdateExecution(
            self.uuid, WebTypes.MERCADOLIBRE.value,  WebTypesStatus.COMPLETED.value)

    def marketPlace(self):
        print('Market Place...', self.uuid)
        MarketPlace(self.searchText, self.uuid)
        self.insertUpdateExecution(
            self.uuid, WebTypes.MARKETPLACE.value,  WebTypesStatus.COMPLETED.value)

    def runAll(self):
        self.corotos()
        self.laPulga()
        self.emarket()
        self.mercadoLibre()
        self.marketPlace()

    def insertUpdateExecution(self, uuid, web, status=WebTypesStatus.STARTED.value):

        query = {'uuid': uuid, 'web': web}
        update = {'$set': {'uuid': uuid, 'web': web, 'status': status}}

        return self.db.executions.update_one(query, update, upsert=True)

    def getExecutions(self):
        executions = []

        for execution in self.db.executions.distinct('uuid'):
            where = {'uuid': {'$eq': execution}}
            count = self.db.products.count_documents(where)

            if (count > 0):
                executions.append(execution)

        return executions

    def getExecutionsByUuid(self, uuid):
        executions = []

        where = {'uuid': {'$eq': uuid}}

        for execution in self.db.executions.find(where):
            executions.append(execution)

        return executions

    def delete(self, uuid):
        # Define the conditions for the AND operation

        where = {'uuid': {'$eq': uuid}}

        self.db.executions.delete_many(where)
