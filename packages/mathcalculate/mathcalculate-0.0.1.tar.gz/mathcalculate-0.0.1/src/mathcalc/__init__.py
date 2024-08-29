"""
Calculating using mathcalc:
If you want to calculate, use the Calculation function.
Example:
import mathcalc as mc

calc = mc.Calculation()

result = mc.add(5, 3)
mc.add(12, 87, print_result=True) # Adding print_result=True will print result automatically
"""

class Calculation:
    def add(self, num1, num2, print_result=False):
        result = num1 + num2
        if print_result:
            print(result)
        
        return result
    
    def subtract(self, num1, num2, print_result=False):
        result = num1 - num2
        if print_result:
            print(result)

        return result
    
    def multiply(self, num1, num2, print_result=False):
        result = num1 * num2
        if print_result:
            print(result)

        return result
    
    def divide(self, num1, num2, print_result=False):
        result = num1 / num2
        if print_result:
            print(result)

        return result
    
    def exponent(self, num1, num2, print_result=False):
        result = num1 ** num2
        if print_result:
            print(result)

        return result
    
    def modulo(self, num1, num2, print_result=False):
        result = num1 % num2
        if print_result:
            print(result)

        return result
    
    def floor_division(self, num1, num2, print_result=False):
        result = num1 % num2
        if print_result:
            print(result)

        return result
