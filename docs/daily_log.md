# Daily Log

## Week 1 （07/08-07/14）

### 日期: 2024-07-08

#### 今日工作内容
- [ ] 任务1描述：描述今天完成的工作任务。
  - 如果需要 简述细节
- [ ] 任务2描述：描述今天完成的工作任务。
  - 如果需要 简述细节

#### 遇到的问题
- 问题1描述：描述今天遇到的问题及其影响。
  - 如果需要 简述解决方案

#### 明日计划
- Todo任务：描述明天计划进行的工作任务。

#### 导师的工作内容
- [x] git环境创建:<a href="https://git.woa.com/dreamanlan/spark_mf2024summer.git">当前实践git链接</a> 
- [ ] 约定每日同步会议的时间：尽量避开每日晨会及每周组会的时间，线上召开。
- [ ] 确认第一周的任务

#### 备注
- 其他需要记录的事项或说明。


### 日期: 2024-07-09

#### 今日工作内容
- [ ] 阅读bangaru2023slangd论文，完善笔记
- [ ] 根据SLANG.D官网学习SLANG.D，跑通部分代码
- [ ] 阅读Extracting Triangular 3D Models, Materials, and Lighting From Images，完善部分笔记。
- [ ] 尝试配置tinycudann相关环境以跑通上述论文代码。
#### 遇到的问题
- 配置tinycudann环境出现问题

#### 明日计划
- 配置tinycudann
- 跑通Extracting论文代码
- 定下后续研究方向

#### 导师的工作内容
- [x] git环境创建:<a href="https://git.woa.com/dreamanlan/spark_mf2024summer.git">当前实践git链接</a> 
- [ ] 约定每日同步会议的时间：尽量避开每日晨会及每周组会的时间，线上召开。
- [ ] 确认第一周的任务

#### 备注
- 其他需要记录的事项或说明。

### 日期: 2024-07-10

#### 今日工作内容
- [ ] 阅读SoftRas论文，完善笔记
- [ ] 配置SoftRas代码环境，跑通代码
- [ ] 配置pytorch3d环境
- [ ] 查找gltf仓库
#### 遇到的问题
- SoftRas数据集对内存要求高
  - 减少数据集跑通代码，由于iteration数量减少，最终效果并未很好，明天再进行尝试。

#### 明日计划
- 再次尝试SoftRas
- 阅读gltf相关内容，尝试gltf的渲染器
- 查找已有的gltf渲染内容

### 日期: 2024-07-11

#### 今日工作内容
- [ ] 阅读gltf官方文档
- [ ] 阅读moderngl官方文档
- [ ] 跑通moderngl例子
- [ ] 尝试moderngl渲染gltf文件
#### 遇到的问题
- gltf文件处理indices时出现问题
- moderngl的纹理处理不太理解

#### 明日计划
- 解决昨天的bug
- 完善三角形的渲染
- 尝试法线贴图任务

### 日期: 2024-07-12

#### 今日工作内容
- [ ] 阅读gltf中material内容
- [ ] 完成昨日问题，处理了三角形的渲染工作
- [ ] 法线贴图任务完成了单张纹理的贴图
- [ ] 初步阅读UV optimization论文
#### 遇到的问题
- 未弄明白多张纹理的使用方法

#### 明日计划
- 完成<a href="https://learnopengl.com/Advanced-Lighting/Normal-Mapping"></a> 的阅读
- 完成多张纹理的贴图任务
- 完善UV optimization论文阅读


### 日期: 2024-07-15

#### 今日工作内容
- [ ] 阅读UV optimization论文
- [ ] 尝试UV optimization代码
#### 遇到的问题
- 联合UV论文中$L_{diff}$如何理解
- ψ是双射的保证方法
- 联合UV中的参数信息比如$T_{D}$，$T_{l,m}$
- 联合UV代码没跑通
#### 明日计划
- 跑通UV optimization论文代码
- 完善UV optimization论文阅读

### 日期: 2024-07-16

#### 今日工作内容
- [ ] 阅读UV optimization论文
- [ ] 初步阅读textureAtlas论文
- [ ] 复现textureAtlas和UV optimization
#### 遇到的问题
- 复现textureAtlas和UV optimization出现环境问题（文件缺失）
#### 明日计划
- 尝试解决之前的问题：比如nvdiff等环境配置
- 完善textureAtlas论文

### 日期: 2024-07-17

