import pygame
import moderngl
import numpy as np

class Triangle:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx
        self.program = self.get_shader_program("triangle")
        self.vbo = self.ctx.buffer(self.get_vertices())
        self.vao = self.ctx.vertex_array( self.program, [(self.vbo, '2f', 'in_pos')])

    def render(self):
        self.vao.render()

    def get_vertices(self):
        return np.array([
            [-0.5, -0.5],
            [ 0.5, -0.5],
            [ 0.0,  0.5]
            ], dtype='f4')

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

        self.scene = [Triangle(self)]

        # BOOLS
        self.is_running = True

    def update(self):
        pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")
        self.ctx.clear(color=(0.0, 0.0, 0.0, 1.0))

        for obj in self.scene:
            obj.render()

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
