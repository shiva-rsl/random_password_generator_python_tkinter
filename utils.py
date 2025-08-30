import os
import re
import random
import string
from typing import Sequence, TypedDict


# Variables
BORDER = '*' * 20
DIGITS = '0123456789'
SYMBOLS = """!?@#$%&*^~/\|+=:;.,"'"""
BRACKETS = '[]{}()<>'
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 30
DEFAULT_PASSWORD_LENGTH = 8



class PasswordSettings(TypedDict):
    """
    Represents the settings for generating a password.

    Attributes:
        password_length (int): Desired length of the generated password.
        uppercase (bool): Include uppercase letters if True.
        lowercase (bool): Include lowercase letters if True.
        space (bool): Include spaces if True.
        minus (bool): Include minus '-' characters if True.
        underline (bool): Include underline '_' characters if True.
        digit (bool): Include digits from the DIGITS string if True.
        symbol (bool): Include special symbols from the SYMBOLS string if True.
        bracket (bool): Include brackets from the BRACKETS string if True.
    """

    password_length: int
    uppercase: bool
    lowercase: bool
    space: bool
    minus: bool
    underline: bool
    digit: bool
    symbol: bool
    bracket: bool


def clear_screen() -> None:
    """
    Clears the terminal screen.

    Uses 'cls' command on Windows and 'clear' on Unix-based systems.
    If the command fails, it prints multiple newlines as a fallback.
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        print('\n' * 100)



def generate_upper_case_char() -> str:
    """Return a random uppercase ASCII letter."""
    return random.choice(string.ascii_uppercase)



def generate_lower_case_char() -> str:
    """Return a random lowercase ASCII letter."""
    return random.choice(string.ascii_lowercase)



def generate_digit() -> str:
    """Return a random digit character from the DIGITS string."""
    return random.choice(DIGITS)



def generate_symbol() -> str:
    """Return a random symbol character from the SYMBOLS string."""
    return random.choice(SYMBOLS)



def generate_bracket() -> str:
    """Return a random bracket character from the BRACKET string."""
    return random.choice(BRACKETS)


def generated_password_char(settings: Sequence[str]) -> str:

    """
    Generate a random character based on enabled password settings.

    This function randomly selects one character type from the provided list 
    of enabled options (e.g., 'uppercase', 'digit', 'symbol') and returns a 
    randomly generated character of that type.

    Args:
        settings (Sequence[str]): 
            A sequence of enabled character types to choose from.

    Returns:
        str: A randomly generated character from the selected character type.

    Raises:
        ValueError: If an unsupported character type is encountered.
    """
    char_type = random.choice(settings)

    generators = {
        'uppercase': generate_upper_case_char,
        'lowercase': generate_lower_case_char,
        'bracket': generate_bracket,
        'symbol': generate_symbol,
        'digit': generate_digit,
        'space': lambda: ' ',
        'minus': lambda: '-',
        'underline': lambda: '_'
    }

    generator_func = generators.get(char_type)
    if not generator_func:
        raise ValueError(f"Unsupported character type: {char_type}")
    return generator_func()



def random_password_generator(settings: PasswordSettings) -> str:
    """
    Generates a random password based on the given settings.

    Args:
        settings (dict): A dictionary containing user preferences for
                         character types and password length.

    Returns:
        str: A randomly generated password.
    """

    password_length = settings['password_length']
    
    enabled_char_types = []
    all_options = ['uppercase', 'lowercase', 'space', 'minus', 'underline', 'digit', 'symbol', 'bracket']
    
    for option in all_options:
        if settings.get(option):
            enabled_char_types.append(option)

    password_chars = []
    for _ in range(password_length):
        password_chars.append(generated_password_char(enabled_char_types))

    return ''.join(password_chars)

