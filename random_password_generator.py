import os
import random
import string


os.system('cls' if os.name == 'nt' else 'clear')


# Variables

DIGITS = '0123456789'
SYMBOLS = """!?@#$%&*^~/\|+=:;.,"'`"""
BRACKET = '[]{}()<>'
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 25
DEFAULT_PASSWORD_LENGTH = 8



def ask_if_change_settings(settings):

    prompt = "Do you want to change the default settings? [y/n]: "
    valid_yes = ['y', '']
    valid_no = 'n'

    while True:
        user_answer = input(prompt).strip().lower()

        if user_answer in valid_yes:
            print('-'*5, 'Changing default settings', '-'*5, sep='')
            get_password_settings(settings)
            break
        elif user_answer == valid_no:
            random_password_generator(settings)
            break
        else:
            print("Invalid input! Please enter "
                  "'y' for yes, 'n' for no, "
                  "or press Enter to accept the default.")



def get_user_password_length(option, default, min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH):
    while True:
        user_input = input(f'{option} (Default is {default})')
        
        if user_input.isdigit():
            password_length = int(user_input)
            if min_length <= password_length <= max_length:
                return password_length
            
        print('Invalid input!')
        print('Password length must be between '
             f'{min_length} and {max_length}. '
              'Please try again.')


def get_user_password_settings(option, default):
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


def get_password_settings(settings_dict):

    for option, default in settings_dict.items():

        if option == 'password_length':
            settings_dict[option] = get_user_password_length(option, default)
        else:
            settings_dict[option] = get_user_password_settings(option, default)



def generate_upper_case_char():
    return random.choice(string.ascii_uppercase)


def generate_lower_case_char():
    return random.choice(string.ascii_lowercase)


def generate_digit():
    return random.choice(DIGITS)


def generate_symbol():
    return random.choice(SYMBOLS)


def generate_bracket():
    return random.choice(BRACKET)



def generated_password_char(password_settings):
    char_type = random.choice(password_settings)

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

    if char_type in generators:
        return generators[char_type]()
        

def random_password_generator(settings):

    password_length = settings['password_length']
    
    enabled_char_types = []
    all_options = ['uppercase', 'lowercase', 'bracket', 'symbol', 'digit', 'space', 'minus', 'underline']
    
    for option in all_options:
        if settings.get(option):
            enabled_char_types.append(option)

    password_chars = []
    for _ in range(password_length):
        password_chars.append(generated_password_char(enabled_char_types))

    return ''.join(password_chars)


def print_generated_password(settings):
    border = '*' * 20
    print(border)
    
    password = random_password_generator(settings)
    print(f'Generated password: {password}')
    
    print(border)
    


def regenerate_random_password(settings):

    prompt = "Regenerate? [y/n] (Enter = yes by default): "
    valid_yes = ['y', '']
    valid_no = 'n'

    while True:

        user_input = input(prompt).strip().lower()

        if user_input in valid_yes:
            print_generated_password(settings)

        elif user_input == valid_no:
            print('Thanks for choosing us. Good luck.')
            break

        else:
            print("Invalid input. please enter 'y' or 'n'.")
            


def run(settings):
    """
    Run the password generator workflow:
    1. Ask user to change settings.
    2. Print the generated password.
    3. Allow user to regenerate password.
    """
    ask_if_change_settings(settings_dict)
    print_generated_password(settings_dict)
    regenerate_random_password(settings_dict)
    


if __name__ == "__main__":
    
    settings_dict = {
        'password_length': DEFAULT_PASSWORD_LENGTH,
        'uppercase': True,
        'lowercase': True,
        'digit': True,
        'space': True,
        'minus': True,
        'underline': True,
        'symbol': True,
        'bracket': True,
    }

    run(settings_dict)