def main():
    greeting = input("Greeting: ")
    cleaned_greeting = greeting.strip().lower()
    if cleaned_greeting.startswith("hello"):
        print("$0")
    elif cleaned_greeting.startswith("h"):
        print("$20")
    else:
        print("$100")

main()

