import pyperclip

from ._check_params_decorator import check_params


@check_params
def append_clipboard(text: str) -> str:
    r"""
    Appends the given ``text`` to the clipboard
    :param text:
    :return: The given ``text``
    """
    pyperclip.copy(text)
    return text