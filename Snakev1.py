from pygame.locals import *
import pygame, random, os, time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Apple:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Snake:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        self.x[1] = 1 * 44
        self.x[2] = 2 * 44

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            #Позиция головы змейки
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Igra:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


class Game:
    windowWidth = 800
    windowHeight = 600
    snake = 0
    apple = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Igra()
        self.snake = Snake(3)
        self.apple = Apple(5, 5)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Змейка')
        self._running = True
        self._image_surf = load_image('snake1.jpg')
        self._apple_surf = load_image('apple1.png')

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.snake.update()

        #Проверка съела ли змейка яблоко
        for i in range(0, self.snake.length):
            if self.game.isCollision(self.apple.x, self.apple.y, self.snake.x[i], self.snake.y[i], 44):
                self.apple.x = random.randint(2, 9) * 44
                self.apple.y = random.randint(2, 9) * 44
                self.snake.length = self.snake.length + 1

        #Проверка врезается ли змейка
        for i in range(2, self.snake.length):
            if self.game.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i], 40):
                print('Вы проиграли')
                exit(0)

        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.snake.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.snake.moveRight()

            if (keys[K_LEFT]):
                self.snake.moveLeft()

            if (keys[K_UP]):
                self.snake.moveUp()

            if (keys[K_DOWN]):
                self.snake.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0)
        self.on_cleanup()


if __name__ == "__main__":
    app = Game()
    app.on_execute()
