def convert(text):
    return text.replace(':)', '🙂').replace(':(', '🙁')

def main():
    text = input("enter text: ")
    print(convert(text))
main()

