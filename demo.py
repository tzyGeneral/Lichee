from tools import Tools


print(Tools.get_rankListDic([{'1':1},{'2':2},{'4':4},{'3':3}]))

print(Tools.get_cssEncryption_str("<div>&#xFF08;2015&#xFF09;</div>"))

print(Tools.get_cleanHtml_str('<div>（2015）</div>'))

print(Tools.dateStrTodatetime("2019-08-26"))

print(Tools.getMaxDic({'d1': 2,'d2': 4,'d3':3},reverse=False))

print(Tools.date2Zodiac(5,12))