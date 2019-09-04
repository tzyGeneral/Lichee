# -*- coding:utf-8 -*-
import re
import datetime
import zipfile
import os
import random
import hashlib
import time


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

    @classmethod
    def date2Zodiac(cls, month, day):
        """
        根据输入的月份与日，获取星座信息
        :param month:
        :param day:
        :return:
        """
        n = ('摩羯座','水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座')
        d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
        return n[len(list(filter(lambda y: y <= (month, day), d))) % 12]

    @staticmethod
    def zipOneFile(dirpath, outFullName):
        """
        压缩指定文件
        :param dirpath:
        :param outFullName:
        :return: None
        """
        # dirpath 目标文件  like: C:\Users\zhenyuan\Desktop\233.txt
        # outFullName: 压缩文件保存路径 + xxx.zip  like: C:\Users\zhenyuan\Desktop\233.zip
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
        baseName = os.path.basename(dirpath)
        fpath = dirpath
        zip.write(fpath, arcname=baseName)
        zip.close()

    @staticmethod
    def zipManyFile(dirpath, outFullName):
        """
        压缩指定文件夹
        :param dirpath:
        :param outFullName:
        :return: None
        """
        # dirpath: 目标文件夹路径  like: C:\Users\zhenyuan\Desktop\233
        # outFullName: 压缩文件保存路径 + xxx.zip  like: C:\Users\zhenyuan\Desktop\233.zip
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()

    @staticmethod
    def getDayStr(dayNum):
        """
        获取从当天开始往回推dayNum天的时间字符串
        :param dayNum:
        :return:
        """
        dayStrList = []
        for index in range(1,dayNum):
            day = (datetime.datetime.now() - datetime.timedelta(days=index)).date().__str__()
            dayStrList.append(day)
        return dayStrList

    @staticmethod
    def getRandomStr(randomlength=16):
        """
        生成一个指定长度的随机字符串
        :param randomlength:
        :return:
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    @staticmethod
    def getHashEncodeData(string: str):
        """
        hash加密字符串
        :param string:
        :return:
        """
        hash_sha1 = hashlib.sha1(string.encode('utf-8')).hexdigest()
        return hash_sha1

    @staticmethod
    def getMd5EncodeData(string: str):
        """
        Md5加密字符串
        :param string:
        :return:
        """
        hash_md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
        return hash_md5

    @staticmethod
    def getUTCtimesmap():
        """
        获取当前UTC时间的时间戳
        :return:
        """
        return str(int(round(time.time() * 1000)))





