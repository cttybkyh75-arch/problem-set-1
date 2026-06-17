
import random
import sys

def main():
    while True:
        level_input = input("Level: ")
        if is_positive_integer(level_input):
            n = int(level_input)
            break
    target_number = random.randint(1, n)
    while True:
        guess_input = input("Guess: ")
        if not is_positive_integer(guess_input):
            continue
            
        guess = int(guess_input)
        if guess < target_number:
            print("Too small!")
        elif guess > target_number:
            print("Too large!")
        else:
            print("Just right!")
            sys.exit()


def is_positive_integer(value):
    if value.isdigit() and int(value) > 0:
        return True
    return False



main()