# 实验一 倒排索引与布尔查询

## 实验目标及完成情况：

- 使用介绍的方法，在 tweets 数据集上构建 inverted  index;
- 实现 Boolean Retrieval Model 
- Boolean Retrieval Model:
  - Input a query
  - Output the qualified tweets
  - 支持and or not

- 实现了任意长度的查询以及比较自然的以空格代替 and
- 用的课上讲的O(N)的算法

## 实验过程：

### 	对tweets数据集进行预处理

![Screen Shot 2019-10-10 at 11.01.55](https://github.com/liks144/irGit/blob/master/images/Screen%20Shot%202019-10-10%20at%2011.01.55.png)

​	观察发现tweet数据集结构比较统一。有用信息主要包括"username" "text"和"tweetid"。第一步需要进行normalize 并删去不需要的词段。

![Screen Shot 2019-10-10 at 11.16.31](https://github.com/liks144/irGit/blob/master/images/Screen%20Shot%202019-10-10%20at%2011.16.31.png)

做过分词、normalize并删去无关词段后

使用字典结构构建倒排索引表，其中每个term作为key，值为包含这个term的tweetid：

![Screen Shot 2019-10-10 at 11.17.16](https://github.com/liks144/irGit/blob/master/images/Screen%20Shot%202019-10-10%20at%2011.17.16.png)

取前100条做出来的倒排索引表。

### 对Query的处理

- 注意对query和tweets要进行相同的预处理，所以这里调用同一个函数即可

![Screen Shot 2019-10-10 at 17.08.27](https://github.com/liks144/irGit/blob/master/images/Screen%20Shot%202019-10-10%20at%2017.08.27.png)

### 对预处理过的Query做查询

实验采用了一种“流”的方式逐个查询Query中的Term，声明一个PRESET列表，然后逐个与Query中的Term做and、or、not查询，将结果更新到PRE中

![Screen Shot 2019-10-10 at 21.12.42](https://github.com/liks144/irGit/blob/master/images/Screen%20Shot%202019-10-10%20at%2021.12.42.png)

三种逻辑操作均采用**课上讲的算法**，这要求PRESET的中间状态也要保持有序。为了实现这个目的，实验采用了一种“哨兵”的方法，即在两个需要做and或or的列表最后加一个最大的ID值：

![Screen Shot 2019-10-10 at 21.25.48](https://github.com/liks144/irGit/blob/master/images/Screen%20Shot%202019-10-10%20at%2021.25.48.png)

例如，在两个列表做or时，两个指针按情况向后移动，较快的最终回卡在ID_MAX上，直到较慢的列表元素全部放进结果中。这样保证了在复杂度是**线性**的情况下中间结果有序。

## 实验结果分析：

简单的逻辑效果：

and：

```bash
>>sargent and servando
['28967095878287360']
```

```bash
>>sargent servando
['28967095878287360']
```

or：

```bash
>>sargent or servando
['28967095878287360', '29012766593384448', '29208901270380544', '29355674039230464', '29910567581913089', '302176719081713664']
```

not：

```bash
>>sargent not servando
['29012766593384448', '29208901270380544', '29355674039230464', '302176719081713664']
```

多个关键词查询：

```bash
>>Mourners recall Sarge Shriver's charity
['28967095878287360', '29105101847138304']
```

## 评价和改进：

​		实现了基础的倒排索引和and or not 布尔查询，支持任意长度的关键词组合以及比较自然的以空格代替 and。查询的复杂度仍保持线性。

​		一上来就用set存储，导致后面没法做关于词频的研究。下个实验可以改进这个地方。

#### 留给后来看的注释和注意事项：

- retrieve()负责处理预处理好的Query（列表），分析具体怎么做，然后传给rtv()，后者真正做Bool Retrive操作。
- retrieve()里的endbit是用来判断最后一个词是不是还要做查询（区分 ... A B 和 ... A and B）firstbit用来判断第一个Term，jump用来判断下一个词还需不需要再判断。
- rtv()里每个空集判断都不能删，删掉后面合并没法做了
- 记得对于 tweets 与 queries 要使用相同的预处理