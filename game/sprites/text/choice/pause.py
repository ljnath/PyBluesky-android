from game.data.enums import Choice
from game.environment import GameEnvironment
from game.sprites.text.choice import ChoiceText


class PauseChoiceText(ChoiceText):
    """ PauseTextMenu class extended from ChoiceText class.
        It creates the game pause menu with confirmation sprite
    """
    def __init__(self):
        ChoiceText.__init__(self, title='PAUSED', question="DO YOU WANT TO RESUME?", choices=(Choice.YES, Choice.NO))
        self.__game_env = GameEnvironment()

    def check_input(self, position):
        if self.choice1.rect.collidepoint(position) or self.choice1_selected.rect.collidepoint(position):
            if self.user_choice == Choice.YES:
                self.__game_env.dynamic.user_choice = Choice.YES
            self.user_choice = Choice.YES

        if self.choice2.rect.collidepoint(position) or self.choice2_selected.rect.collidepoint(position):
            if self.user_choice == Choice.NO:
                self.__game_env.dynamic.user_choice = Choice.NO
            self.user_choice = Choice.NO

        self.render()
