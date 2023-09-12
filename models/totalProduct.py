class TotalProduct:

    web = '',
    minPrice = 0
    total = 0
    search = ''
    
    def __init__(self, web = '', minPrice = 0, total = 0, search = ''):
        self.web = web
        self.minPrice = minPrice
        self.total = total
        self.search = search
      

    def __str__(self):
        return f"{self.web} {self.minPrice} {self.total} {self.search}"