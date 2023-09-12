from enum import Enum

class WebTypes(Enum):
    COROTOS = 'Corotos'
    EMARKET = 'Emarket'
    LAPULGA = 'LaPulga'
    MARKETPLACE = 'MarketPlace'
    MERCADOLIBRE = 'MercadoLibre'
    ALL = 'All'

class WebTypesStatus(Enum):
    STARTED = 0
    COMPLETED = 1