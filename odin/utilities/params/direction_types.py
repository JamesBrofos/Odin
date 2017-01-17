from .odin_enum import OdinEnum


class Directions(OdinEnum):
    """Direction Type Declaration Module

    Trades may either be long or short in Odin.
    """
    long_dir = "LONG"
    short_dir = "SHORT"

