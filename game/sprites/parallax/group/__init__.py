import pygame


class ParallaxGroup(pygame.sprite.Group):
    """
    Custom Sprite Group class inherited from pygame.sprite.Group to implement len() functionality
    """
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def __len__(self):
        """
        Custom len() implementation for pygame.sprite.Group, as pygame.sprite.Group doesn't have this implementation
        """
        return len(self.sprites())
