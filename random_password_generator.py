import os
import random
import string


os.system('clear')


# Variables

DIGITS = '0123456789'
SYMBOL = """!?@#$%&*^~/\|+=:;.,"'`"""
BRACKET = '[]{}()<>'
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 25
DEFAULT_PASSWORD_LENGTH = 8



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


def get_user_password_length(option, default, min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH):
    while True:
        user_input = input(f'{option} (Default is {default})')
        if(
            user_input.isdigit() and
            int(user_input) >= min_length and
            int(user_input) <= max_length
        ):
            return int(user_input)

        print('Invalid input!')
        print('The password length should be'
             f'between {min_length} to {max_length}.'
              'Please try again.')



def get_user_password_settings(option, default):
    while True:
        user_input = input(f'Include {option}?'
                            '(Default is {default})'
                            '(y = True, n = False, enter = Default) ').lower()

        if user_input == '':
            return default

        if user_input in ['y', 'n']:
            return user_input == 'y'

        print('Invalid input!')
        print('Please enter y or n.')



def get_password_settings(settings_dict):

    for option, default in settings_dict.items():

        if option == 'password_length':
            user_choice = get_user_password_length(option, default)
            settings_dict[option] = user_choice
        else:
            user_password_length = get_user_password_settings(option, default)
            settings_dict[option] = user_password_length

    print(settings_dict)



def generate_upper_case_char():
    upper_case_char = string.ascii_uppercase
    return random.choice(upper_case_char)

def generate_lower_case_char():
    lower_case_char = string.ascii_lowercase
    return random.choice(lower_case_char)


def generate_digit():
    return random.choice(DIGITS)


def generate_symbol():
    return random.choice(SYMBOL)


def generate_bracket():
    return random.choice(BRACKET)



def generate_random_password(settings):

    password_settings = []
    generated_password = ''

    for key, value in settings.items():
        if value == True:
            password_settings.append(key)
    print(password_settings)

    if 'uppercase' in password_settings:
        generated_password += generate_upper_case_char()
    if 'lowercase' in password_settings:
        generated_password += generate_lower_case_char()
    if 'bracket' in password_settings:
        generated_password += generate_bracket()
    if 'symbol' in password_settings:
        generated_password += generate_symbol()
    if 'digit' in password_settings:
        generated_password += generate_digit()
    if 'space' in password_settings:
        generated_password += ' '
    if 'minus' in password_settings:
        generated_password += '-'
    if 'underline' in password_settings:
        generated_password += '_'


    print('*'*20)
    print(generated_password)
    print('*'*20)


def regenerate_random_password():

    while True:

        regenerate_password = input('Regenerate? (y:yes, n:no, enter:continue): ')

        if regenerate_password in ['y', 'n', '']:
            if regenerate_password in ['y', '']:
                generate_random_password(settings_dict)
            else:
                print('Thanks for choosing us.')
                break
        else:
            print('Invalid input. please enter y or n.')
            print('Please try again.')



def run():
    get_password_settings(settings_dict)
    generate_random_password(settings_dict)
    regenerate_random_password()



run()