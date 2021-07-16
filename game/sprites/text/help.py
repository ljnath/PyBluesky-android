from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame.surface import Surface


class HelpText(Text):
    """ HelpText class extended from Text class.
        It creates the game help sprite
    """
    def __init__(self):
        Text.__init__(self, size=22)
        game_env = GameEnvironment()
        seperator = self.font.render(' ', 1, self.color)
        header = self.font.render('=== HELP ===', 1, self.color)
        footer = self.font.render('=== GOOD LUCK ===', 1, self.color)
        all_surfaces = []
        all_surfaces.append(seperator)
        all_surfaces.append(self.font.render('Your objective should you choose to accept is to navigate your jet without getting hit by', 1, self.color))
        all_surfaces.append(self.font.render('the incoming missiles. For self-defence you can shoot down the enemy missiles. You are', 1, self.color))
        all_surfaces.append(self.font.render('armed with 100 special missiles. Level-up awards you another 100 special missiles and a', 1, self.color))
        all_surfaces.append(self.font.render('power-up star which will instantly deactivate all the enemy missiles.', 1, self.color))
        all_surfaces.append(self.font.render('Your jet can carry maximum 999 special missiles.', 1, self.color))
        all_surfaces.append(seperator)
        all_surfaces.append(self.font.render('During menu screen, move your device horizontally and vertically to select options in menu', 1, self.color))
        all_surfaces.append(self.font.render('and tap on screen to confirm. During gameplay, move your device horizontally and vertically', 1, self.color))
        all_surfaces.append(self.font.render('to control the jet and tap on the screen to shoot', 1, self.color))
        all_surfaces.append(self.font.render(' ', 1, self.color))
        all_surfaces.append(self.font.render('POINTS: Destroy Missle -> 10 pts. Power-up Star -> 100 pts. Level-up -> 10 pts.', 1, self.color))
        all_surfaces.append(seperator)

        self.surf = Surface((all_surfaces[1].get_width(), all_surfaces[0].get_height() * (len(all_surfaces) + 2)), game_env.SRCALPHA)

        self.surf.blit(header, (self.surf.get_width() / 2 - header.get_width() / 2, 0))
        for index, temp_surf in enumerate(all_surfaces):
            self.surf.blit(temp_surf, (0, header.get_height() + index * temp_surf.get_height()))
        self.surf.blit(footer, (self.surf.get_width() / 2 - footer.get_width() / 2, self.surf.get_height() - footer.get_height()))

        self.rect = self.surf.get_rect(center=(game_env.static.screen_width / 2, game_env.static.screen_height / 2))
