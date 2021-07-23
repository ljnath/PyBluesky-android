from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame import Surface


# Define a ScoreText class object by Text class
class ScoreText(Text):
    """ ScoreText class extended from Text class.
        It creates the game score sprite
    """
    def __init__(self):
        game_env = GameEnvironment()
        Text.__init__(self, text="LEVEL 00 TIME 0 AMMO 0 SCORE 0 HEALTH 0", size=game_env.static.score_sprite_size, color=(103, 103, 103))  # initializing parent class with defautl text and color
        self.rect = self.surf.get_rect(topright=(game_env.static.screen_width - self.surf.get_width() / 2, 2))                              # creating rectangle from text surface

        self.surf = Surface((200, game_env.static.score_sprite_size), game_env.SRCALPHA, 32)
        self.rect = self.surf.get_rect(topright=(600, 5))

    def update(self):
        game_env = GameEnvironment()
        self.surf = Surface((game_env.static.screen_width, game_env.static.score_sprite_size), game_env.SRCALPHA, 32)

        # updating scoreboard score and time
        score_text = self.font.render(
            f"LEVEL {str(game_env.dynamic.game_level).zfill(2)} "
            f"TIME {str(game_env.dynamic.game_playtime).zfill(5)} "
            f"AMMO {str(game_env.dynamic.ammo).zfill(3)} "
            f"SCORE {str(game_env.dynamic.game_score).zfill(8)} "
            f"HEALTH ",
            1, self.color)

        # creating and filling color in health bar
        health_bar = Surface((game_env.dynamic.jet_health * 2, game_env.static.score_sprite_size - 22))
        health_bar.fill(self.__get_color(game_env.dynamic.jet_health))

        self.surf.blit(score_text, (0, 0))
        self.surf.blit(health_bar, (score_text.get_width() + 2, 2))

        self.rect = self.surf.get_rect(topleft=(10, 5))

    def __get_color(self, health):
        fill_color = (0, 0, 0)

        health100 = (37, 227, 0)
        health80 = (0, 254, 77)
        health60 = (255, 199, 62)
        health40 = (255, 111, 36)
        health20 = (255, 30, 19)

        if 80 < health <= 100:
            fill_color = health100
        elif 60 < health <= 80:
            fill_color = health80
        elif 40 < health <= 60:
            fill_color = health60
        elif 20 < health <= 40:
            fill_color = health40
        elif 0 < health <= 20:
            fill_color = health20

        return fill_color
