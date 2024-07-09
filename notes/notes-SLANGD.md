##
### 3个特征
执行模型（不进行跟踪）,中间表示，程序优化
### SLANG.D
- 着色器专门化和动态调度与泛型和接口的统一
### SLANG.D LANGUAGE DESIGN
#### 可微架构
- 现有区别方法:
1. var.req_- grad=True
2. 静态编译系统（double可微分，int不可）
- 优化：
1. 将数据类型与语义类型解耦：SLANG.D定义IDifferentiable接口。
2. 四个元素：Differential,dzero(),dadd(), dmul()
3. 自动类型合成
#### 高阶函数：AD运算符
- 如何调用导数计算
1. 调用变量反向传播
2. 调用高阶函数生成计算反向导数的新函数
3. SLANG.D：静态表示为高阶函数运算，使用fwd_- diff (f)和bwd_diff (f)分别调用f（）的正向导数或反向导数
- SLANG.D
1. 泛型对类型
```
struct DifferentialPair<T : IDifferentiable> :
IDifferentiable {
property T p;
property T.Differential d;
// Implementation of IDifferentiable requirements...
}
```
其中属性d存储属性p的导数
2. 导数函数签名
正向函数fwd_-diff(f),：
```
func(DifferentialPair<T>, U) ->DifferentialPair<R>
```
反向函数bwd_diff(f)：
```
func(inout DifferentialPair<T>, U, R.Differential) -> void
```
可微输入输出都与微分对配对。
3. 标记可微分方法
使用[Differentiable]属性标注函数
no_diff关键字
4. 通过接口方法可微
编译器添加额外的接口方法来表示[Differentiable]方法的前向和向后导数。
5. 高阶应用
$Differential.Differential=Differential$
确保IDifferentiable的实现可以终止。
#### 用户定义的派生数
1. 强制执行全局内存访问指令在默认情况下不可微
2. 简单地用提供的自定义函数替换调用
#### Checkpointing Primitives
1. 使用轻量级启发式：确定一个值是否会缓慢地重新计算
2. 对函数使用 [PreferCheckpoint] and [PreferRecompute]，对循环使用[ForceUnroll]或分割为两个嵌套：指定首选项。
3. SLANG.D：within-kernel;Pytorch
:across-kernel
### SLANG.D的编译器
#### 处理
1. 删除地址别名：两个可变参数永远不能有别名
eg:副本更新：$A[i]=x$.$A1 = update A0,i,x$
2. 控制流归一化
### 自动微分
#### 线性化
1. 将所有可微参数转换为微分对类型,从输入操作数的导数传播到原始指令的输出
#### Tranposition
1. 解压缩：将原始结构重新排序到第一个微分指令之前
2. 每个块中转位
3. 控制流反转
### Checkpointing
#### 1.分类
1. 将所有原始指令分类为cache和 recompute两类，使用贪婪策略计算
#### 2.缓存
1. 默认情况下放在线程本地内存上
2. 在gpu上慢，着色语言不允许动态分配
#### 3.重计算
1. 标记为重新计算的指令被克隆到它们在差异块中的适当位置。对指令的所有操作数重复克隆过程，直到差分块中的所有依赖项都可用为止。
#### 4.提取
### 高阶微分
1. 通过重复应用AD传递，直到耗尽fwd_diff或bwd_diff操作
### 案例分析
#### 例子
- Falcor实时渲染器
1. 随着材料实例数量的增加，Falcor的性能基本保持不变
- Warped-Area Reparameterized Path Tracer
- 更换CUDA内核
### 问题
- Across-kernel differentiation.
- Sub-optimal handling of local arrays