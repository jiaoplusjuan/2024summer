### Appearance-Driven Automatic 3D Model Simplification
#### Introduction
1. 方法特征：
- Geometric simplification（几何简化）
- Joint shape-appearance simplification.
- Simplification of aggregate geometry（聚合几何体）
- Animation
- Conversion between rendering systems
- Conversion between shape representations.
#### Previous work
1. Mesh decimation：误差度量通常基于几何图形，目标函数是基于视觉差异，通过可微渲染来利用基于层次的优化
2. appearance prefiltering：过滤正态分布函数（NDF）
3. Appearance and geometry capture
4. Scene acquisition with neural networks:NeRF将场景表现为神经辐射场
5. Differentiable rendering
#### Method
1. 同时优化shape和，material parameters
2. latent representation:三角形网格和一组纹理
3. 通过可微渲染管线渲染潜在空间、
4. 在结果图像和由参考渲染器生成的目标图像之间计算图像空间损失，反向传播优化顶点位置和纹理内容
5. 用随机相机和单个随机点光迭代大量的图像
6. 其中${\theta}$为潜在表示的参数，c为camera，l为light
$
 \text{argmin}_{\theta} \quad E_{c,l} \left[ L (I_{\theta}(c,l),I_{\text{ref}}(c,l) \right) ] 
$
7. ref渲染器看作黑盒，不需要可维，甚至不需要同一框架
8. 目标函数中包含了一个拉普拉斯正则化器
#### Applications
##### Joint Shape-Appearance Simplification
1. Normal map baking：从一个具有3k个三角形的球体开始，优化形状和一个切线空间正线映射
2. Displacement map baking
3. Simplification with complex materials： 使用了an image domain loss robust to large floating-point values
4. Automatic cleanup