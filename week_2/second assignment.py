# Basic Calculator with Error Handling
def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
def power(a, b):
    return a ** b
def calculator():
    while True:
        print("\\n----- Basic Calculator -----")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Power (Bonus)")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        if choice == '6':
            print("Exiting the calculator. Goodbye!")
            break
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Error: Please enter valid numeric values.")
            continue
        if choice == '1':
            print("Result:", add(num1, num2))
        elif choice == '2':
            print("Result:", subtract(num1, num2))
        elif choice == '3':
            print("Result:", multiply(num1, num2))
        elif choice == '4':
            print("Result:", divide(num1, num2))
        elif choice == '5':
            print("Result:", power(num1, num2))
        else:
            print("Invalid choice. Please choose a valid option.")
if __name__ == "__main__":
    calculator()