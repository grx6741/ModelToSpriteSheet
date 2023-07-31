import pygame
import moderngl
import glm
import numpy as np

pygame.init()

class Camera:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx

        self.aspectRatio = self.app.size[0] / self.app.size[1]

        self.pos = glm.vec3(0, 0, 3)
        self.target = glm.vec3(0);
        self.direction = self.pos - self.target
        up = glm.vec3(0, 1, 0)
        self.right = glm.normalize(glm.cross(up, self.direction))
        self.up = glm.cross(self.direction, self.right)

        self.view = glm.lookAt(self.pos, self.target, self.up)
        self.projection = glm.perspective(glm.radians(45), self.aspectRatio, 0.1, 100)

        self.scene = []

    def update(self):
        self.direction = self.pos - self.target
        up = glm.vec3(0, 1, 0)
        self.right = glm.normalize(glm.cross(up, self.direction))
        self.up = glm.cross(self.direction, self.right)
        self.view = glm.lookAt(self.pos, self.target, self.up)

        self.model = glm.rotate(glm.mat4(1), glm.radians(pygame.time.get_ticks() / 10), glm.vec3(1, 0, 0))

    def render(self):
        for obj in self.scene:

            obj.set_uniform_matrix("model", self.model)
            obj.set_uniform_matrix("view", self.view)
            obj.set_uniform_matrix("projection", self.projection)

            obj.render()


class Rectangle:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx

        self.uniforms = {}
        self.uniforms_matrices = {}

        self.program = self.get_shader_program("triangle")
        self.vbo = self.ctx.buffer(self.get_vertices())
        self.vao = self.ctx.vertex_array( self.program, [(self.vbo, '2f 3f', 'in_pos', 'in_color')])

    def render(self):

        for name in self.uniforms:
            self.program[name].value = self.uniforms[name]

        for name in self.uniforms_matrices:
            self.program[name].write(self.uniforms_matrices[name])

        self.vao.render(mode=moderngl.TRIANGLE_STRIP)

    def get_vertices(self):
        return np.array([ [
             -0.5, -0.5, 1.0, 0.0, 0.0,
              0.5, -0.5, 0.0, 1.0, 0.0,
             -0.5,  0.5, 0.0, 0.0, 1.0,
              0.5,  0.5, 1.0, 1.0, 1.0
             ]], dtype='f4')

    def set_uniform(self, name: str, value: float):
        self.uniforms[name] = value

    def set_uniform_matrix(self, name, matrix):
        self.uniforms_matrices[name] = matrix

    def get_shader_program(self, name):
        path = f"shader/{name}/"

        with open(path + "vertex.glsl") as f:
            vertexData = f.read()

        with open(path + "fragment.glsl") as f:
            fragmentData = f.read()

        return self.ctx.program(vertex_shader=vertexData, fragment_shader=fragmentData)

class Engine:
    def __init__(self, size=(1280, 720), fps=60) -> None:
        # CONSTANTS
        self.size = size
        self.fps = fps

        # OBJECTS
        self.window = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.ctx = moderngl.create_context()

        self.cam = Camera(self)
        self.cam.scene.append(Rectangle(self))
        # self.scene = [Triangle(self)]

        # BOOLS
        self.is_running = True

    def update(self):
        pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")
        self.ctx.clear(color=(0.0, 0.0, 0.0, 1.0))

        self.cam.update()
        self.cam.render()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.is_running = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    Engine().run()
