"""
Class responsible for acting as metaclass for generation of singleton classes
"""


class Singleton(type):
    """
    Class responsible for acting as metaclass for generation of singleton classes
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args,
                **kwargs
            )
        return cls._instances[cls]
