from .Terminal.color import foreground
from ._better_input import better_input
from ._check_params_decorator import check_params
from ._utils import ANSICodeBase


@check_params
def better_color_input(
        *args,
        sep: str = ' ',
        delay: float = .01,
        beforeColor: ANSICodeBase = foreground.RESET,
        inputColor: ANSICodeBase = foreground.CYAN
) -> str:
    r"""
    Prints ``args`` seperated by ``sep`` with the given ``delay`` between each character and gets an
    input in ``inputColor``. Resets the color to ``beforeColor`` afterwards
    :param args:
    :param sep:
    :param delay:
    :param beforeColor:
    :param inputColor:
    :return: The received input string
    """

    if not args:
        text: str | None = None
    else:
        text = sep.join(map(str, args))

    if text is not None:
        res = better_input(text + inputColor, delay=delay)
    else:
        res = better_input(inputColor, delay=delay)

    print(beforeColor.value, end="")

    return res