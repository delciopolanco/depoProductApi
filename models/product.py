class Product:

    id = ''
    search = ''
    price = 0
    currency = ''
    store = ''
    description = ''
    web = '',
    uuid = ''

    def __init__(self, search = '', price = 0, currency = '', store = 'n/a', description = '', web = '', uuid = '', id = ''):

        self.search = search
        self.price = price
        self.currency = currency
        self.store = store
        self.description = description
        self.web = web
        self.uuid = uuid
        self.id = id

    def __str__(self):
        return f"{self.currency} {self.price} {self.store} {self.description}"