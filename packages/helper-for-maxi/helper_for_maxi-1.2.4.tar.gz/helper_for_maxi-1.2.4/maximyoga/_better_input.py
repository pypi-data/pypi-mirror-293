from ._better_print import better_print
from ._check_params_decorator import check_params


@check_params
def better_input(*args, sep: str = ' ', delay: float = .01) -> str:
    r"""
    Prints args seperated by sep with the given delay between each character and gets an input
    :param args:
    :param sep:
    :param delay:
    :return: The received input string
    """

    if not args:
        text = ''
    else:
        text = sep.join(map(str, args))

    if text:
        better_print(text, delay=delay, end='')
    res = input()
    return res
