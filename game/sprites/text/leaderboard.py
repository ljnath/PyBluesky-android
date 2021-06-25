import time

from game.environment import GameEnvironment
from game.handlers.leaderboard import LeaderBoardHandler
from game.sprites.text import Text
from pygame.surface import Surface


class LeaderBoardText(Text):
    """ LeaderBoardText class extended from Text class.
        It creates the the leaderboard table sprite
    """
    def __init__(self):
        Text.__init__(self, size=22)
        game_env = GameEnvironment()
        name_length = game_env.static.name_length * 2
        leaders = LeaderBoardHandler().load()
        seperator = self.font.render('===================================================================================================', 1, self.color)
        header = self.font.render('=== HALL OF FAME ===', 1, self.color)
        all_surfaces = []
        all_surfaces.append(seperator)
        all_surfaces.append(self.font.render(f"{'RANK'.ljust(5)} {'NAME'.ljust(name_length)} {'SCORE'.ljust(10)} {'LEVEL'.ljust(5)} {'ACCURACY'.ljust(8)} {'TIME'.rjust(21)}", 1, self.color))
        all_surfaces.append(seperator)
        try:
            if len(leaders) == 0:
                all_surfaces.append(self.font.render('No records, make sure you have working internet connectivity', 1, self.color))

            for index, score in enumerate(leaders['scores']):
                all_surfaces.append(self.font.render(f"{str(index+1).ljust(5)} {score['name'][:name_length].ljust(name_length)} {str(score['score']).ljust(10)} {str(score['level']).ljust(5)} {str(score['accuracy'] + '%').ljust(8)} {str(time.ctime(int(score['epoch']))).rjust(25)}", 1, self.color))
        except Exception:
            pass
        all_surfaces.append(seperator)

        self.surf = Surface((all_surfaces[2].get_width(), all_surfaces[0].get_height() * (len(all_surfaces) + 1)), game_env.SRCALPHA)

        self.surf.blit(header, (self.surf.get_width() / 2 - header.get_width() / 2, 0))
        for index, temp_surf in enumerate(all_surfaces):
            self.surf.blit(temp_surf, (0, header.get_height() + index * temp_surf.get_height()))

        self.rect = self.surf.get_rect(center=(game_env.static.screen_width / 2, game_env.static.screen_height / 2))
