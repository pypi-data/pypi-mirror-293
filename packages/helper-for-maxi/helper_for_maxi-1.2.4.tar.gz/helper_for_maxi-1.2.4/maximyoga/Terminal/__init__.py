# -*- coding: utf-8 -*-

"""
Terminal
~~~~~~~~

Contains Stuff for the Terminal
"""
import platform as __platform

if __platform.system() == "Windows":
    from ._choice_interface import ChoiceInterface

from ._cursor import Cursor
from ._manager import Manager