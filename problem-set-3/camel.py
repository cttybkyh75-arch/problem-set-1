

def main():
    camel_case = input("camelCase: ")
    snake_case = ""
    for char in camel_case:
        if char.isupper():
            snake_case += "_" + char.lower()
        else:
            snake_case += char
    print("snake case:",snake_case)

main()