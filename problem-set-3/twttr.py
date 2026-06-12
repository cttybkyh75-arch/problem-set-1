
text = input("Input: ")


result = ""


for vowel in text:
  
    if vowel.lower() not in ['a', 'e', 'i', 'o', 'u']:
        
        result += vowel 
print("Output:",result)