import random
from os import system
from string import digits

from pygetwindow import getActiveWindowTitle
from pynput.keyboard import Key, KeyCode, Listener

from .color import background, foreground
from .._utils import ANSICodeBase


type _key = Key | KeyCode
type _keys = list[_key] | tuple[_key, ...]


def clear() -> None:
    system("cls")


class ChoiceInterface:
    def __init__(
            self, *,
            textColor: ANSICodeBase = foreground.WHITE,
            highlightTextColor: ANSICodeBase = foreground.BLACK,
            highlightBackgroundColor: ANSICodeBase = background.WHITE,
            confirmKey: _keys | _key = (Key.enter, Key.right),
            cancelKey: _keys | _key = Key.esc,
            navigatePreviousKeys: _keys | _key = Key.up,
            navigateNextKeys: _keys | _key = Key.down,
            choicesSurround: str = "",
            addArrowToSelected: bool = False,
            choicesOnLine: int = 1,
            seperator: str = ""
    ) -> None:
        r"""
        Creates an instance of the interface
        :param textColor:
        :param highlightTextColor:
        :param highlightBackgroundColor:
        :param confirmKey:
        :param cancelKey:
        :param navigatePreviousKeys:
        :param navigateNextKeys:
        :param choicesSurround:
        :param addArrowToSelected:
        :param choicesOnLine:
        :param seperator:
        :raises ValueError: if values in confirmKey and cancelKey overlap
        """
        cfKeys = self.__conv_keys(confirmKey)
        ccKeys = self.__conv_keys(cancelKey)
        npKeys = self.__conv_keys(navigatePreviousKeys)
        nnKeys = self.__conv_keys(navigateNextKeys)

        seenKeys = set()
        for key in cfKeys + ccKeys + npKeys + nnKeys:
            if key in seenKeys:
                raise ValueError("Parameters specifying Keys may not overlap!")
            seenKeys.add(key)

        self.confirmKeys = cfKeys
        self.cancelKeys = ccKeys
        self.navPrevKeys = npKeys
        self.navNextKeys = nnKeys
        self.textColor = textColor
        self.hlColor = highlightTextColor + highlightBackgroundColor
        self.choicesSurround = choicesSurround
        self.addArrowToSelected = addArrowToSelected
        self.choicesOnLine = choicesOnLine
        self.seperator = seperator
        self.terminalWindowTitle = ("Choice Interface {" +
                                    "".join(random.choices(digits, k=10)) + "}")
        self.lastKeyPressed = None

    @staticmethod
    def __conv_keys(item: tuple[_key, ...] | list[_key] | _key) -> list[_key]:
        if isinstance(item, tuple):
            return list(item)
        elif isinstance(item, list):
            return item
        return [item]

    def __call__(
            self,
            choices: list[str],
            prefix: str = "",
            suffix: str = "",
            selected: int = 0,
            minimumHighlightLength: int = 0,
            terminalTitleBefore: str = "Terminal",
            returnLine: bool = False
    ) -> int | tuple[int, str]:
        r"""
        Starts the interface
        :param choices:
        :param prefix:
        :param suffix:
        :param selected:
        :param minimumHighlightLength:
        :param terminalTitleBefore:
        :param returnLine:
        :return: The index of the chosen line, or, if ``returnLine`` is ``True``, a tuple of the
        index and the line itself.
        :raises ValueError: If an argument is invalid.
        :raises Exception: If an unexpected and unaccounted-for error occurs.
        """
        system(f"TITLE {self.terminalWindowTitle}")

        if len(choices) <= 1 or (not (isinstance(choices, list) and
                                      all([isinstance(x, str) for x in choices]))):
            raise ValueError("Parameter 'lines' must be of length >= 2 and of type list[str]")
        if 0 > selected >= len(choices):
            raise ValueError(
                "Parameter 'selected' must be index of line in 'lines' and may therefore not "
                "be bigger than the biggest index of 'lines' or smaller than 0"
            )

        if minimumHighlightLength > 0:
            hlLen = minimumHighlightLength
        else:
            hlLen = max([len(line) for line in choices]) + abs(minimumHighlightLength)
            if self.addArrowToSelected:
                hlLen += 3

        while True:
            clear()
            if prefix:
                print(self.textColor + prefix + foreground.RESET)

            _out = []
            for i, line in enumerate(choices):
                if i == selected:
                    if self.addArrowToSelected:
                        _out.append(
                            f"{self.hlColor}{line:<{hlLen - 3}} > "
                            f"{foreground.RESET}"
                        )
                    else:
                        _out.append(f"{self.hlColor}{line:<{hlLen}}{foreground.RESET}")
                else:
                    _out.append(f"{self.textColor}{line:<{hlLen}}{foreground.RESET}")
                if self.choicesSurround:
                    x = _out[-1]
                    _out[-1] = f"{self.choicesSurround}{x}{self.choicesSurround}"

            out = []

            for i, line in enumerate(_out):
                if i % self.choicesOnLine == 0 and i != 0:
                    out.append("\n")
                out.append(line)
                if (i + 1) % self.choicesOnLine != 0 and i != len(_out) - 1:
                    out.append(self.seperator)

            outputstring = "".join(out)
            print(outputstring)

            if suffix:
                print(self.textColor.value + prefix + foreground.RESET)

            key: _key | None = self._waitForKey()

            if key in self.navNextKeys and selected != len(choices) - 1:
                selected += 1
            elif key in self.navPrevKeys and selected != 0:
                selected -= 1
            elif key in self.confirmKeys:
                if key == Key.enter: input()
                system(f"TITLE {terminalTitleBefore}")
                if returnLine:
                    return selected, choices[selected]
                return selected
            elif key in self.cancelKeys:
                if key == Key.enter: input()
                system(f"TITLE {terminalTitleBefore}")
                if returnLine:
                    return -1, ""
                return -1
            elif key in self.navPrevKeys + self.navNextKeys:
                pass
            else:
                raise Exception("Somehow, Somewhere, Something went wrong :/")

    def _waitForKey(self) -> _key | None:
        lst = Listener(on_press=lambda key: self._onKeyPress(key, lst))
        lst.start()
        lst.join()
        return self.__lastKeyPressed

    def _onKeyPress(self, key: _key | None, lst: Listener) -> None:
        if getActiveWindowTitle() != self.terminalWindowTitle:
            return
        self.__lastKeyPressed = key
        validKeyList: list[_key] = (
                self.confirmKeys
                + self.cancelKeys
                + self.navPrevKeys
                + self.navNextKeys
        )
        if self.__lastKeyPressed in validKeyList:
            lst.stop()