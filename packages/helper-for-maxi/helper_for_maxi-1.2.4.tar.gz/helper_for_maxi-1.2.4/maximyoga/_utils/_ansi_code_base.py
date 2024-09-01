from typing import Self

from .._output_stdout import output_stdout


class ANSICodeBase:
    def __init__(self, *values: int | str) -> None:
        if not values:
            raise ValueError("ANSICodeBase must be initialized with at least one value.")
        elif len(values) == 1 and isinstance(values[0], str):
            value: str = f"\033[{values[0]}"
            ansi_numbers: list[int] = []
        elif all(isinstance(value, int) for value in values):
            value: str = f"\033[{";".join(map(str, values))}m"
            ansi_numbers: list[int] = list(values)
        else:
            raise TypeError("ANSICodeBase can only be initialized with integers or a string.")

        self.value: str = value
        self.ansi_numbers: list[int] = ansi_numbers

    def __repr__(self) -> str:
        return self.value

    def __add__(self, other: str | Self) -> str | Self:
        if isinstance(other, str):
            return f"{self.value}{other}"
        elif isinstance(other, ANSICodeBase):
            if not other.ansi_numbers or not self.ansi_numbers:
                raise TypeError(
                    f"Can only add ANSICodeBase objects with ANSI number codes together."
                )
            return ANSICodeBase(*(self.ansi_numbers + other.ansi_numbers))  # problem
        else:
            raise TypeError(
                f"Cannot add value of type {type(other).__name__} to an ANSI code object."
            )

    def __radd__(self, other: str | Self) -> str | Self:
        if isinstance(other, str):
            return f"{other}{self.value}"
        elif isinstance(other, ANSICodeBase):
            if not other.ansi_numbers or not self.ansi_numbers:
                raise TypeError(
                    f"Can only add ANSICodeBase objects with ANSI number codes together."
                )
            return ANSICodeBase(*(other.ansi_numbers + self.ansi_numbers))  # problem
        else:
            raise TypeError(
                f"Cannot add value of type {type(other).__name__} to an ANSI code object."
            )

    def __call__(self) -> None:
        output_stdout(self.value)