## Created by Jarod L. Cunningham

#\TODO
"""
Add the modular option to choose what to convert:
- Binary
- Decimal
- Hexadecimal 

#/
"""
print("Input a Binary number to convert to decimal")
binary_str = input()
decimal = int(binary_str, 2)
hex = hex(int(binary_str, 2))
print(f"Binary: {binary_str}\nDecimal: {decimal}\nHex: {hex}")