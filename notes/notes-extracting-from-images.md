##
### Method
#### 概述
1. 目标： triangle meshes, spatially-varying materials (stored in 2D textures) and lighting (a high dynamic range environment probe)。
2. 直接优化目标形状
3. 使用DMnet监督，共同优化形状、材料和照明
4. 在每个优化步骤中，表面网格渲染在可微光栅化器。计算损失函数，反向传播
5. 使用differentiable marching tetrahedrons优化拓扑结构，输出为三角形网格
#### 优化任务
1. 优化参数:SDF值和顶点偏移量表示形状，空间变化的材料和光探针参数
2. 损失函数：$L = L_{image} + L_{mask} + λL_{reg}$:色调映射颜色上的L1范数、Lmask平方L2和正则化器来改善几何形状
#### 假设
不支持反射、折射和半透明，直接照明无阴影。