from models.product import Product
from models.webTypes import WebTypes
from utils.chromeDriver import chromeDriver
from utils.file import saveDBInfo
from utils.utils import fromStrToFLoat
import calendar
import time


class LaPulga:

    def __init__(self, searchText='', uuid=''):

        if searchText == '' or uuid == '':
            return

        self.searchText = searchText

        for i in range(1, 5):

            url = f'https://www.lapulga.com.do/busquedas/{searchText.replace(" ", "-")}?pag={i}'
            soup = chromeDriver(url)
            # find page searcher and click on search button
            items = soup.find_all('div', class_='card')

            noRegistry = soup.find(id="noregistros")

            if noRegistry != None:
                return

            time_stamp = calendar.timegm(time.gmtime())

            # search prices, name, and store.
            for item in items:
                search = Product()
                container = item.find('div', class_='card-title')
                titleConstainer = container.find('div', class_='title').h3
                priceContainer = container.find('div', class_='title').h2
                currency = str(priceContainer.text).strip()[0:3]
                price = str(priceContainer.text.strip())[
                    3:len(priceContainer.text)]

                # fields
                search.search = searchText
                search.currency = currency
                search.price = fromStrToFLoat(price)
                search.description = str(titleConstainer.text).strip()
                search.uuid = uuid
                search.web = WebTypes.LAPULGA.value

                saveDBInfo(search)
