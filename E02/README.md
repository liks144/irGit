#E02 Ranked Retrival

##实验任务和实现效果
1. 在Homework1.1的基础上实现最基本的Ranked retrieval model
	• Input： a query (like Ron Weasley birthday)
	• Output: Return the top K (e.g., K = 10) relevant tweets.
	• Use SMART notation: lnc.ltc
	• Document: ***logarithmic tf*** (l as first character), _**no idf**_  and _**cosine normalization**_
	• Query: _**logarithmic tf**_  (l in leftmost column), _**idf**_ (t in second column), _**nonormalization**_
2. 改进Inverted index
	• 在Dictionary中存储每个term的DF
	• 在posting list中存储term在每个doc中的TF with pairs (docID, tf)

	实验目前实现了**lnc.ltn**模型，将Inverted index 中的每一个docID改为(docID,tf)，调用函数计算DF 没有实现其他SMART模型

##实验过程
####一、数据处理
​	数据处理和实验1.1相同，读入文本，返回一个每一行tweet term 的列表，列表第一个元素是tweetid

![[数据处理]](https://github.com/liks144/irGit/blob/master/E02/img/Screen%20Shot%202019-10-22%20at%2015.45.20.png)

####二、索引构建
​	利用collection中的count方法将列表转换成（词项：词频）的字典，然后用items属性变成键值对，构建一个列表，元组（词项：词频）是一个元素。
这样索引就能用下面的方法构建，索引的每一个键是term，每一个值是一个列表，包含（docID，词频）。

![索引构建](https://github.com/liks144/irGit/blob/master/E02/img/Screen%20Shot%202019-10-22%20at%2015.56.47.png)

构建方法示例：

![[索引构建]](https://github.com/liks144/irGit/blob/master/E02/img/Screen%20Shot%202019-10-22%20at%2015.05.27.png)

在构建字典时要记录每条tweet的长度，用一个字典保存即可。

####三、检索 Search()
​	在这个函数中接受一个query，和tweet做同样的token返回一个list，根据list去查posting，然后对遇到的每个docID进行打分并把结果记录到visit\{\}里, Search_document()是一个计算分值的函数，接收一个docID，返回Query和这个ID的分支。最后对这个visit排序并取前K个即可。

![[Search]](https://github.com/liks144/irGit/blob/master/E02/img/Screen%20Shot%202019-10-22%20at%2016.20.11.png)

​	这里比较重要的就是这个Search_document()函数，找到一个尚未访问的document，执行这个函数，算出所需要的tf_wght和normalize项，直接在这个函数中计算余弦相似度。

![[re\_doc]](https://github.com/liks144/irGit/blob/master/E02/img/Screen%20Shot%202019-10-22%20at%2015.56.37.png)

##实验结果
![实验结果](https://github.com/liks144/irGit/blob/master/E02/img/Screen%20Shot%202019-10-22%20at%2015.00.10.png)

##实验评价和改进

​	在上一个实验的基础上实现最基本的Ranked retrieval model，Use SMART notation: lnc.ltc

这次试验做的时间比较长，下次要快一点。