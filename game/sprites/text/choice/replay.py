from game.data.enums import Choice
from game.environment import GameEnvironment
from game.sprites.text.choice import ChoiceText


class ReplayChoiceText(ChoiceText):
    """
    ReplayChoiceText class extended from ChoiceText class.
    It creates the game exit menu with confirmation sprite
    """
    def __init__(self):
        ChoiceText.__init__(self, title='GAME OVER', question="DO YOU WANT TO RETRY?", choices=(Choice.YES, Choice.NO))

    def check_input(self, position) -> None:
        """
        Method to handle user interaction with the Replay Menu
        """
        game_env = GameEnvironment()
        if self.choice1.rect.collidepoint(position) or self.choice1_selected.rect.collidepoint(position):
            if self.user_choice == Choice.YES:
                game_env.dynamic.user_choice = Choice.YES
            self.user_choice = Choice.YES

        if self.choice2.rect.collidepoint(position) or self.choice2_selected.rect.collidepoint(position):
            if self.user_choice == Choice.NO:
                game_env.dynamic.user_choice = Choice.NO
            self.user_choice = Choice.NO

        self.render()
