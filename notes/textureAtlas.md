##
### Intro
- 传统的纹理数据减少方法：手动识别重复的纹理内容——依赖手工
- 提出全自动管道：压缩重复内容减少纹理大小
- 三个过程：repeated salient（重复显著性） region removal, background，compression, and new texture generation.
- 参数𝜖来平衡压缩比和视觉质量
### related work
1. Image and Texture Compression
- 数字图像压缩：利用图像中相邻样本，神经网络，熵编码技术的新型超压缩技术
2.  Feature Extraction and Matching
- Segment Anything Model (SAM)
- KLT算法：局部优化相对仿射变换和最大化相似度分数
### method
1. pipeline:
![](textureAtlas1.png)
输入：texture和UVmap，(c)的代表性区域来检测和去除重复的显著特征区域，删除具有重复内容(d).的三角形来生成一个新的UV贴图，切割和重新包装(e)创建了一个新的UV图谱
2. input：3D model with provided UV atlas and texture image； output a new model withupdated mesh, UV, and texture，尺寸尽可能小，输出模型在视觉上尽可能一样
#### Repetitive Salient Feature Removal
1. Texture Dilation（扩张）：
- 为了处理跨UV图边界的纹理内容不连续，采用traveler’s map method
- 识别出所有对应于切割的UV边界边
- 沿着每个UV顶点𝑣的法线方向 𝑛扩展每个UV顶点，移动距离$d_{D}$
- 对于每个边界边𝑒（𝑣𝑖,𝑣𝑗），我们可以构造一个由四个顶点组成的四边形区域，记为𝑀（𝑣𝑖，𝑣𝑗，𝑣𝑗+𝑛𝑗𝑑𝐷，𝑣𝑖+𝑛𝑖𝑑𝐷）
- 复制其他UV补丁的纹理
- 假设另一个补丁上对应的边为𝑒‘，𝑒和𝑒’可以通过仿射变换𝑇𝑒→𝑒‘对齐
![](textureAtlas2.png)
2. Feature Extraction
- 采用SAM模型，输出一组表示为M𝑓的纹理区域，每个区域𝑀𝑖∈M𝑓都配备有一个分割掩模
- 𝑀𝑖∈M𝑓无效：
|𝑀𝑖|/|𝑀|∈[<u>𝜖</u>，𝜖]，其中||表示像素数量
或者𝜎（𝑀𝑖）≥𝜖𝜎，𝜎（𝑀𝑖）表示像素颜色标准色调变化
3. Repetitive Feature Detection.
- 给定M𝑓，我们将继续匹配所有具有重复内容的区域。
- 遍历每一对𝑀𝑖，𝑀𝑗∈M𝑓
- 

在Markdown中，你可以使用LaTeX语法来打印数学公式。但是请注意，标准的Markdown不支持LaTeX，你需要在一个支持LaTeX渲染的Markdown编辑器中使用它，例如GitHub或一些在线Markdown编辑器。

以下是你提供的公式的Markdown LaTeX表示：

markdown
$$
\arg\min_{T_{ij}} \ O(M_i, T_{ij}) = \sum_{x \in M_i} \| M[\sigma x] - M[T_{ij}x] \|^2 / (𝜎（𝑀𝑖）^a + λ)
$$
其中$M_{j}$并不直参与优化过程，但提供$T_{ij}$初始化，在$𝑂（𝑀_{𝑖}，𝑇_{𝑖𝑗}）≤𝜖𝑜|𝑀_{𝑖}|$时，$M_{i}$成功注册到$M_{j}$
4. Local Re-meshing
- M𝑓被写成不相交并集$M_f = \bigcup_{i \in I} M_i^f$，其中$M_i^f$是具有成功匹配的相同重复内容的区域子集
- 与其他区域的配准误差最小的$M_i^*$∈$M_i^f$
- 将$M_i^*$放大𝑑𝑀像素，以确保显著内容完全包含在掩模中
#### Background Compression
- 删除包含重复背景颜色的三角形来压缩背景
- step1：聚类：满足以下条件的三角形可认为他们有相同颜色：
$ \sigma(H) < 100\epsilon \land \sigma(S) < 0.5\epsilon \land \sigma(V) < 3\epsilon $
其中$\sigma$是颜色通道𝐻∈[0,360)，𝑆∈[0,1]，𝑉∈[0,1]，$\epsilon$是唯一的用户可控参数
- step2：压缩：对于每一簇三角形，所有的三角形称为一个具有代表性的𝑀𝑖∗∈M_{𝑖𝑏}
#### New Texture Generation
- 生成一个新的紫外线图谱来消除这些空洞，然后烘焙一个新的纹理图像
- step1:UV packing:采用了标准的紫外图谱生成管道，其中包括切割、参数化和包装
- step2:Texture baking:使用UV图谱烘焙一个新的纹理图像,使用基于微分法的优化框架进行全局纹理烘焙
