def  multiplication_table(start: int = 1 , end: int = 5) -> None:
    for i in range(start,end+1):
        print(f'multiplication_table for {i} ↓')
        print()
        for j in range(1,11):
            print(f'{i}*{j} : {i*j}')
        print()

def fahrenheit_to_celsius(fahrenheit_temperatures : int) -> str:
    celsius = (fahrenheit_temperatures - 32) * 5 / 9
    return f'Fahrenheit {fahrenheit_temperatures} -> Celsius : {celsius:.2f}'

def celsius_to_fahrenheit(celsius : int) -> str:
    fahrenheit = (celsius * 9/5) + 32
    return f'Celsius {celsius} -> fahrenheit : {fahrenheit:.2f}'

def finds_the_longest_word(sentence: str) -> str:
    longest_word = [word for word in sentence.split() if len(word) == len(max(sentence.split(),key=len))][0]
    return f'The longest word is : {longest_word}'

def _main(num : int) -> int | str:
    if num < 0:
        return "Please enter a positive binary number."
    else:
        boolean : bool = any(char in "23456789" for char in str(num))
        if boolean :
            return "Invalid binary number. Only 0 and 1 are allowed."
        else:
            last_digit : int = 0
            binary : int = 0
            power : int = 0
            while num != 0:
                last_digit = num%10
                binary = binary + (last_digit * 2 ** power)
                num = num//10
                power+=1
            return binary

def binary_to_decimal() -> None:
        binary_number : int = int(input("Enter the Binary Number : "))
        result : int = _main(binary_number) #type:ignore
        if isinstance(result, str):  # Check if the result is a message
            print(result)
        else:
            print(f"The decimal of {binary_number} is {result}")
