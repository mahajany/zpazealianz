import random

import pygame

# Initialize pygame to access the core methods etc. inside this module
from constants import *
from model.alien import Alien
from model.point2d import Point2d
from model.space_ship import SpaceShip
from model.velocity2d import Velocity2d
from pygame import mixer

class App:
    def __init__(self):
        self._running = True

        self._display_surf = None
        self.size = self.weight, self.height = SCREEN_WIDTH, SCREEN_HEIGHT

        self._player = None
        self._aliens = []
        self.background = None

        self.font = None
        self._message = None
        self._music = True


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        midScreen = Point2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        zeroVelocity = Velocity2d(0, 0)
        self._player = SpaceShip(midScreen, zeroVelocity, BASE_LOCATION + "assets\\images\\spaceship.png", "player")

        for i in range(MAX_ENIMIES):
            randomLocation = Point2d(random.randint(50, SCREEN_WIDTH-50), random.randint(50, SCREEN_HEIGHT-50))
            randomVelocity = Velocity2d(random.randint(-1 * ONE_STEP, ONE_STEP),
                                        random.randint(-1 * ONE_STEP, ONE_STEP))
            image_id = i % 5
            image_name = BASE_LOCATION + "assets\\images\\alien-" + str(image_id) + ".png"
            self._aliens.append(Alien(randomLocation, randomVelocity, image_name))

        # Title and Icon
        pygame.display.set_caption(GAME_NAME)
        # Icons made by <a href="https://www.flaticon.com/authors/pixel-buddha" title="Pixel Buddha">Pixel Buddha</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
        # icon = pygame.image.load(os.path.join(os.getcwd(), "assets", "icons", "ufo.png"))
        icon = pygame.image.load(BASE_LOCATION + "assets\\icons\\ufo.png")
        pygame.display.set_icon(icon)
        #
        # <a href="https://www.freepik.com/photos/star">Star photo created by wirestock - www.freepik.com</a>
        self.background = pygame.image.load(BASE_LOCATION + "assets\\images\\background.png")
        #
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self._message="Welcome"

        # Load background mucic
        mixer.music.load(BASE_LOCATION + "assets\\sounds\\background_mr_clown.wav")
        # ...and play it continuously (that is why -1 is there)
        if self._music:
            mixer.music.play(-1)
        self.sound_missile  = mixer.Sound(BASE_LOCATION + "assets\\sounds\\fire_missile.wav")
        self.sound_missile  = mixer.Sound(BASE_LOCATION + "assets\\sounds\\fire_missile-2.wav")
        self.sound_explosion  = mixer.Sound(BASE_LOCATION + "assets\\sounds\\boom.wav")

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            key_pressed = pygame.key.get_pressed()  # checking pressed key_pressed

            if key_pressed[pygame.K_LEFT]:
                self._player.velocity.x += -1 * ONE_STEP
            if key_pressed[pygame.K_RIGHT]:
                self._player.velocity.x += ONE_STEP
            if key_pressed[pygame.K_UP]:
                self._player.velocity.y += -1 * ONE_STEP
            if key_pressed[pygame.K_DOWN]:
                self._player.velocity.y += ONE_STEP
            if key_pressed[pygame.K_p]:
                self._player.velocity.set(Point2d(0,0))
            if key_pressed[pygame.K_SPACE]:
                self._player.fire_missile()
                if self._music:
                    self.sound_missile.play()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_m:
                    self._music=not self._music
                    if self._music:
                        mixer.music.play(-1)
                    else:
                        mixer.music.stop()


    def check_boundry(self, object):
        if object.__class__.__name__ == "Missile":
            if object.state == "fire" and (object.location.x <= 0 or object.location.x >= SCREEN_WIDTH - SHIP_WIDTH
                                           or object.location.y <= 0 or object.location.y >= SCREEN_HEIGHT - SHIP_HEIGHT):
                object.state = "ready"

        if object.location.x <= 0 or object.location.x >= SCREEN_WIDTH - 2*SHIP_WIDTH:
            object.velocity.x = -1 * object.velocity.x

        if object.location.y <= 0 or object.location.y >= SCREEN_HEIGHT - 2*SHIP_HEIGHT:
            object.velocity.y = -1 * object.velocity.y

    def on_loop(self):
        self.check_boundry(self._player)
        self.check_boundry(self._player.missile)

        self._player.unit_displacement()
        self._player.missile.unit_displacement()

        self.alien_actions()

    def alien_actions(self):
        # Check alien movements, if they are hit, have hit space-ship and if they are just bumping into each other
        for alien in self._aliens:
            self.check_boundry(alien)
            # Move aliens
            alien.unit_displacement()

            # Has any alien been hit?
            if self._player.missile.state == "fire" and \
                    alien.alive and \
                    Point2d.is_collideded((alien.mid_point()), self._player.missile.mid_point(),
                                          SHIP_HALF_WIDTH):
                self._player.score += 1
                alien.alive = False
                self._aliens.remove(alien)
                self._player.missile.state = "ready"
                if self._music:
                    self.sound_explosion.play()
                continue

            # Or have they devoured you..yum, yum, yum!
            if alien.alive and Point2d.is_collideded(alien.mid_point(), self._player.mid_point(), SHIP_WIDTH):
                self._player.score -= 1
                if self._music:
                    self.sound_explosion.play()

            # Or are these clumsy aliens just bumping into each other?
            for j in range(self._aliens.index(alien)+1, len(self._aliens)):
                 if Point2d.is_collideded(alien.mid_point(), self._aliens[j].mid_point(), SHIP_WIDTH):
                     self._aliens[j].velocity, alien.velocity = alien.velocity, self._aliens[j].velocity

    def on_render(self):
        self._display_surf.fill(BACKGROUND_COLOUR)
        # Show backgrounnd image
        self._display_surf.blit(self.background, TOP_LEFT)

        # Draw player
        self.draw(self._player)
        if self._player.missile.state == "fire":
            self.draw(self._player.missile)

        for alien in self._aliens:
            if alien.alive:
                self.draw(alien)
        # Update the game-window (display)

        self.draw_text("Score:" + str(self._player.score), Point2d(SHIP_HALF_WIDTH,10))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            self.on_event()
            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def draw(self, object):
        self._display_surf.blit(object.image, (object.location.x, object.location.y))

    def draw_text(self, message, location = Point2d(0,0)):
        text = self.font.render(message, True, (255, 255,255))
        self._display_surf.blit(text, (location.x, location.y))

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
    pygame.init()
