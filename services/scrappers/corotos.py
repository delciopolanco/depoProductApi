from models.product import Product
from models.webTypes import WebTypes
from utils.chromeDriver import chromeDriver
from utils.file import saveDBInfo
from utils.utils import fromStrToFLoat
import calendar
import time


class Corotos:

    def __init__(self, searchText='', uuid=''):

        if searchText == '' or uuid == '':
            return

        self.searchText = searchText

        for i in range(1, 5):

            url = f'https://www.corotos.com.do/k/{searchText}&page{i}'
            soup = chromeDriver(url)

            # find page searcher and click on search button
            items = soup.find_all(
                'div', class_='flex transition group flex-col space-y-3 mb-8 border-b border-gray-4 border-solid')
            pageCount = str(
                soup.find(class_="location__results").text).strip().split()[0]

            time_stamp = calendar.timegm(time.gmtime())

            # search prices, name, and store.
            for item in items:
                search = Product()
                priceContainer = item.find('div', class_='price-info')
                storeContainer = item.find(attrs={'target': '_blank'})
                # fields
                search.search = searchText
                search.currency = str(priceContainer.find(
                    'span', class_='text-overline').text).strip()
                search.price = fromStrToFLoat(str(priceContainer.find(
                    'span', class_='text-title-3 ml-1').text).strip())
                search.description = str(item.find(
                    'h3', class_='text-body-2 m-0 md:mb-2 truncate-2-line md:h-12').text).strip()
                search.uuid = uuid
                search.web = WebTypes.COROTOS.value
                try:
                    search.store = str(storeContainer['id']).replace(
                        '-verify-icon', '').strip()
                except:
                    search.store = 'n/a'

                saveDBInfo(search)

            if pageCount == "0":
                return
