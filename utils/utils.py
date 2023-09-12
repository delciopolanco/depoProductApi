def fromStrToFLoat(text: str):
    return float(text.replace(',', '').strip())

def splitStr(string: str):
 
    # Split the string based on space delimiter
    string = string.split(' ')
     
    return string
 
def joinStr(string: str):
    # Join the string based on '-' delimiter
    string = '-'.join(string)
     
    return string