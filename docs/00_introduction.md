## 项目技术背景

可微渲染（Differentiable Rendering）是一种允许从渲染结果反向传播梯度的新型渲染技术。

这种技术的核心思想是将渲染过程建模为一个可微分的函数，从而可以利用梯度下降等优化算法进行参数优化。

这使得我们可以利用深度学习技术进行渲染参数的自动调整和优化，从而获得更好的渲染效果。

本项目将探索在游戏领域应用可微渲染技术的方式和前景。

<img src="imgs/background/image1.png" alt="image 1" width="600" >

## 项目描述 

在游戏开发领域，可微渲染技术的应用可以大大提高开发效率和提升游戏体验。以下是一些可行的探索方向:

1. 将可微渲染技术应用于传统游戏美术资产的处理

使用可微渲染技术，开发者能够自动化优化游戏内的材质、网格和其他渲染参数，这将极大地降低了手动调整这些元素的工作量。例如，通过应用这项技术，我们可以在特定的环境和观察条件中生成更优质的LOD资产，从而实现最佳的视觉效果。

2. 将可微渲染技术应用于程序化内容的生成

程序化内容是指使用程序和算法自动生成的内容，比如程序化生成的纹理、地形、建筑等。这种技术可以大大提高内容创建的效率，同时也可以生成出丰富多样、具有无限可能性的内容。将可微渲染应用到程序化内容的生成中，可以实现对内容生成参数的自动优化，从而生成出更满足视觉需求或者游戏规则的内容。此外，可微渲染还可以应用于程序化内容相关的训练和优化。例如，我们可以通过可微渲染模型训练出一个深度学习模型，这个模型可以根据输入的条件自动生成满足这些条件的内容。

3. 可微分着色语言的实现

可微渲染器的实现存在两条技术路线：（1）利用可微分编程语言实现渲染器，使用自动微分的功能完成微分计算，性能和效率方面偏弱；（2）利用传统着色语言实现渲染器，使用手动推到的导数公式完成微分的计算，灵活性方面偏弱。 需要对传统着色语言进行自动微分的扩展，来弥补两种方法之间的差距，进而更好的对大量传统游戏资产使用可微渲染技术。