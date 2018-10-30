# 第一周工作记录

<!-- Write By JChrysanthemum at 2018.10.30 -->


<br>

##一、总表
<br>

|时间|目标|阶段性成果|存在的问题
|:---:|:---|:---|:---|
|2016.10.21<br>*<br>2018.10.27|1.仔细阅读[天池服装搭配](https://tianchi.aliyun.com/competition/introduction.htm?spm=5176.11165320.5678.1.483f660e4d5X12&raceId=231575)比赛介绍，思考方案并进行讨论。<br>2.下载并部署数据，对数据进行简单分析。<br>3.对商品图片文件进行分类。<br>4.将项目部署至github方便管理。|1.发现数据分布并不均匀([图片一](https://github.com/lzutianchi/TBClothe/blob/master/Log/data/dim_fashion_matchsets_data_alternativeCount.png) [图片二](https://github.com/lzutianchi/TBClothe/blob/master/Log/data/dim_fashion_matchsets_data_packageCount.png))<br>2.通过讨论决定首先进行图片文件的分类工作，并通过初步实验和讨论决定使用若干网络共同识别来提高准确率。<br>3.实验得出使用vgg16和xception网络进行共同识别有着相对不错的效果，得出的[分类结果](https://github.com/lzutianchi/TBClothe/blob/master/Log/data/items(v1).txt)，试验结果的结果统计见本总结附录|1.结合网络可能均出现识别错误的问题，导致识别一致性偏移，需要验证。|

<br>

##二、附录
<br>

###2.1 第一阶段分类成果统计
<br>

[items(v1).txt](https://github.com/lzutianchi/TBClothe/blob/master/Log/data/items(v1).txt)
<br>


|前(i)分类|前i项目分类包含商品数占比|
|:---:|:---:|
|5|39.88%|
|10|53.29%|
|20|68.97%|
|30|78.96%|
|50|87.99%|
|70|91.74%|

* 分类已按照其包含的商品数降序排序
* 两个网络识别概率top5无重合标签为None
> [1,2,3,4,5] & [2,4,7,8,9] -> 2 <br> [1,2,3,4,5] & [9,8,7,6,10] -> 'None'
* 'None'标签包含商品数占商品总数的 **6.23%**
> 相较于单独网络识别时 **200+** 类才能覆盖70%左右数据情况来说，多个网络混合识别效果相对较好