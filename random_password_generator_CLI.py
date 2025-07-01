import os
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


def clear_screen() -> None:
    """
    Clear the terminal or console screen.

    Attempts to run the appropriate system command to clear the screen 
    depending on the operating system ('cls' for Windows, 'clear' for Unix/Linux). 
    If the command fails, it falls back to printing multiple newlines 
    to simulate clearing the screen.
    
    Returns:
        None
    """

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        print('\n' * 100)



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



def ask_if_change_settings(settings: PasswordSettings) -> None:
    
    """
    Prompt the user to decide if they want to change the default password settings.

    The user is repeatedly asked until a valid response is provided:
    - 'y' or Enter (empty input): proceeds to change the settings by calling `get_password_settings`.
    - 'n': skips changing settings and generates a password with current settings.
    - Other inputs: prompts the user again with an error message.

    Args:
        settings (PasswordSettings): 
            A dictionary of current password settings to be potentially modified.

    Returns:
        None
    """

    prompt = (
        "Do you want to change the default settings? "
        "(y = yes, n = no, Enter = yes): "
    )
    valid_yes = {'y', ''}
    valid_no = 'n'

    while True:
        user_answer = input(prompt).strip().lower()

        if user_answer in valid_yes:
            print('-'*5, 'Changing default settings', '-'*5, sep='')
            get_password_settings(settings)
            break
        elif user_answer == valid_no:
            break
        else:
            print("Invalid input! Please enter 'y' for yes, "
                  "'n' for no, or press Enter to accept the default.")
            


def get_user_password_length(option: str, default: int,
                            min_length: int = MIN_PASSWORD_LENGTH, 
                            max_length: int = MAX_PASSWORD_LENGTH) -> int:
    
    """
    Prompt the user to enter a password length within a specified range.

    The function repeatedly asks for input until the user enters a valid integer
    within the `min_length` and `max_length` bounds. The default value is shown in the prompt.

    Args:
        option (str): The description or name of the option being set (used in the prompt).
        default (int): The default password length if the user presses Enter without input.
        min_length (int, optional): The minimum allowed password length. Defaults to MIN_PASSWORD_LENGTH.
        max_length (int, optional): The maximum allowed password length. Defaults to MAX_PASSWORD_LENGTH.

    Returns:
        int: The validated password length input by the user.
    """

    while True:
        user_input = input(f'{option} (Default is {default}): ')
        
        if user_input == '':
            return default

        if user_input.isdigit():
            password_length = int(user_input)
            if min_length <= password_length <= max_length:
                return password_length
            
        print('Invalid input!')
        print('Password length must be between '
             f'{min_length} and {max_length}. '
              'Please try again.')



def get_user_password_settings(option: str, default: bool) -> bool:
    
    """
    Prompt the user to include or exclude a specific password option.

    The user is asked whether to include the option (e.g., uppercase letters,
    symbols) in the password. The prompt shows the default choice, which is
    returned if the user presses Enter without input.

    Args:
        option (str): The name of the password option to include or exclude.
        default (bool): The default setting for the option (True to include, False to exclude).

    Returns:
        bool: True if the option should be included, False otherwise.
    """

    prompt = (
        f"Include {option}? (Default is {default}) "
        "(y = True, n = False, Enter = Default): "
    )
    
    while True:
        user_input = input(prompt).strip().lower()

        if user_input == '':
            return default
        if user_input in {'y', 'n'}:
            return user_input == 'y'

        print("Invalid input! Please enter 'y' or 'n'.")



def get_password_settings(settings: PasswordSettings) -> None:
    
    """
    Prompt the user to update password settings.

    For each setting in the dictionary, asks the user to input a new value.
    For 'password_length', requests a numeric input within defined limits.
    For other options, asks for yes/no confirmation.

    Args:
        settings (PasswordSettings): 
            A dictionary of password settings with option names as keys and their default values.

    Returns:
        None: modifies the dictionary in-place.
    """
    
    for option, default in settings.items():

        if option == 'password_length':
            settings[option] = get_user_password_length(option, default)
        else:
            settings[option] = get_user_password_settings(option, default)



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



def print_generated_password(settings: PasswordSettings) -> None:

    """
    Generate and display a random password with a decorative border.

    This function generates a password based on the provided settings 
    and prints it to the console, wrapped with a decorative border for 
    improved readability.

    Args:
        settings (PasswordSettings): 
            An object containing the user-defined settings for password generation.

    Returns:
        None
    """

    print(BORDER)
    password = random_password_generator(settings)
    print(f'Generated password: {password}')
    print(BORDER)
    


def regenerate_random_password(settings: PasswordSettings) -> None:
    """
    Continuously prompts the user to regenerate a password until they decline.
    
    Args:
        settings (dict): A dictionary of password settings used for generation.

    Returns:
        None
    """
    
    prompt = "Regenerate? [y/n] (Enter = yes by default): "
    valid_yes = ['y', '']
    valid_no = 'n'

    while True:

        user_input = input(prompt).strip().lower()

        if user_input in valid_yes:
            print_generated_password(settings)

        elif user_input == valid_no:
            print('Password generator session ended. Goodbye!')
            break

        else:
            print("Invalid input! Please enter 'y' or 'n'.")
            


def run(settings: PasswordSettings) -> None:
    """
    Runs the main password generation workflow.

    This function performs the following steps:
    1. Clears the terminal screen.
    2. Prompts the user to optionally change password settings.
    3. Generates and prints a password based on the current settings.
    4. Offers the option to regenerate the password.

    Args:
        settings (PasswordSettings): The current configuration for password generation.

    Returns:
        None
    """

    clear_screen()
    ask_if_change_settings(settings)
    print_generated_password(settings)
    regenerate_random_password(settings)
    


if __name__ == "__main__":
    
    settings: PasswordSettings = {
        'password_length': DEFAULT_PASSWORD_LENGTH,
        'uppercase': True,
        'lowercase': True,
        'space': True,
        'minus': True,
        'underline': True,
        'digit': True,
        'symbol': True,
        'bracket': True,
    }

    run(settings)

