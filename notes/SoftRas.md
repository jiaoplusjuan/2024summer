##
### Intro
1. 反转渲染器：从二维图像中获取三维信息
2. 基本离散化步骤：rasterizer(图形->像素)，阻止可微的渲染过程。传统渲染过程的不可微，组织梯度流入网格顶点
3. 作用：使用可微函数渲染彩色网格，反向传播信息网格顶点及其属性
4. 方法：将渲染视为聚合函数，提出可微的渲染框架
![](SoftRas-1.png)
5. 将渲染视作一个“soft”概率过程：所有三角形对每个渲染像素都有概率贡献，建模为屏幕空间的概率映射：基于相对深度和概率
6. 可以在没有三位监督下实现图像到网络的重建。
7. 从输入图像中提取有代表性的颜色，把颜色回归作为分类问题。
### Related work
1. Differentiable Rendering:用于特殊目的
2. Image-based 3D Reasoning：中间的2.5D
### Soft Rasterizer
#### 渲染管线
1. 定义环境设置的外部变量：摄像机P和照明条件L；内在属性：三角形网格M，每个顶点的外观（材料，颜色）
2. 相机p转换输入几何M，可以得到网格法线N、图像空间坐标U和视觉相关深度Z
3. 通过照明和材料模型，计算给定A、N、L的颜色C
![](SoftRas-2.png)
4. 把rasterization看作像素和三角形之间的相对位置决定的二进制掩码，z-buffering基于三角形的相对深度合并栅格化结果F。
5. 概率映射$D_{j}$，建模像素停留在特定三角形内的概率，聚合函数$A()$，融合颜色映射和三角形间的相对深度
#### Probability Map Computation
1. $$[ D_{j}^i = \text{sigmoid}(\delta_{j}^i \cdot d^2(i, j) / \sigma) ]$$
- 计算三角形$f_{j}$的影响映射$D_{j}$
- $D_{j}$和像素$p_{i}$
- $\sigma$ 正标量，控制概率分布密度
- $\delta_{j}^i$，符号指示器，$p_{i}$是否属于$f_{j}$
- d(i，j)是从$p_{i}$到$f_{j}$的边最近的距离
- sigmoid归一化输出
- 较小的σ导致更尖锐的概率分布，而较大的σ倾向于模糊结果
#### Aggregate Function
1. 使用重心坐标插值顶点颜色，在图像平面上的像素$f_{i}$处定义其颜色映射$C_{j}$
2. 用聚合函数合并颜色映射：
$$I^i = [AS \left(  C_j \right) = \sum_{j} w_{j}^i C_{j}^i + w_{b}^i C_{b}^i ]$$
- $C_{b}$：背景颜色。
- $ P_j w_{j}^i + w_{b}^i = 1 $
- $$ w_{j}^i = \frac{D_{j}^i \exp(z_{j}^i / \gamma)}{\sum_{k} D_{k}^i \exp(z_{k}^i / \gamma) + \exp(\epsilon / \gamma)} $$，其中$z_{j}^i$表示$f_{i}$上三维点的归一化逆深度
- w与D和z有关，赋予更大z和更近三角形更高权重。w对z轴平移鲁棒性
3. 
$[ I_s = A O \left(  D_j \right) = 1 - \prod_{j} (1 - D_{j}^i) ]$
#### Compare
1. 梯度流到不可见的三角形和所有三角形的z坐标上
2. 没有只能接受周围像素梯度的问题
### Image-based 3D Reasoning
#### Single-view Mesh Reconstruction
1. 结构：
![](SoftRas-3.png)
- 生成三角形网格M及其相应的颜色C，然后将其输入软光栅化器
- 损失函数：轮廓损失Ls，颜色损失Lc和几何损失Lg（正规化），三者加权和。
2. 颜色重构
- 将颜色重建作为一个分类问题，学习为每个采样点重用输入图像中的像素颜色
- 使用调色板为网格着色：采样网络和选择网络
#### Image-based Shape Fitting
1. $[ \text{argmin}_{\rho, \theta, t} \left\| R(M(\rho, \theta, t)) - I_t \right\|^2 ]$
- R:从网格M生成渲染图象I的渲染函数，由其姿态θ、平移t和非刚性变形参数ρ参数化
