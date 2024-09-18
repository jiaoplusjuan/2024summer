### simple example
#### simple-test
1. 
```SLANG
uint3 dispatchIdx = cudaThreadIdx() + cudaBlockIdx() * cudaBlockDim()
```
- cudaThreadIdx():这个函数返回当前线程在它的线程块（block）内的索引,返回的是一个三元组(uint3) {x, y, z}。
- cudaBlockIdx():这个函数返回当前线程块在网格（grid）中的索引。同样，它返回的是一个三元组(uint3) {i, j, k}，表示线程块在网格中的位置.
- cudaBlockDim():这个函数返回每个线程块的尺寸。它也是一个三元组(uint3) {x, y, z}，表示线程块在每个维度上的大小
2. 
```SLANG
if (dispatchIdx.x >= input.size(0))
    return;
```
- dispatchIdx与input的维度相对应，判断是否出现越界现象。
3. 
```SLANG
[AutoPyBindCUDA]
[CUDAKernel]
```
- [CUDAKernel]属性是一个装饰器或元数据标签，用于标记那些需要被编译为CUDA内核的函数
- [AutoPyBindCUDA]属性提供了一种自动化的方式，允许开发者直接从Python调用标记为[CUDAKernel]的函数
4. 
```python
import torch
import slangtorch

m = slangtorch.loadModule('square.slang')

A = torch.randn((1024,), dtype=torch.float).cuda()

output = torch.zeros_like(A).cuda()

# Number of threads launched = blockSize * gridSize
m.square(input=A, output=output).launchRaw(blockSize=(32, 1, 1), gridSize=(64, 1, 1))

print(output)
```
- slangtorch.loadModule("square.slang")返回了需要的kernel
- 调用啊用sqaure，绑定参数
- 在Slang-Torch中调用一个CUDA内核：launchRaw()方法用于根据指定的CUDA启动参数（blockSize和gridSize）在GPU上执行内核
- blockSize定义了每个线程块的尺寸。gridSize定义了网格的尺寸，也就是要启动的线程块的总数。
#### differentiable-test
1. 
- 使用[AutoPyBindCUDA]属性，并且函数需要支持自动微分，可以添加[Differentiable]属性来指示
- 可调用的句柄：square,square.fwd,square.bwd，用于绑定一对张量后计算导数
2. 
```python
# Invoke reverse-mode autodiff by first allocating tensors to hold the gradients
input = torch.tensor((0, 1, 2, 3, 4, 5), dtype=torch.float).cuda()
input_grad = torch.zeros_like(input).cuda()

output = torch.zeros_like(input)
# Pass in all 1s as the output derivative for our example
output_grad = torch.ones_like(output) 

m.square.bwd(
    input=(input, input_grad), output=(output, output_grad)
).launchRaw(
    blockSize=(6, 1, 1), gridSize=(1, 1, 1))
```
- 绑定成对的张量来计算导数
- output_grad已经完成了它的功能，其信息已经被用来更新input_grad，已经consumed
#### Wrapping your kernels as pytorch functions
```python
class MySquareFunc(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        output = torch.zeros_like(input)

        kernel_with_args = m.square(input=input, output=output)
        kernel_with_args.launchRaw(
            blockSize=(32, 32, 1),
            gridSize=((input.shape[0] + 31) // 32, (input.shape[1] + 31) // 32, 1))

        ctx.save_for_backward(input, output)

        return output

    @staticmethod
    def backward(ctx, grad_output):
        (input, output) = ctx.saved_tensors

        input_grad = torch.zeros_like(input)
        
        # Note: When using DiffTensorView, grad_output gets 'consumed' during the reverse-mode.
        # If grad_output may be reused, consider calling grad_output = grad_output.clone()
        #
        kernel_with_args = m.square.bwd(input=(input, input_grad), output=(output, grad_output))
        kernel_with_args.launchRaw(
            blockSize=(32, 32, 1),
            gridSize=((input.shape[0] + 31) // 32, (input.shape[1] + 31) // 32, 1))
        
        return input_grad
```
- 定义自定义 autograd 函数，把Slang kernels作为pytorch-compatible operations
#### Specializing shaders
- 使用 loadModule 加载时特殊化：通过 slangtorch.loadModule 函数加载Slang模块时，可以使用 defines 参数来定义编译时常量
#### Back-propagating Derivatives through Complex Access Patterns
- Eg:
1. 包装张量访问（Wrapping Tensor Access）
2. 修改computeOutputPixel以支持自动微分
3. 定义反向传播内核（Backward Kernel Definition）
4. 定义getInputElement的反向传播逻辑
#### Manually binding kernels
```CUDA
[TorchEntryPoint]
TorchTensor<float> square(TorchTensor<float> input)
{
    var result = TorchTensor<float>.zerosLike(input);
    let blockCount = uint3(1);
    let groupSize = uint3(result.size(0), result.size(1), 1);
    __dispatch_kernel(square_kernel, blockCount, groupSize)(input, result);
    return result;
}
```
- 编写一个带有[TorchEntryPoint]属性的host函数，手动调用内核
- 使用__dispatch_kernel语法来调度square_kernel内核
#### Manual binding for kernel derivatives
```SLANG
[CudaKernel]
void square_bwd_kernel(TensorView<float> input, TensorView<float> grad_out, TensorView<float> grad_propagated)
{
    uint3 globalIdx = cudaBlockIdx() * cudaBlockDim() + cudaThreadIdx();

    if (globalIdx.x >= input.size(0) || globalIdx.y >= input.size(1))
        return;

    DifferentialPair<float> dpInput = diffPair(input[globalIdx.xy]);
    var gradInElem = grad_out[globalIdx.xy];
    bwd_diff(square)(dpInput, gradInElem);
    grad_propagated[globalIdx.xy] = dpInput.d;
}
```
- 使用bwd_diff(square)调用来计算每个张量元素的梯度
- 使用[TorchEntryPoint]属性标记square_bwd函数\
### Writing a 2D triangle rasterizer in Slang
1. ```CUDA
[AutoPyBindCUDA]
[CUDAKernel]
void rasterize(
    TensorView<float> vertices,
    TensorView<float> color,
    TensorView<float3> output)
{
    uint3 dispatch_id = cudaBlockIdx() * cudaBlockDim() + cudaThreadIdx();

    if (dispatch_id.x > output.size(0) || dispatch_id.y > output.size(1))
        return;

    // Load vertices of our triangle.
    // Assume our input tensor is of the form (3, 2) where 3 is the number of vertices
    // and 2 is the number of coordinates per vertex.
    // 
    float2 v1 = float2(vertices[0, 0], vertices[0, 1]);
    float2 v2 = float2(vertices[1, 0], vertices[1, 1]);
    float2 v3 = float2(vertices[2, 0], vertices[2, 1]);
    float3 c = float3(color[0], color[1], color[2]);

    // Convert our 2D thread indices directly into pixel coordinates
    // This way pixel at location, say (9, 20) covers the real-number space 
    // between (9.0, 20.0) to (10.0, 21.0)
    // 
    float2 pixel_coord = dispatch_id.xy;

    // Use white as the default background color.
    float3 background_color = float3(1.0, 1.0, 1.0);

    // Center of the pixel will be offset by 50% of the pixel size,
    // which we will assume is 1 unit by 1 unit.
    // 
    float2 sample_coord = pixel_coord + 0.5;

    bool hit = triangle(sample_coord, v1, v2, v3);

    // If we hit the triangle return the provided color, otherwise 0.
    float3 result = hit ? c : background_color;

    // Fill in the corresponding location in the output image.
    output[dispatch_id.xy] = result;
}
```
- Slang's TensorView<T> object\
- rasterize()的并行执行
- [CUDAKernel]和[AutoPyBindCUDA]
```CUDA
struct Camera
{
    // World origin
    float2 o;

    // World scale
    float2 scale;

    // Frame dimensions (i.e. image resolution)
    float2 frameDim;

    // Convert from
    // screen coordinates [(0, 0), (W, H)] to
    // world coordinates [(o.x - scale.x, o.y - scale.y), (o.x + scale.x, o.y + scale.y)]
    //
    float2 screenToWorld(float2 uv)
    {
        float2 xy = uv / frameDim;
        float2 ndc = xy * 2.0f - 1.0f;
        return ndc * scale + o;
    }
};
```
- 基于物体的编程：添加camera组件