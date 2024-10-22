import glm
import moderngl_window as mglw

from math import sin
from scene import OrbitCamera, Scene

class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (512, 512)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We can specify optional camera class
        self.scene = Scene(self.argv.path, OrbitCamera())

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument(
            'path'
        )

    def render(self, time, frame_time):
        # We can apply transformation to all objects
        for object in self.scene.objects.values():
            object.model = glm.translate((0, 0, 1))

        # Or transform some objects specifically by name
        self.scene.objects['Hat'].model = glm.rotate(
            self.scene.objects['Hat'].model, time, (0, 1, 0)
        )

        # We also can set up material properties for certain objects
        self.scene.materials[self.scene.object_material('Hat')].diffuse = [
            sin(time)*0.8, sin(time+2)*0.8, sin(time+4)*0.8,
        ]
        self.scene.draw(time, frame_time)

    # We also have to plug in our key and mouse input to the camera
    def key_event(self, key, action, modifiers):
        self.scene.camera.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
        self.scene.camera.mouse_position_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.scene.camera.mouse_scroll_event(x_offset, y_offset)

mglw.run_window_config(Window)
