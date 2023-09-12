from models.product import Product
from models.webTypes import WebTypes
from utils.chromeDriver import chromeDriver
from utils.file import saveDBInfo
from utils.utils import fromStrToFLoat
import calendar
import time


class MarketPlace:

    def __init__(self, searchText='', uuid=''):

        if searchText == '' or uuid == '':
            return

        self.searchText = searchText
        url = f'https://www.facebook.com/marketplace/santodomingo/search?query={self.searchText}'

        soup = chromeDriver(url)

        # find page searcher and click on search button
        items = soup.find_all(
            'a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv')
        time_stamp = calendar.timegm(time.gmtime())

        # search prices, name, and store.
        for item in items:
            search = Product()
            titleConstainer = item.find(
                'span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
            priceContainer = item.find(
                'span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u')
            currency = str(priceContainer.string).strip()[0:3]
            price = str(priceContainer.string)[
                3:len(str(priceContainer.string).strip())]
            # # fields
            search.search = searchText
            search.currency = currency

            try:
                search.price = fromStrToFLoat(price)
            except:
                search.price = 0

            try:
                search.description = titleConstainer.string
            except:
                search.description = 'n/a'

            search.uuid = uuid
            search.web = WebTypes.MARKETPLACE.value

            saveDBInfo(search)
