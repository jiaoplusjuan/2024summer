import math
import os
import sys
import base64
import moderngl
import pygame
import glm
from pygltflib import GLTF2
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

component_types_size = {
    5120: 1,  # GL_BYTE
    5121: 1,  # GL_UNSIGNED_BYTE
    5122: 2,  # GL_SHORT
    5123: 2,  # GL_UNSIGNED_SHORT
    5125: 4,  # GL_INT
    5126: 4,  # GL_UNSIGNED_INT
    5124: 4,  # GL_FLOAT
}

def handle_accessor(gltf:GLTF2, primitive, type):
    if type == "position":
        accessor = gltf.accessors[primitive.attributes.POSITION]
    elif type == "indices":
        accessor = gltf.accessors[primitive.indices]
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
    return data, count
    
def hanlde_gltf(filename):
    gltf = GLTF2().load(filename)
    for node in gltf.nodes:
        # print(node)
        if node.mesh is not None:
            mesh = gltf.meshes[node.mesh]
            for primitive in mesh.primitives:
                position_data, count = handle_accessor(gltf, primitive, "position")
                indices_data, count = handle_accessor(gltf, primitive, "indices")
                return count, position_data, indices_data
    
class Scene:
    def __init__(self):
        self.ctx = moderngl.get_context()

        self.program = self.ctx.program(
            vertex_shader='''
                #version 330 core
                layout (location = 0) in vec3 in_vertex;
                uniform mat4 camera;
                void main() {
                    gl_Position = camera * vec4(in_vertex, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330 core

                layout (location = 0) out vec4 out_color;

                void main() {
                    out_color = vec4(1.0, 1.0, 1.0, 1.0);
                }
            ''',
        )
        count, position_data, indices_data = hanlde_gltf(filename="/home/tony/workspace/glTF-Sample-Models/gltf-project/smalltest/simple-test.gltf")
        self.count = count
        # 创建VBO和IBO
        self.vbo = self.ctx.buffer(position_data)  # 使用提取的顶点数据创建buffer
        self.ibo = self.ctx.buffer(indices_data)
        print(self.ibo)
        self.vao = self.ctx.vertex_array(self.program, [
            (self.vbo, '3f', 'in_vertex'),
        ],index_buffer=self.ibo)
        print(position_data)
        # self.vao.vertices = count

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
        self.vao.render()

scene = Scene()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.render()

    pygame.display.flip()
