"""
This module is part of the zen standard library, An alternative standard library for python.
Combines: string, difflib.
"""

__all__ = ['alphabet', 'alphabet_lowercase', 'alphabet_uppercase', 'digits', 'hexadecimals', 'octal', 'printable',
           'punctuation', 'special_characters', 'utf8_characters', 'whitespace_characters', 'capitalize_all_words',
           'capitalize_first_word', 'TextTemplate']

from .classes import TextTemplate
from .functions import capitalize_all_words, capitalize_first_word
from .constants import *


_ = alphabet, alphabet_lowercase, alphabet_uppercase, digits, hexadecimals, octal, printable, \
    punctuation, special_characters, utf8_characters, whitespace_characters, \
    capitalize_all_words, capitalize_first_word, TextTemplate
