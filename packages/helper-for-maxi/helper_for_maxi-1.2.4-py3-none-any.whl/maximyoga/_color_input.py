from .Terminal.color import foreground
from ._check_params_decorator import check_params
from ._utils import ANSICodeBase


@check_params
def color_input(
        *args,
        sep: str = ' ',
        beforeColor: ANSICodeBase | None = foreground.FGRESET,
        inputColor: ANSICodeBase = foreground.CYAN
) -> str:
    r"""
    Gets an input in CYAN. Resets the color to `beforeColor` afterwards
    :param args:
    :param sep:
    :param beforeColor:
    :param inputColor:
    :return:
    """
    if args:
        res = input(sep.join(map(str, args)) + inputColor)
    else:
        res = input(foreground.CYAN)
    if beforeColor is not None:
        beforeColor()
    return res