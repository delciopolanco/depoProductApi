from models.product import Product
from models.webTypes import WebTypes
from utils.chromeDriver import chromeDriver
from utils.file import saveDBInfo
from utils.utils import fromStrToFLoat, joinStr, splitStr
import calendar
import time


class MercadoLibre:

    def __init__(self, searchText='', uuid=''):

        if searchText == '' or uuid == '':
            return

        self.searchText = joinStr(splitStr(searchText))
        url = f'https://listado.mercadolibre.com.do/{self.searchText}'

        soup = chromeDriver(url)

        # find page searcher and click on search button
        items = soup.find_all('div', class_='ui-search-result--core')

        time_stamp = calendar.timegm(time.gmtime())

        # search prices, name, and store.
        for item in items:
            search = Product()
            titleConstainer = item.find('h2', class_='ui-search-item__title')

            # #fields
            search.search = searchText
            search.currency = str(
                item.find('span', class_='andes-money-amount__currency-symbol').text).strip()
            search.price = fromStrToFLoat(
                item.find('span', class_='andes-money-amount__fraction').text)
            search.description = str(titleConstainer.text).strip()
            search.uuid = uuid
            search.web = WebTypes.MERCADOLIBRE.value

            saveDBInfo(search)
