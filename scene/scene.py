import glm
import moderngl
import moderngl_window as mglw

from . import Camera, KeyboardCamera
from . import Object
from wavefront import Material, Wavefront

class Scene:
    def __init__(self, path: str,
            camera: Camera = KeyboardCamera(), **kwargs):
        self.object_data = Wavefront(path)
        self.camera: Camera = camera
        self.objects: dict[str, Object] = dict()
        self.materials: dict[str, Material] = dict()
        self.light_color: glm.vec3 = glm.vec3(1)
        self.light_pos: glm.vec3 = self.camera.eye
        self.frame_texture: moderngl.Texture = self.ctx.texture(self.wnd.size, 4)
        self.depth_texture: moderngl.Texture = self.ctx.depth_texture(self.wnd.size)
        self.fbo: moderngl.Framebuffer = self.ctx.framebuffer(
            [self.frame_texture], self.depth_texture,
        )
        self.wnd.mouse_exclusivity = self.camera.enabled
        self.parse_data()

    @property
    def ctx(self):
        return mglw.ctx()

    @property
    def wnd(self):
        return mglw.window()

    def parse_data(self):
        self.materials = self.object_data.materials
        for n, object in enumerate(self.object_data.objects.values()):
            if object.material_name not in self.materials:
                object.material_name = "Material"
            texture_path = self.materials[object.material_name].texture_path
            self.objects[object.name] = Object(n, object, texture_path)

    def draw(self, time, frametime):
        self.ctx.enable(self.ctx.DEPTH_TEST | self.ctx.CULL_FACE)
        self.fbo.clear()
        self.fbo.use()
        for object in self.objects.values():
            for attr, value in zip(
                ('model', 'view', 'proj', 'light_color', 'light_pos', 'view_pos'),
                (object.model, self.camera.view, self.camera.proj,
                 self.light_color, self.light_pos, self.camera.eye)
            ):
                object.vao.program.get(attr, None).write(value)
            for uniform in ('ambient', 'diffuse', 'specular',
                            'shininess', 'transparency', 'ambient_strength'):
                value = uniform 
                if uniform in ('ambient', 'diffuse', 'specular'):
                    uniform += '_value'
                object.program.get(uniform, None).value = getattr(
                    self.materials[object.data.material_name], value
                )
            object.vao.render()
        self.ctx.copy_framebuffer(self.wnd.fbo, self.fbo)
        self.camera.update(frametime)
        self.light_pos = self.camera.eye

    def object_material(self, object_name: str) -> str:
        return self.objects[object_name].data.material_name
