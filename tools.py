import re
import datetime


class Tools:

    @staticmethod
    def convert(s):
        s = s.strip('&#x;')
        s = bytes(r'\u' + s, 'ascii')
        return s.decode('unicode_escape')

    @staticmethod
    def list2Dic(keysList, valuesList):
        """
        将两个列表合并成一个字典
        :param keysList:
        :param valuesList:
        :return:
        """
        return dict(zip(keysList, valuesList))

    @staticmethod
    def getMaxDic(dic, reverse=True):
        """
        获取一个字典中值最大的元素组成新的单个元素字典 {'d1': 2,'d2': 4,'d3':3}
        :param dic:
        :return:
        """
        maxDic = {}
        s = [k for k in sorted(dic,key=dic.__getitem__, reverse=reverse)][0]
        maxDic[s] = dic.get(str(s))
        return maxDic

    @classmethod
    def get_cssEncryption_str(cls, strData):
        """
        处理类似<div>&#xFF08;2015&#xFF09;</div>的数据
        :param strData:
        :return:
        """
        return re.sub(r'&#x....;', lambda match: cls.convert(match.group()), strData)

    @classmethod
    def get_cleanHtml_str(cls, html):
        """
        返回去掉html标签的纯净文本
        :param strData:
        :return:
        """
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html).strip()
        return dd

    @classmethod
    def get_rankListDic(cls, lis, reverse=True):
        """
        将装有字典的列表，按照字典中值的大小进行排序，[{'1':1},{'2':2},{'4':4},{'3':3}]
        :param list:
        :return:
        """
        dic = {}
        rankeData = []
        for n in lis:
            dic[list(n.values())[0]] = n
        l = list(dic.keys())
        l.sort(reverse=reverse)
        for x in l:
            rankeData.append(dic[x])
        return rankeData

    @classmethod
    def dateStrTodatetime(cls, dateStr):
        """
        将时间字符串转为 datetime.datetime 格式 "2019-08-26"
        :param dateStr:
        :return:
        """
        dateDic = cls.list2Dic(keysList=['year', 'month', 'day'], valuesList=dateStr.split('-'))
        date = datetime.date(int(dateDic['year']), int(dateDic['month']), int(dateDic['day']))
        return date



