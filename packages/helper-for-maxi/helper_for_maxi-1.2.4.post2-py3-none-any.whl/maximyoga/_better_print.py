import time

from ._check_params_decorator import check_params


@check_params
def better_print(*args, sep: str = ' ', delay: float = .01, end: str = '\n') -> None:
    r"""
    Prints args seperated by sep with the given delay between each character
    :param args:
    :param sep:
    :param delay:
    :param end:
    :return:
    """

    if not args:
        text = ''
    else:
        text = sep.join(map(str, args))

    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(end)