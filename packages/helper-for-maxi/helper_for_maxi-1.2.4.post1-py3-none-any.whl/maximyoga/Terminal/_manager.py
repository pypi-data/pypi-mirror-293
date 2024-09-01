from .._utils import ANSICodeBase

class Manager:
    r"""A class for manipulating the terminal."""

    class __ANSICodes:
        CLEAR_SCREEN = ANSICodeBase("2J")
        CLEAR_CURSOR_TO_SCREEN_END = ANSICodeBase("0J")
        CLEAR_CURSOR_TO_SCREEN_START = ANSICodeBase("1J")
        CLEAR_LINE = ANSICodeBase("2K")
        CLEAR_CURSOR_TO_LINE_END = ANSICodeBase("0K")
        CLEAR_CURSOR_TO_LINE_START = ANSICodeBase("1K")

    @classmethod
    def clear_screen(cls) -> None:
        r"""Clears the terminal screen."""
        cls.__ANSICodes.CLEAR_SCREEN()

    @classmethod
    def clear_cur2s_end(cls) -> None:
        r"""Clears from the cursor to the end of the screen."""
        cls.__ANSICodes.CLEAR_CURSOR_TO_SCREEN_END()

    @classmethod
    def clear_cur2s_start(cls) -> None:
        r"""Clears from the cursor to the start of the screen."""
        cls.__ANSICodes.CLEAR_CURSOR_TO_SCREEN_START()

    @classmethod
    def clear_line(cls) -> None:
        r"""Clears the current line."""
        cls.__ANSICodes.CLEAR_LINE()

    @classmethod
    def clear_cur2l_end(cls) -> None:
        r"""Clears from the cursor to the end of the current line."""
        cls.__ANSICodes.CLEAR_CURSOR_TO_LINE_END()

    @classmethod
    def clear_cur2l_start(cls) -> None:
        r"""Clears from the cursor to the start of the current line."""
        cls.__ANSICodes.CLEAR_CURSOR_TO_LINE_START()