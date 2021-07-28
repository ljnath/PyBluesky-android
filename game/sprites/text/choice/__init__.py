"""
Menu layout
+-------------------------------------------------+
|                   TITLE TEXT                    |
|                                                 |
|                    QUESTION ?                   |
|                                                 |
|     CHOICE_1                         CHOICE2    |
+-------------------------------------------------+
"""
from abc import ABC, abstractmethod
from typing import Tuple

from game.data.enums import Choice
from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame.surface import Surface


class ChoiceText(Text, ABC):
    """ PauseTextMenu class extended from Text class.
        It creates the game exit menu with confirmation sprite
    """
    def __init__(self, title: str, question: str, choices: Tuple[Choice, Choice]):
        Text.__init__(self)
        title_font_size = 90
        normal_font_size = 40
        space_padding = ' ' * 5

        self.__game_env = GameEnvironment()
        self.user_choice = Choice.UNSELECTED

        self.__title_text = Text(title, title_font_size)
        self.__choices = choices

        choice_1_text = f'{space_padding}{choices[0].value}'
        choice_2_text = f'{choices[1].value}{space_padding}'

        self.__question = Text(question, normal_font_size)
        self.choice1 = Text(choice_1_text, normal_font_size, self.color)
        self.choice2 = Text(choice_2_text, normal_font_size, self.color)

        self.choice1_selected = Text(choice_1_text, normal_font_size, self.__game_env.static.text_selection_color)
        self.choice2_selected = Text(choice_2_text, normal_font_size, self.__game_env.static.text_selection_color)

        self.__title_text_height = self.__question.surf.get_height()
        self.__normal_text_height = self.__question.surf.get_height()
        self.__max_surface_width = self.__question.surf.get_width()

        # rendering the screen to create the rect for collidepoint detection
        self.render()

        # updating position of the CHOICE buttons
        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width / 2, self.__game_env.static.screen_height / 2))

        pos_x = self.rect.left
        pos_y = self.rect.top + self.__title_text_height + self.__normal_text_height * 3
        self.choice1.rect.update(pos_x, pos_y, self.choice1.surf.get_width(), self.choice1.surf.get_height())
        self.choice1_selected.rect.update(pos_x, pos_y, self.choice1.surf.get_width(), self.choice1.surf.get_height())

        pos_x += self.__max_surface_width - self.choice2.surf.get_width()
        self.choice2.rect.update(pos_x, pos_y, self.choice2.surf.get_width(), self.choice2.surf.get_height())
        self.choice2_selected.rect.update(pos_x, pos_y, self.choice2.surf.get_width(), self.choice2.surf.get_height())

    def render(self) -> None:
        """
        Method to render the menu with title, question and choice buttons
        """
        # created a surface with all the text sprites
        self.surf = Surface((self.__max_surface_width, self.__title_text_height + self.__normal_text_height * 4), self.__game_env.SRCALPHA)
        self.surf.blit(self.__title_text.surf, (self.__max_surface_width / 2 - self.__title_text.surf.get_width() / 2, 0))
        self.surf.blit(self.__question.surf, (self.__max_surface_width / 2 - self.__question.surf.get_width() / 2, self.__title_text_height + self.__normal_text_height * 2))

        self.surf.blit(self.choice1_selected.surf if self.user_choice == self.__choices[0] else self.choice1.surf,
                       (0, self.__title_text_height + self.__normal_text_height * 3))

        self.surf.blit(self.choice2_selected.surf if self.user_choice == self.__choices[1] else self.choice2.surf,
                       (self.__max_surface_width - self.choice2.surf.get_width(), self.__title_text_height + self.__normal_text_height * 3))

    @abstractmethod
    def check_input(self, position: Tuple[int, int]) -> None:
        """
        Abstract method for handling user input
        """
        raise NotImplementedError()
