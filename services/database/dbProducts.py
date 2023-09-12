import certifi
from bson import ObjectId
from pymongo import MongoClient
import pymongo
from models.product import Product
from models.totalProduct import TotalProduct


class DBProducts:

    client = MongoClient(
        'mongodb+srv://admin:QLA3JHG57paGlsnT@cluster0.gjhy2xk.mongodb.net/', tlsCAFile=certifi.where())
    db = client.depoProducts

    def getByUuid(self, uuid):
        users = []

        # Define the conditions for the AND operation
        where = {'uuid': {'$eq': uuid}}

        for doc in self.db.products.find(where).sort("price", pymongo.ASCENDING):
            id = doc.get('_id')

            if (id != None):
                id = str(ObjectId(doc['_id']))

            users.append(Product(doc.get('search'),
                                 doc.get('price'),
                                 doc.get('currency'),
                                 doc.get('store'),
                                 doc.get('description'),
                                 doc.get('web'),
                                 doc.get('uuid'),
                                 id))

        return users

    def getByWebAndUuid(self, web, uuid):
        users = []

        # Define the conditions for the AND operation

        where = {
            '$and': [
                {'uuid': {'$eq': uuid}},
                {'web': {'$eq': web}}
            ]
        }

        for doc in self.db.products.find(where):
            id = doc.get('_id')

            if (id != None):
                id = str(ObjectId(doc['_id']))

            users.append(Product(doc.get('search'),
                                 doc.get('price'),
                                 doc.get('currency'),
                                 doc.get('store'),
                                 doc.get('description'),
                                 doc.get('web'),
                                 doc.get('uuid'),
                                 id))

        return users

    def getExecutionsByUuid(self, uuid):
        executions = []

        where = {'uuid': {'$eq': uuid}}

        for execution in self.db.executions.find(where):
            executions.append(execution)

        return executions

    def getTotals(self, uuid):
        products = []
        websInTotals = []
        websInExecutions = []

        # Define the conditions for the AND operation

        match = {
            '$match': {
                'uuid':  uuid,
            }
        }

        groupBy = {
            '$group': {
                '_id': '$web',
                'search': {'$first': '$search'},
                'prices': {'$min': '$price'},
                'count': {'$sum': 1}

            }
        }

        alias = {
            '$project': {
                '_id': 0,
                'web': '$_id',
                'minPrice': '$prices',
                'total': '$count',
                'search': '$search'
            }
        }

        for doc in self.db.products.aggregate([match, groupBy, alias]):
            websInTotals.append(doc.get('web'))
            products.append(TotalProduct(doc.get('web'),
                                         doc.get('minPrice'),
                                         doc.get('total'),
                                         doc.get('search')))

        # To identify if there is any execution that hasn't finished yet
        where = {'uuid': {'$eq': uuid}, 'status': {'$eq': 0}}
        executionNotFinished = self.db.executions.count_documents(where)

        if (executionNotFinished > 0):
            return []

         # To identify webs in executions
        where = {'uuid': {'$eq': uuid}}
        executions = self.db.executions.find(where)

        # identify those executions that finished but where didn't found anything
        for doc in executions:
            websInExecutions.append(doc.get('web'))

         # if exist, we need to return an empty totals of these.
        emptyWebs = list(set(websInExecutions) - set(websInTotals))

        for web in emptyWebs:
            products.append(TotalProduct(
                web, 0.00, 0, products[0].search if len(products) > 0 else ''))

        if (self.didRunnersFinished(products, websInExecutions) == False):
            return []

        return products

    def didRunnersFinished(self, totals, executions):

        uuidInProductsCount = len(totals)
        uuidInExecutionCount = len(executions)

        if (uuidInProductsCount != uuidInExecutionCount):
            return False

        return True

    def insert(self, product: Product):
        id = self.db.products.insert_one({
            'search': product.search,
            'web': product.web,
            'description': product.description,
            'store': product.store,
            'currency': product.currency,
            'price': product.price,
            'uuid': product.uuid
        })

        inserted = product
        inserted.id = str(ObjectId(id.inserted_id))
        return inserted

    def delete(self, uuid):
        # Define the conditions for the AND operation

        where = {'uuid': {'$eq': uuid}}

        self.db.products.delete_many(where)
