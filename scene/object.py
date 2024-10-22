import os
import glm
import moderngl
import moderngl_window as mglw
import wavefront

from array import array
from PIL import Image

vertex_path = os.path.join(os.path.dirname(__file__), 'resources', 'vertex.glsl')
fragment_path = os.path.join(os.path.dirname(__file__), 'resources', 'fragment.glsl')

class Object:
    def __init__(
        self,
        id: int,
        data: wavefront.Object,
        texture_path: str,
        vertex_path: str = vertex_path,
        fragment_path: str = fragment_path,
    ):
        self.id: int = id
        self.data: wavefront.Object = data
        self.texture_path: str = texture_path
        self.vertex_shader: str = open(vertex_path).read()
        self.fragment_shader: str = open(fragment_path).read()
        self.program: moderngl.Program = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_shader,
        )
        self.image = None
        self.texture: moderngl.Texture | None = None
        self.sampler: moderngl.Sampler | None = None
        self.flags: list[bool] = [False] * 4
        self.vao: moderngl.VertexArray = self.build_vertex_array()
        self.model: glm.mat4 = glm.mat4()

    @property
    def ctx(self):
        return mglw.ctx()

    @property
    def wnd(self):
        return mglw.window()

    def build_vertex_array(self):
        record = list()
        inputs = ('in_vert', 'in_tex_pos', 'in_normal', 'in_color')
        buffer = self.ctx.buffer(array('f', self.data.mesh.data).tobytes())
        record.append(buffer)
        for i in range(4):
            if (1 << i) & self.data.mesh.mode:
                record.append(inputs[i])
                self.flags[i] = True
        self.flags[1] = self.texture_path != ""
        if self.flags[1]:
            self.image = Image.open(self.texture_path)
            self.texture = self.ctx.texture(
                self.image.size, components=4, data=self.image.tobytes()
            )
            self.sampler = self.ctx.sampler(texture=self.texture)
            self.sampler.use(location=self.id)
        self.set_values()
        return self.ctx.vertex_array(self.program, *record)

    def set_values(self):
        self.program.get('sampler', None).value = self.id
        attributes = ('has_texture', 'has_normal', 'has_color')
        for i, attribute in enumerate(attributes):
            self.program.get(attribute, None).value = self.flags[i+1]
