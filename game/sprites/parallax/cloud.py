import random

from game.data.enums import BackgroundType, CloudType
from game.sprites.parallax import Parallax


class CloudParallax(Parallax):
    """
    CloudParallax sprite class for creating and updating the cloud in the game screen
    """
    def __init__(self, type: CloudType):
        """
        Constructor to create a cloud with a random cloud image
        :param type : Type of cloud that needs to be created
        """
        # super(CloudParallax, self).__init__()

        if type == CloudType.BIG:
            random_cloud = random.choice([BackgroundType.BIG_CLOUD_1,
                                          BackgroundType.BIG_CLOUD_2,
                                          BackgroundType.BIG_CLOUD_3,
                                          BackgroundType.BIG_CLOUD_4,
                                          BackgroundType.BIG_CLOUD_5])
        elif type == CloudType.SMALL:
            random_cloud = random.choice([BackgroundType.SMALL_CLOUD_1,
                                          BackgroundType.SMALL_CLOUD_2])
        elif type == CloudType.MEDIUM:
            random_cloud = random.choice([BackgroundType.MEDIUM_CLOUD_1,
                                          BackgroundType.MEDIUM_CLOUD_2,
                                          BackgroundType.MEDIUM_CLOUD_3])
        Parallax.__init__(self, type=random_cloud)

    def update(self) -> None:
        """
        Method to update the cloud sprite
        """
        super().update()