#### 今日工作内容
- [ ] 完善textureAtlas论文
- [ ] 初步阅读Neural 3D Mesh Renderer论文
- [ ] 回顾softras论文
- [ ] 尝试更改softras论文代码：包括encoder和decoder层，有风格迁移思路
#### 遇到的问题
- 无
#### 明日计划
- 阅读Neural 3D Mesh Renderer论文
- 阅读NMR的风格迁移工作寻找思路
- 阅读nvdiffmodeling论文，跑通代码

### 日期: 2024-07-18

#### 今日工作内容
- [ ] 阅读nvdiffrast论文
- [ ] 阅读nvdiffmodeling论文
- [ ] 配置Windows下conda环境
#### 遇到的问题
- linux下运行nvdiffmodeling论文代码时出现问题
#### 明日计划
- 尝试在windowsa下运行nvdiffmodeling论文代码
- 回顾nvdiffrast/nvdiffmodeling论文

### 日期: 2024-07-19

#### 今日工作内容
- [ ] 配置jittor/stylegaussian环境
- [ ] 复习渲染管线
#### 遇到的问题
- 环境配置失败
#### 明日计划
- 继续复习渲染管线

### 日期: 2024-07-22

#### 今日工作内容
- [ ] 在windows上跑通nvdiffrast和nvdiffmodeling
- [ ] 复习渲染管线
#### 遇到的问题
- 无
#### 明日计划
- 继续复习渲染管线
- 仔细阅读nvdiffmodeling论文

### 日期: 2024-07-23

#### 今日工作内容
- [ ] 读nvdiffrast和nvdiffmodeling代码
- [ ] 复习渲染管线
- [ ] 查找cuda编程相关资料
#### 遇到的问题
- 了解cuda学习路径
#### 明日计划
- 学习cuda编程
- 读nvdiffrast中的cuda内容

### 日期: 2024-07-24

#### 今日工作内容
- [ ] 学习cuda编程
- [ ] 读nvdiffrast中的cuda内容
#### 遇到的问题
- cuda编程入门
#### 明日计划
- 继续学习cuda编程
- 读stylegaussian，cuda代码

### 日期: 2024-07-25

#### 今日工作内容
- [ ] 配置stylegaussian环境
- [ ] 读render代码
#### 遇到的问题
- stylegaussian环境失败
#### 明日计划
- 继续stylegaussian环境
- 读stylegaussian，cuda代码

### 日期: 2024-07-26

#### 今日工作内容
- [ ] 配置windows的cuda环境
- [ ] 找到text2mesh和3d-style diffusion
#### 遇到的问题
- windows的cuda环境配置失败
#### 明日计划
- 继续配置windows的cuda环境
- 读text2mesh和3d-style diffusion相关内容

### 日期: 2024-07-29

#### 今日工作内容
- [ ] 完成cuda环境配置
- [ ] 配置text2mesh和3d-style diffusion论文环境
#### 遇到的问题
- 3d-style diffusion论文环境存在cache问题
- 论文细节
#### 明日计划
- 阅读论文，跑通代码

### 日期: 2024-07-30

#### 今日工作内容
- [ ] 阅读text2mesh和3d-style diffusion论文
- [ ] 尝试配置3d-style diffusion论文环境
- [ ] 查找TANGO论文，跑通代码
#### 遇到的问题
- 3d-style diffusion论文环境存在cache问题
- 论文细节
#### 明日计划
- 阅读论文细节，尝试创新点

### 日期: 2024-07-31

#### 今日工作内容
- [ ] 阅读text2mesh,TANGO和3d-style diffusion论文
- [ ] 跑通TANGO代码
- [ ] 查找2024新的text-to-mesh论文
#### 遇到的问题
- 无
#### 明日计划
- 接着查找2024新的text-to-mesh论文

### 日期: 2024-08-01

#### 今日工作内容
- [ ] 阅读dreamfussion和3d-style diffusion论文
- [ ] 初步阅读styke-gaussian论文
#### 遇到的问题
- 无
#### 明日计划
- 阅读新论文，核对思路与改进方案
<!--
每天工作内容可以拆分的细一些
-->

<!--
### 日期：YYYY-MM-DD

#### 今日工作内容
- [ ] 任务1描述：描述今天完成的工作任务。
  - 如果需要 简述细节
- [ ] 任务2描述：描述今天完成的工作任务。
  - 如果需要 简述细节

#### 遇到的问题
- 问题1描述：描述今天遇到的问题及其影响。
  - 如果需要 简述解决方案


#### 明日计划
- Todo任务：描述明天计划进行的工作任务。

#### 导师的工作内容
- [&#x2714;] 内容1描述：描述今天实践相关的工作或指导内容。
- [&#x2716;] 内容2描述：描述今天实践相关的工作或指导任务。

#### 备注
- 其他需要记录的事项或说明。
-->

