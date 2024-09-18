import math
import os
import sys
import base64
import moderngl
import pygame
import glm
from pygltflib import GLTF2
import numpy as np
from PIL import Image
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'

pygame.init()
pygame.display.set_mode((800, 800), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)
def get_component_type_info(component_type):
    # 使用字典映射来模拟switch结构
    component_type_map = {
        5120: "GL_BYTE: Signed 8-bit integer",
        5121: "GL_UNSIGNED_BYTE: Unsigned 8-bit integer",
        5122: "GL_SHORT: Signed 16-bit integer",
        5123: "GL_UNSIGNED_SHORT: Unsigned 16-bit integer",
        5125: "GL_INT: Signed 32-bit integer",
        5126: "GL_UNSIGNED_INT: Unsigned 32-bit integer",
        5124: "GL_FLOAT: 32-bit floating-point"
    }
    return component_type_map.get(component_type, "Unknown component type")

def get_type_info(type_value):
    # 使用if-elif-else结构来模拟switch结构
    if type_value == "SCALAR":
        return "Single value, such as a texture coordinate index."
    elif type_value == "VEC2":
        return "2-component vector."
    elif type_value == "VEC3":
        return "3-component vector, such as vertex positions or normals."
    elif type_value == "VEC4":
        return "4-component vector, such as homogeneous coordinates or RGBA color."
    elif type_value == "MAT2":
        return "2x2 matrix."
    elif type_value == "MAT3":
        return "3x3 matrix."
    elif type_value == "MAT4":
        return "4x4 matrix."
    else:
        return "Unknown type"

component_type_mapping = {
    5120: ('b', 'int8'),  # GL_BYTE -> Python: int, NumPy: int8
    5121: ('B', 'uint8'),  # GL_UNSIGNED_BYTE -> Python: int, NumPy: uint8
    5122: ('h', 'int16'),  # GL_SHORT -> Python: int, NumPy: int16
    5123: ('H', 'uint16'), # GL_UNSIGNED_SHORT -> Python: int, NumPy: uint16
    5125: ('i', 'int32'),  # GL_INT -> Python: int, NumPy: int32
    5126: ('I', 'uint32'), # GL_UNSIGNED_INT -> Python: int, NumPy: uint32
    5124: ('f', 'float32'),# GL_FLOAT -> Python: float, NumPy: float32
}

class Object:
    def __init__(self, material,position_data, indices_data,normal_data,tangent_data,texcoord_data):
        self.material = material
        self.position_data = position_data
        self.indices_data = indices_data
        self.normal_data = normal_data
        self.tangent_data = tangent_data
        self.texcoord_data = texcoord_data

class Data:
    def __init__(self, data, count, data_type, component_type):
        self.data = data
        self.count = count
        self.data_type = data_type # vec3
        self.component_type = component_type # 5123
        
class Texture:
    def __init__(self, sampler,source):
        self.source = source
        self.ctx = moderngl.create_context()
        img = Image.open(source.uri).convert('RGBA')
        self.texture = self.ctx.texture(img.size, 4, img.tobytes())
        self.sampler = sampler
        
class Material:
    def __init__(self,double_sided, normalTexture, occlusionTexture, baseColorTexture, metallicRoughnessTexture):
        # self.material = material
        self.double_sided = double_sided
        self.normalTexture = normalTexture
        self.occlusionTexture = occlusionTexture
        self.baseColorTexture = baseColorTexture
        self.metallicRoughnessTexture = metallicRoughnessTexture
        
def handle_accessor(gltf:GLTF2, primitive, type):
    # if primitive.attributes.get(type) == None:
    #     return None
    if type == "position":
        if primitive.attributes.POSITION == None:
            return None
        accessor = gltf.accessors[primitive.attributes.POSITION]
        
    elif type == "indices":
        if primitive.indices == None:
            return None
        accessor = gltf.accessors[primitive.indices]
        
    elif type == "tangent":
        if primitive.attributes.TANGENT == None:
            return None
        accessor = gltf.accessors[primitive.attributes.TANGENT]
        
    elif type == "texcoord":
        if primitive.attributes.TEXCOORD_0 == None:
            return None
        accessor = gltf.accessors[primitive.attributes.TEXCOORD_0]
        
    elif type == "normal":
        if primitive.attributes.NORMAL == None:
            return None
        accessor = gltf.accessors[primitive.attributes.NORMAL]
        
    bufferView = gltf.bufferViews[accessor.bufferView]
    component_type =  accessor.componentType
    data_type =  accessor.type
    count =  accessor.count
    byte_offset = accessor.byteOffset + bufferView.byteOffset
    byte_length = bufferView.byteLength
    target = bufferView.target
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    data = data[byte_offset:byte_offset + byte_length]
    assert isinstance(data, bytes)
    # print(data)
    return Data(data, count, data_type, component_type)

