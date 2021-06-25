from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame.surface import Surface


class ReplayMenuText(Text):
    """ ReplayText class extended from Text class.
        It creates the game replay menu sprite
    """
    def __init__(self):
        Text.__init__(self, size=30)                                                                  # initilizing parent class with default text color as red
        game_env = GameEnvironment()
        self.__gameover = Text("GAME OVER", 60)

        self.__replaytext_surf = self.font.render("Replay ", 1, self.color)                                     # creating surface with the Replay text

        self.__y_selected_surf = self.font.render("Yes", 1, game_env.static.text_selection_color)               # creating surface with Yes text when highlighted
        self.__n_surf = self.font.render("/No", 1, self.color)                                                   # creating surface with No text
        self.__y_surf = self.font.render("Yes/", 1, self.color)                                                 # creating surface with Yes text
        self.__n_selected_surf = self.font.render("No", 1, game_env.static.text_selection_color)                 # creating surface with No text when highlighted

        self.__replaytext_pos_x = self.__gameover.surf.get_width() / 2 - (self.__replaytext_surf.get_width() + self.__y_selected_surf.get_width() + self.__n_surf.get_width()) / 2

        self.__highlight_yes()                                                                                     # calling method to highlight Yes (the default choice)

    def __recreate_surf(self):
        game_env = GameEnvironment()
        # creating default surface of combination of expected length
        self.surf = Surface((self.__gameover.surf.get_width(), self.__gameover.surf.get_height() + self.__replaytext_surf.get_height()), game_env.SRCALPHA)
        self.surf.blit(self.__gameover.surf, (self.surf.get_width() / 2 - self.__gameover.surf.get_width() / 2, 0))         # updating the surface by drawing the prefex surface
        self.surf.blit(self.__replaytext_surf, (self.__replaytext_pos_x, self.__gameover.surf.get_height()))                # updating the surface by drawing the prefex surface

    def update(self, acceleration_values):
        if not acceleration_values or len(acceleration_values) != 3 or None in acceleration_values:            # validation of acceleration_values
            return

        game_env = GameEnvironment()
        y_axis = acceleration_values[1]
        if y_axis > 3:                                                                                          # checking if android device is tiled LEFT
            game_env.dynamic.replay = False                                                                    # setting game replay choice as False
            self.__highlight_no()                                                                               # calling method to highlight Nos
        elif y_axis < -3:                                                                                       # checking if android device is tiled RIGHT
            game_env.dynamic.replay = True                                                                      # setting game replay choice as True
            self.__highlight_yes()                                                                              # calling method to highlight Yes

        self.rect = self.surf.get_rect(center=(game_env.static.screen_width / 2, game_env.static.screen_height / 2 + 10))   # creating default rect and setting its position center below the GAME OVER text

    def __highlight_yes(self):
        self.__recreate_surf()
        self.surf.blit(self.__y_selected_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width(), self.__gameover.surf.get_height()))                                  # updating the surface by drawing the highlighted Yes after the prefix
        self.surf.blit(self.__n_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width() + self.__y_selected_surf.get_width(), self.__gameover.surf.get_height()))      # updating the surface by drawing the No after the highlighted Yes

    def __highlight_no(self):
        self.__recreate_surf()
        self.surf.blit(self.__y_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width(), self.__gameover.surf.get_height()))                                           # updating the surface by drawing the Yes after the prefix
        self.surf.blit(self.__n_selected_surf, (self.__replaytext_pos_x + self.__replaytext_surf.get_width() + self.__y_surf.get_width(), self.__gameover.surf.get_height()))      # updating the surface by drawing the highlighted No after the Yes
