# -*- coding:utf-8 -*-
import re
import datetime
import zipfile
import os
import random
import hashlib
import time
from collections.abc import *


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

    @staticmethod
    def get2ListIntersection(list1: list, list2: list) ->list:
        """
        获取两个列表的交集
        l1 = [1,2,3,4,5,6,7]
        l2 = [6,7,8,9,0]
        :return:
        """
        return list(set(list1).difference(set(list2)))

    @staticmethod
    def getListProduct(lis: list) ->int:
        """
        获取一个列表的乘积
        :param lis:
        :return:
        """
        from functools import reduce
        product = reduce((lambda x, y: x*y), lis)
        return product

    @staticmethod
    def getNameDic(lis):
        """
        将一个列表中的小列表按照第一个元素为键生成字典
        colours = (
            ('Yasoob', 'Yellow'),
            ('Ali', 'Blue'),
            ('Arham', 'Green'),
            ('Ali', 'Black'),
            ('Yasoob', 'Red'),
            ('Ahmed', 'Silver'),
        )
        :param list:
        :return:
        """
        from collections import defaultdict
        favourite_colours = defaultdict(list)
        for key, value in lis:
            favourite_colours[key].append(value)

        return favourite_colours

    @staticmethod
    def listToInt(intList: list) -> int:
        """
        将列表里所有的整数组成一个整数
        :param intList:
        :return:
        """
        a = [i * 10 ** index for index, i in enumerate(intList[::-1])]
        b = sum(a)
        return b

    @classmethod
    def manyListToOne(cls, lst, out_list=None) -> list:
        """
        让多个嵌套列表展开为一维列表
        :param lst:
        :return:
        """
        if out_list is None:
            out_list = []
        for i in lst:
            if isinstance(i, Iterable):  # 判定i是否可迭代
                cls.manyListToOne(i, out_list)  # 尾数递归
            else:
                out_list.append(i)
        return out_list

    @classmethod
    def splitList(cls, initList: list, childernListLen: int) -> list:
        """
        将列表分割为指定大小的小列表
        :param initList: 待分割的原始列表
        :param childernListLen: 分割大小
        :return:
        """
        list_of_group = zip(*(iter(initList),) * childernListLen)
        end_list = [list(i) for i in list_of_group]
        count = len(initList) % childernListLen
        end_list.append(initList[-count:]) if count != 0 else end_list
        return end_list

    @classmethod
    def rankDicList(cls, inputList: list, sortKey: str, reverseType=True) -> list:
        """
        将列表中有字典，根据字典中的某个值排序
        例: inputList = [{'name':'zs','age':12},{'name':'ls','age':16},{'name':'ww','age':10}]
        :param inputList:
        :return:
        """
        keyCheck = inputList[0].get(sortKey, '')
        if not keyCheck:
            assert KeyError("排序的键不存在")
        return sorted(inputList, key=lambda x: x[sortKey], reverse=reverseType)

    @classmethod
    def rankDicListTwo(cls, inputList: list, sortKeyOne: str, sortKeyTwo: str, reverseType=True) -> list:
        """
        将列表中有字典，根据字典中的某个值排序，如果第一个条件相同，则按照第二个条件排序
        :param inputList:
        :param sortKeyOne:
        :param sortKeyTwo:
        :return:
        """
        keyCheckOne, keyCheckTwo = inputList[0].get(sortKeyOne, ''), inputList[0].get(sortKeyTwo, '')
        if not keyCheckOne or not keyCheckTwo:
            assert KeyError("排序的键不存在")
        return sorted(inputList, key=lambda x: (x[sortKeyOne], x[sortKeyTwo]), reverse=reverseType)



l = Tools.getNameDic([
            ('Yasoob', 'Yellow'),
            ('Ali', 'Blue'),
            ('Arham', 'Green'),
            ('Ali', 'Black'),
            ('Yasoob', 'Red'),
            ('Ahmed', 'Silver'),
])
print(l)








