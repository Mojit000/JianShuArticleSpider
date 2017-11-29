import pandas as pd
import numpy
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pymongo
def read_data():
    """
    读取MongoDB数据
    """
    client = MongoClient()
    db = client.JIANSHU
    collection = db.WEEKLY
    data = pd.DataFrame(set(collection.find()))
    return data


data = read_data()
userClientCol = ['作者', '次数']
# 注意：需数组转置
userClientDataFrame = pd.DataFrame(numpy.array([list(set(data.get('author'))), [list(data.get('author')).count(level) for level in list(set(data.get('author')))]]).T, columns=userClientCol)
# 按照作者发布的文章数量进行排序
userClientDataFrame = userClientDataFrame.sort_values('次数', ascending=False)
# 选取文章数量前20名作者
userClientDataFrame = userClientDataFrame.head(20)
plt.figure(figsize=(20,8),dpi=100)
labels = list(userClientDataFrame['作者'])
plt.bar(range(len(labels)),userClientDataFrame['次数'],tick_label=labels)
plt.title('作者')
plt.show()