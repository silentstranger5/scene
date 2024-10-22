import glm
import moderngl_window as mglw
from math import cos, radians, sin

class Camera:
    def __init__(
        self,
        fovy: float = 45,
        aspect: float = 1,
        near: float = 1,
        far: float = 100,
    ):
        self.eye: glm.vec3 = glm.vec3()
        self.target: glm.vec3 = glm.vec3()
        self.up: glm.vec3 = glm.vec3()
        self.view: glm.mat4 = glm.mat4()
        self.fovy: float = fovy
        self.aspect: float = aspect
        self.near: float = near
        self.far: float = far
        self.proj: glm.mat4 = glm.perspective(
            self.fovy, self.aspect, self.near, self.far,
        )
        self.sensitivity = 0.1
        self.speed = 8
        self.enabled: bool = True
        self.pressed: set = set()

    @property
    def wnd(self):
        return mglw.window()

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            self.pressed.add(key)

            if key == self.wnd.keys.C:
                self.enabled = not self.enabled
                self.wnd.mouse_exclusivity = self.enabled
                self.wnd.cursor = not self.enabled

        if action == self.wnd.keys.ACTION_RELEASE:
            self.pressed.remove(key)

    def mouse_position_event(self, x, y, dx, dy):
        pass

    def mouse_scroll_event(self, x_offset, y_offset):
        if self.enabled:
            self.fovy -= y_offset * self.sensitivity
            if self.fovy < 1:
                self.fovy = 1
            if self.fovy > 45:
                self.fovy = 45

    def update(self, frametime):
        pass

    def move(self, frametime):
        pass


class KeyboardCamera(Camera):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eye: glm.vec3 = glm.vec3(0, 0, 5)
        self.direction: glm.vec3 = glm.vec3(0, 0, -1)
        self.front: glm.vec3 = self.direction
        self.target: glm.vec3 = self.eye + self.direction
        self.up: glm.vec3 = glm.vec3(0, 1, 0)
        self.view: glm.mat4 = glm.lookAt(
            self.eye, self.target, self.up,
        )
        self.yaw: float = -90
        self.pitch: float = 0

    def mouse_position_event(self, x, y, dx, dy):
        if self.enabled:
            self.yaw += dx * self.sensitivity
            self.pitch -= dy * self.sensitivity
            if self.pitch > 89:
                self.pitch = 89
            if self.pitch < -89:
                self.pitch = -89

    def update(self, frametime: float):
        self.direction = glm.normalize(glm.vec3(
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch)),
        ))
        self.right = glm.normalize(glm.cross(self.direction, self.up))
        self.front = glm.normalize(glm.cross(self.up, self.right))
        self.move(frametime)
        self.target = self.eye + self.direction
        self.view = glm.lookAt(
            self.eye, self.target, self.up,
        )
        self.proj = glm.perspective(
            self.fovy, self.aspect, self.near, self.far
        )


    def move(self, frametime: float):
        if not self.enabled:
            return

        keys = self.wnd.keys
        displacement = glm.vec3((0, 0, 0))

        for key, direction in zip(
                'QWEASD',
                (self.up, self.front, -self.up,
                 -self.right, -self.front, self.right)
        ):
            if getattr(keys, key) in self.pressed:
                displacement += direction

        if displacement != glm.vec3((0, 0, 0)):
            displacement = glm.normalize(displacement)

        self.eye += displacement * self.speed * frametime


class OrbitCamera(Camera):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theta: float = glm.radians(90)
        self.radius: float = 5
        self.height: float = 0
        self.eye: glm.vec3 = glm.vec3(
            self.radius * cos(self.theta), self.height,
            self.radius * sin(self.theta)
        )
        self.target: glm.vec3 = glm.vec3(0, self.height, 0)
        self.up: glm.vec3 = glm.vec3(0, 1, 0)

    def update(self, frametime: float):
        self.move(frametime)
        self.view = glm.lookAt(
            self.eye, self.target, self.up,
        )
        self.proj = glm.perspective(
            self.fovy, self.aspect, self.near, self.far
        )

    def move(self, frametime: float):
        if not self.enabled:
            return

        keys = self.wnd.keys

        if keys.Q in self.pressed:
            self.height += self.speed * frametime
        if keys.W in self.pressed:
            self.radius -= self.speed * frametime
        if keys.E in self.pressed:
            self.height -= self.speed * frametime
        if keys.S in self.pressed:
            self.radius += self.speed * frametime
        if keys.A in self.pressed:
            self.theta += self.speed * frametime
        if keys.D in self.pressed:
            self.theta -= self.speed * frametime

        self.eye = glm.vec3(
            self.radius * cos(self.theta), self.height,
            self.radius * sin(self.theta)
        )
        self.target = glm.vec3(0, self.height, 0)
