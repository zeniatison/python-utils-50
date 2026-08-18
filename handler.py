import sys
import json

class InputValidator:
    @staticmethod
    def validate_choice(choice, valid_choices):
        if choice not in valid_choices:
            raise ValueError(f"Invalid choice: {choice}. Valid options are: {valid_choices}")

def main_loop():
    valid_choices = ['start', 'stop', 'exit']
    print('Welcome to the game! Type your command:')
    while True:
        user_input = input('> ').strip().lower()
        try:
            InputValidator.validate_choice(user_input, valid_choices)
            if user_input == 'start':
                print('Game is starting...')
            elif user_input == 'stop':
                print('Game has been stopped.')
            elif user_input == 'exit':
                print('Exiting game. Goodbye!')
                break
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main_loop()