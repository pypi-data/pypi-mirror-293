from ansitoolkit.core.constants import AnsiGraphicsAndCharacterSets
from ansitoolkit.core.generator import ansi_graphics_and_character_set_sequence


class GraphicsAndCharacterSets:
    STANDARD_MODE = ansi_graphics_and_character_set_sequence(AnsiGraphicsAndCharacterSets.STANDARD_MODE)
    ENABLE_LINE_WRAPPING = ansi_graphics_and_character_set_sequence(AnsiGraphicsAndCharacterSets.ENABLE_LINE_WRAPPING)
    DISABLE_LINE_WRAPPING = ansi_graphics_and_character_set_sequence(AnsiGraphicsAndCharacterSets.DISABLE_LINE_WRAPPING)
    SET_CHARACTER_SET_G0 = ansi_graphics_and_character_set_sequence(AnsiGraphicsAndCharacterSets.SET_CHARACTER_SET_G0)
    SET_CHARACTER_SET_G1 = ansi_graphics_and_character_set_sequence(AnsiGraphicsAndCharacterSets.SET_CHARACTER_SET_G1)
