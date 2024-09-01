import platform
import sys


if platform.system() == 'Windows':
    pass
else:
    import termios
    import tty

#from .._utils import ANSICodeBase
class ANSICodeBase:
    def __init__(self, v): ...
    def __call__(self): ...

class Cursor:
    r"""A class for manipulating the terminal cursor."""

    class __ANSICodes:
        HOME = ANSICodeBase("0;0H")
        UP = ANSICodeBase("A")
        DOWN = ANSICodeBase("B")
        FORWARD = ANSICodeBase("C")
        BACKWARD = ANSICodeBase("D")
        SAVE = ANSICodeBase("s")
        RESTORE = ANSICodeBase("u")
        REQUEST_CURSOR_POS = ANSICodeBase("6n")
        HIDE = ANSICodeBase("?25l")
        SHOW = ANSICodeBase("?25h")

    def __init__(self) -> None:
        raise RuntimeError("This class should not be instantiated.")

    @classmethod
    def home(cls) -> None:
        r"""Moves the cursor to the top left of the terminal screen."""
        cls.__ANSICodes.HOME()

    @classmethod
    def up(cls, count: int = 1) -> None:
        r"""
        Moves the cursor up ``count`` times
        :param count:
        """
        for _ in range(count):
            cls.__ANSICodes.UP()

    @classmethod
    def down(cls, count: int = 1) -> None:
        r"""
        Moves the cursor down ``count`` times
        :param count:
        """
        for _ in range(count):
            cls.__ANSICodes.DOWN()

    @classmethod
    def forward(cls, count: int = 1) -> None:
        r"""
        Moves the cursor forward ``count`` times
        :param count:
        """
        for _ in range(count):
            cls.__ANSICodes.FORWARD()

    @classmethod
    def backward(cls, count: int = 1) -> None:
        r"""
        Moves the cursor backward ``count`` times
        :param count:
        """
        for _ in range(count):
            cls.__ANSICodes.BACKWARD()

    @classmethod
    def save_pos(cls) -> None:
        r"""Saves the current cursor position."""
        cls.__ANSICodes.SAVE()

    @classmethod
    def restore_pos(cls) -> None:
        r"""Restores the saved cursor position."""
        cls.__ANSICodes.RESTORE()

    @classmethod  # !!DOESN'T WORK RN!! TODO: LOOK INTO IT AND FIX IT
    def __get_pos(cls) -> tuple[int, int]:  # !!TEMPORARILY ADDED __
        r"""Returns the current cursor position as (x, y)."""
        if platform.system() == 'Windows':
            from ctypes import Structure, c_short, c_ushort, windll, byref

            class COORD(Structure):
                _fields_ = [("X", c_short), ("Y", c_short)]

            class SMALL_RECT(Structure):
                _fields_ = [("Left", c_short), ("Top", c_short),
                            ("Right", c_short), ("Bottom", c_short)]

            class CONSOLE_SCREEN_BUFFER_INFO(Structure):
                _fields_ = [("dwSize", COORD),
                            ("dwCursorPosition", COORD),
                            ("wAttributes", c_ushort),
                            ("srWindow", SMALL_RECT),
                            ("dwMaximumWindowSize", COORD)]

            csbi = CONSOLE_SCREEN_BUFFER_INFO()
            if windll.kernel32.GetConsoleScreenBufferInfo(
                windll.kernel32.GetStdHandle(-11), byref(csbi)
            ):
                X = csbi.dwCursorPosition.X + 1
                Y = csbi.dwCursorPosition.Y + 1
                return X, Y
            else:
                raise RuntimeError("Failed to get cursor position.")
        else:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)

            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdout.flush()
                cls.__ANSICodes.REQUEST_CURSOR_POS()

                response = ''
                while True:
                    c = sys.stdin.read(1)
                    if c == 'R':
                        break
                    response += c

                if response.startswith('\033['):
                    response = response[2:]
                    y, x = response.split(';')
                    return int(x), int(y)
                else:
                    raise ValueError(f"Failed to get cursor position. \nResponse: {response}")

            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

    @classmethod
    def set_pos(cls, x: int, y: int) -> None:
        r"""
        Sets the cursor position to (``x``, ``y``)
        :param x:
        :param y:
        """
        if x <= 0 or y <= 0:
            raise ValueError(f"Invalid cursor position. x: {x}, y: {y}\n"
                             f"The cursor starts at (1, 1).")
        ANSICodeBase(f"{y};{x}H")()

    @classmethod
    def hide(cls) -> None:
        r"""Hides the cursor."""
        cls.__ANSICodes.HIDE()

    @classmethod
    def show(cls) -> None:
        r"""Shows the cursor."""
        cls.__ANSICodes.SHOW()
