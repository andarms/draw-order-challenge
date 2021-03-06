import sys
import random
import pygame as pg

# Importing prepare initializes the display.
import prepare
import actors
from camera import Camera
        
            
class App(object):
    """This is the main class that runs the program."""
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock  = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.all_sprites = pg.sprite.LayeredDirty()
        self.visible_sprites = pg.sprite.LayeredDirty()
        self.player = actors.Player(self.screen_rect.center, 3)
        self.all_sprites.add(self.player)
        self.make_npcs()
        self.camera = Camera(prepare.SCREEN_SIZE, self.player.rect.center)

    def make_npcs(self):
        """Create a group of NPCs and add them to the all_sprites group."""
        for name in prepare.GFX:
            if name != self.player.name:
                pos = [random.randint(50,400), random.randint(50,400)]
                speed = random.randint(1,2)
                way = random.choice(prepare.DIRECTIONS)
                actors.AISprite(pos, speed, name, way, self.all_sprites)

    def event_loop(self):
        """
        Process all events.
        Send event to player so that they can also handle the event.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.player.get_event(event)

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        template = "{} - FPS: {:.2f}"
        caption = template.format(prepare.CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def update(self):
        """Update all actors."""
        now = pg.time.get_ticks()
        self.all_sprites.update(now, self.screen_rect)
        self.camera.update(self.player)
        visible_sprites = pg.sprite.spritecollide(self.camera, self.all_sprites, False)
        self.visible_sprites.add(visible_sprites)
        for sprite in self.visible_sprites.sprites():
            self.visible_sprites.change_layer(sprite, sprite.rect.bottom)
            if sprite not in visible_sprites:
                self.visible_sprites.remove(sprite)

    def render(self):
        """Fill screen and render all actors."""
        self.screen.fill(prepare.BACKGROUND_COLOR)
        self.visible_sprites.draw(self.screen)
        self.camera.render(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        The main game loop for the whole program.
        Process events; update; render.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            self.display_fps()


def main():
    """Create an App and start the program."""
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()