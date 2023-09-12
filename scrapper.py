from services.scrappers.corotos import Corotos
from services.scrappers.emarket import Emarket
from services.scrappers.laPulga import LaPulga
from services.scrappers.marketPlace import MarketPlace
from services.scrappers.mercadoLibre import MercadoLibre


class Scrapper:
    searchText = ''
    uuid = ''
    
    def __init__(self, searchText='', uuid=''):
        self.searchText = searchText
        self.uuid = uuid
    
    def corotos(self):
        print('Corotos...', self.uuid)
        Corotos(self.searchText, self.uuid)

    def laPulga(self):
        print('La Pulga...', self.uuid)
        LaPulga(self.searchText, self.uuid)

    def emarket(self):
        print('Emarket...', self.uuid)
        Emarket(self.searchText, self.uuid)

    def mercadoLibre(self):
        print('Mercado Libre...', self.uuid)
        MercadoLibre(self.searchText, self.uuid)

    def marketPlace(self):
        print('Market Place...', self.uuid)
        MarketPlace(self.searchText, self.uuid)



    def runAll(self):
        self.corotos()
        self.laPulga()
        self.emarket()
        self.mercadoLibre()
        self.marketPlace()
    


if __name__ == "__main__":
    Scrapper()