def handle_material(gltf, primitive):
    if primitive.material == None:
        return None
    material = gltf.materials[primitive.material]
    double_sided = material.doubleSided
    normalTexture = Texture(gltf.samplers[gltf.textures[material.normalTexture.index].sampler], gltf.images[gltf.textures[material.normalTexture.index].source])
    occlusionTexture = Texture(gltf.samplers[gltf.textures[material.occlusionTexture.index].sampler], gltf.images[gltf.textures[material.occlusionTexture.index].source])
    baseColorTexture = Texture(gltf.samplers[gltf.textures[material.pbrMetallicRoughness.baseColorTexture.index].sampler],gltf.images[gltf.textures[material.pbrMetallicRoughness.baseColorTexture.index].source])
    metallicRoughnessTexture = Texture(gltf.samplers[gltf.textures[material.pbrMetallicRoughness.metallicRoughnessTexture.index].sampler],gltf.images[gltf.textures[material.pbrMetallicRoughness.metallicRoughnessTexture.index].source])
    return Material(double_sided, normalTexture, occlusionTexture, baseColorTexture, metallicRoughnessTexture)

def hanlde_gltf(filename):
    gltf = GLTF2().load(filename)
    objects =[]
    for node in gltf.nodes:
        # print(node)
        if node.mesh is not None:
            mesh = gltf.meshes[node.mesh]
            for primitive in mesh.primitives:
                position_data = handle_accessor(gltf, primitive, "position")
                indices_data = handle_accessor(gltf, primitive, "indices")
                normal_data = handle_accessor(gltf, primitive, "normal")
                tangent_data = handle_accessor(gltf, primitive, "tangent")
                texcoord_data = handle_accessor(gltf, primitive, "texcoord")
                material = handle_material(gltf, primitive)
                objects.append(Object(material=material, position_data=position_data, indices_data=indices_data, normal_data=normal_data, tangent_data=tangent_data, texcoord_data=texcoord_data))
    return objects
    
class Scene:
    def __init__(self):
        self.ctx = moderngl.get_context()

        self.program = self.ctx.program(
             vertex_shader='''
                #version 330 core

                uniform mat4 camera;
                uniform vec3 position;
                uniform float scale;
                
                layout (location = 0) in vec3 in_vertex;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in vec2 in_uv;    //输入变量

                out vec3 v_vertex;
                out vec3 v_normal;
                out vec2 v_uv;  //输出变量

                void main() {
                    v_vertex = position + in_vertex * scale;
                    v_normal = in_normal;
                    v_uv = in_uv;

                    gl_Position = camera * vec4(v_vertex, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330 core

                uniform sampler2D Texture;
                uniform bool use_texture;
                uniform vec3 color;

                in vec3 v_vertex;
                in vec3 v_normal;
                in vec2 v_uv;

                layout (location = 0) out vec4 out_color;

                void main() {
                    out_color = vec4(color, 1.0);
                    if (use_texture) {
                        out_color *= texture(Texture, v_uv);
                    }
                }
            ''',
        )
        self.objects = hanlde_gltf(filename="/home/tony/workspace/glTF-Sample-Models/gltf-project/normal/glTF/NormalTangentMirrorTest.gltf")

    def camera_matrix(self): # 设置相机
        now = pygame.time.get_ticks() / 1000.0
        eye = (math.cos(now), math.sin(now), 0.5)
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        return proj * look

    def render(self):
        camera = self.camera_matrix()
        self.ctx.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)
        self.program['camera'].write(camera)
        self.program['scale'] = 0.3
        self.program['position'] = (0.0, 0.0, 0.0)
        self.program['color'] = (1.0, 1.0, 1.0)
        for object in self.objects:
            self.vbo = self.ctx.buffer(object.position_data.data)  # 使用提取的顶点数据创建buffer
            self.tex = self.ctx.buffer(object.texcoord_data.data) 
            self.nor = self.ctx.buffer(object.normal_data.data)
            self.ibo = self.ctx.buffer(object.indices_data.data)
            python_type = component_type_mapping[object.indices_data.component_type][0]  # 'I'
            arr = np.frombuffer(object.indices_data.data, python_type)
            arr=arr.astype('u4')
            self.ibo = self.ctx.buffer(arr)
            vao_content = [
                self.vbo.bind('in_vertex', layout='3f'),
                # self.nor.bind('in_normal', layout='3f'),
                self.tex.bind("in_uv", layout='2f')
            ]
            self.vao = self.ctx.vertex_array(self.program, vao_content, self.ibo)
            self.normalTexture = object.material.normalTexture.texture
            self.baseColorTexture = object.material.baseColorTexture.texture
            self.occlusionTexture = object.material.occlusionTexture.texture
            self.metallicRoughnessTexture = object.material.metallicRoughnessTexture.texture
            self.vao.program['use_texture'] = True
            # self.vao.program["Texture"]= self.normalTexture # 设置第一个纹理对象
            # self.metallicRoughnessTexture.use()
            # self.normalTexture.use()
            self.baseColorTexture.use()
            
            # self.occlusionTexture.use()
            # self.program['use_texture'] = True
            # self.program['texture_selector'] = 0
            # object.material.normalTexture.use()  # 绑定到纹理单元0
            # object.material.occlusionTexture.use()  # 绑定到纹理单元1
            # object.material.baseColorTexture.use()  # 绑定到纹理单元2
            # object.material.metallicRoughnessTexture.use()  # 绑定到纹理单元3

            # # 设置着色器程序中的uniform变量，以引用这些纹理
            # self.program['u_normal_texture'].value = 0
            # self.program['u_occlusion_texture'].value = 1
            # self.program['u_base_color_texture'].value = 2
            # self.program['u_metallic_roughness_texture'].value = 3
            self.vao.render()
            

scene = Scene()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.render()

    pygame.display.flip()
