from models.product import Product
from models.webTypes import WebTypes
from utils.chromeDriver import chromeDriver
from utils.file import saveDBInfo
from utils.utils import fromStrToFLoat
import calendar
import time


class Emarket:

    def __init__(self, searchText='', uuid=''):

        if searchText == '' or uuid == '':
            return

        self.searchText = searchText
        url = f'https://emarket.do/producto/buscar?q={searchText}'
        soup = chromeDriver(url)

        # find page searcher and click on search button
        items = soup.find_all('a', class_='search-result__post')

        time_stamp = calendar.timegm(time.gmtime())

        # search prices, name, and store.
        for item in items:
            search = Product()
            priceContainer = item.find('h3', class_='post__body__price')
            storeContainer = item.find('div', class_='post__detail')
            store = storeContainer.find_all(
                'div', class_='post__detail__block')[2]

            # fields
            search.search = searchText
            search.currency = str(priceContainer.text).strip()[0:3]
            search.price = fromStrToFLoat(str(priceContainer.text).strip()[
                                          3:len(priceContainer.text)])
            search.description = str(
                item.find('h3', class_='post__body__title').text).strip()
            search.store = str(store.find(
                'p', class_='ng-binding').text).strip()
            search.uuid = uuid
            search.web = WebTypes.EMARKET.value

            saveDBInfo(search)
