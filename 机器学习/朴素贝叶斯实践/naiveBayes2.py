# _*_ coding:utf-8 _*_
from numpy import *
import jieba.analyse
import json


class DataSet:
    """
    处理样例数据 和 测试数据，提供分词方法
    """

    def loadDataSet(self):
        """
        创建样例数据
        :return:
        """
        with open('train_data.json', 'r') as load_f:
            load_dict = json.load(load_f)

            postingList = []
            classVec = []
            for one in load_dict['data']:
                classVec.append(one.pop())
                postingList.append(one)

        return postingList, classVec

    def loadTestDataSet(self):
        """
        创建测试数据(正向)
        :return:
        """
        with open('test_data.json', 'r') as load_f:
            load_dict = json.load(load_f)

            testDataSet = load_dict['data']

        return testDataSet

    def cutWorldTool(self, string: str):
        """
        将中文的电影简介进行分词,使用tf-idf算法进行取词
        :return:
        """
        lis = []
        keywords = jieba.analyse.extract_tags(string, topK=100, withWeight=True, allowPOS=('n', 'vn', 'ns'))
        for item in keywords:
            lis.append(item[0])

        return lis


class NaiveBayes:
    def __init__(self):
        self.dataHeader = DataSet()

    def createVocabList(self, dataSet):  # 创建词库 这里就是直接把所有词去重后，当作词库
        vocabSet = set([])
        for document in dataSet:
            vocabSet = vocabSet | set(document)
        return list(vocabSet)

    def setOfWords2Vec(self, vocabList, inputSet):  # 文本词向量。词库中每个词当作一个特征，文本中就该词，该词特征就是1，没有就是0
        returnVec = [0] * len(vocabList)
        for word in inputSet:
            if word in vocabList:
                returnVec[vocabList.index(word)] = 1
            else:
                # print("the word: %s is not in my Vocabulary!" % word)
                pass
        return returnVec

    def trainNB0(self, trainMatrix, trainCategory):
        numTrainDocs = len(trainMatrix)
        numWords = len(trainMatrix[0])
        pAbusive = sum(trainCategory) / float(numTrainDocs)
        p0Num = ones(numWords) # 防止某个类别计算出的概率为0，导致最后相乘都为0，所以初始词都赋值1，分母赋值为2.
        p1Num = ones(numWords)
        p0Denom = 2
        p1Denom = 2
        for i in range(numTrainDocs):
            if trainCategory[i] == 1:
                p1Num += trainMatrix[i]
                p1Denom += sum(trainMatrix[i])
            else:
                p0Num += trainMatrix[i]
                p0Denom += sum(trainMatrix[i])
        p1Vect = log(p1Num / p1Denom)  # 这里使用了Log函数，方便计算，因为最后是比较大小，所有对结果没有影响。
        p0Vect = log(p0Num / p0Denom)
        return p0Vect, p1Vect, pAbusive

    def classifyNB(self, vec2Classify, p0Vec, p1Vec, pClass1):  # 比较概率大小进行判断，
        p1 = sum(vec2Classify*p1Vec)+log(pClass1)
        p0 = sum(vec2Classify*p0Vec)+log(1-pClass1)
        if p1>p0:
            return 1
        else:
            return 0

    def testingNB(self):
        listOPosts, listClasses = self.dataHeader.loadDataSet()

        myVocabList = self.createVocabList(listOPosts)
        trainMat=[]
        for postinDoc in listOPosts:
            trainMat.append(self.setOfWords2Vec(myVocabList, postinDoc))
        p0V,p1V,pAb = self.trainNB0(array(trainMat),array(listClasses))

        for one in self.dataHeader.loadTestDataSet():
            testEntry = self.dataHeader.cutWorldTool(one) # 将数据分词
            # testEntry = NaiveBayes().getBadData() # 测试数据

            if testEntry:
                thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
                print(one,'classified as: ',self.classifyNB(thisDoc,p0V,p1V,pAb))

        # data = b.getDataFromDatabase('32641')
        data = """广西桂林战事紧急，始安城中学“小霸王”莫家军、“小宋江”杜少维等学生赴前线劳军，日军意外发现这群学生，指挥官浅川得知学生里有始安城守城司令莫啸川之子，决意要活捉这帮孩子，学生出日军魔掌。随后，广西全境征学生兵，莫家军、杜少维等人纷纷参军。一次胜仗之后，学生军正准备回城给家长们报喜，但没想到，浅川率军攻城，莫啸川带领部队进行殊死抵抗，最终全军覆没。共产党教官孙鼎昌带领着学生兵投入战斗，但敌众我寡，孙鼎昌为学生兵能安全脱险，壮烈牺牲。莫家军带领全体人杀出重围，逃进密林。城破家亡，学生兵誓要让浅川血债血偿，加入赣南游击队后，他们一次次跟浅川在丛林间进行殊死搏斗，破坏了浅川对矿产资源的阴谋，最终除掉浅川。随后，莫家军等人加入新四军，踏上新的征程"""
        testEntry = self.dataHeader.cutWorldTool(data)
        # testEntry = NaiveBayes().getDataFromDatabase('28037') # 测试数据
        thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
        print(testEntry,'classified as: ', self.classifyNB(thisDoc,p0V,p1V,pAb))


if __name__ == '__main__':
    NaiveBayes().testingNB()
