from game.environment import GameEnvironment
from game.sprites.text import Text


# Define a ScoreText class object by Text class
class ScoreText(Text):
    """ ScoreText class extended from Text class.
        It creates the game score sprite
    """
    def __init__(self):
        game_env = GameEnvironment()
        Text.__init__(self, text="LEVEL 00 TIME 0 AMMO 0 SCORE 0 HEALTH 0", size=game_env.static.score_sprite_width, color=(103, 103, 103))  # initializing parent class with defautl text and color
        self.rect = self.surf.get_rect(topright=(game_env.static.screen_width - self.surf.get_width() / 2, 2))                      # creating rectangle from text surface

    def update(self):
        game_env = GameEnvironment()
        # updating scoreboard score and time
        self.surf = self.font.render(
            f"LEVEL {str(game_env.dynamic.game_level).zfill(2)} "\
            f"TIME {str(game_env.dynamic.game_playtime).zfill(5)} "\
            f"AMMO {str(game_env.dynamic.ammo).zfill(3)} "\
            f"SCORE {str(game_env.dynamic.game_score).zfill(8)} "\
            f"HEALTH {str(game_env.dynamic.jet_health).zfill(3)}",
            1, self.color)
