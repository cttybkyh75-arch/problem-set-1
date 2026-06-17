
import random
import sys


def main():
    level = get_level()
    score = 0
    for _ in range(10):
        x = generate_integer(level)
        y = generate_integer(level)
        correct_answer = x + y
        
        tries = 0
        while tries < 3:
            try:
                user_answer = input(f"{x} + {y} = ")

                if int(user_answer) == correct_answer:
                    if tries == 0:
                     
                        score += 1
                    break
                else:
                    print("EEE")
                    tries += 1
            except ValueError:
  
                print("EEE")
                tries += 1
        

        if tries == 2:
            print(f"{x} + {y} = {correct_answer}")
            

    print(f"Score: {score}")


def get_level():
    while True:
        user_input = input("Level: ")
        if user_input in ["1", "2", "3"]:
            return int(user_input)


def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    elif level == 3:
        return random.randint(100, 999)
    else:
        raise ValueError("Invalid level")


if __name__ == "__main__":
    main()