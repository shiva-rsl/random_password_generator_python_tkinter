from utils import *


# ----------------------------- Constants ----------------------------- #
BORDER = '*' * 20


# ----------------------------- Functions ----------------------------- #
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
            A dictionary of password settings with option names as keys.

    Returns:
        None: modifies the dictionary in-place.
    """
    
    for option, default in settings.items():

        if option == 'password_length':
            settings[option] = get_user_password_length(option, default)
        else:
            settings[option] = get_user_password_settings(option, default)


def get_generated_password(settings: PasswordSettings) -> str:
    """
    Generate a random password.
    
    Args:
        settings (PasswordSettings): 
            A dictionary of password settings with option names as keys.
    
    Returns:
        str: The generated random password.
    """
    return random_password_generator(settings)


def generate_password_with_metrics(settings: PasswordSettings) -> tuple[str, float, str]:
    """
    Generate a password along with its entropy and strength label.

    Args:
        settings (PasswordSettings): 
            A dictionary of password settings with option names as keys.
    
    Returns:
        tuple: A tuple containing:
            - str: The generated password
            - float: The password entropy in bits
            - str: The password strength label
    """
    password = get_generated_password(settings)
    entropy = calculate_password_entropy(password)
    _, strength_label, _ = calculate_password_strength(password)
    return password, entropy, strength_label


def print_generated_password_entropy_strength(settings: PasswordSettings) -> None:
    """
    Print a generated password along with its entropy and strength to the console. 

    Args:
        settings (PasswordSettings): 
            A dictionary of password settings with option names as keys.
    
    Returns:
        None
    """
    password, entropy, strength = generate_password_with_metrics(settings)
    print(BORDER)
    print(f"Generated password : {password}")
    print(f"Strength           : {strength}")
    print(f"Entropy            : {entropy:.2f} bits")
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
            print_generated_password_entropy_strength(settings)

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
    print_generated_password_entropy_strength(settings)
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