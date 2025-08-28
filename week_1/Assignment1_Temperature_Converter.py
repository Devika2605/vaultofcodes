"""Assignment-1 
   Name : Devika N D
   emial id : devikashetty2716@gmail.com
   AICTE id : STU67fca08f8d7131744609423"""

def convert_temperature(temp, unit):
    """
    Convert temperature between Celsius and Fahrenheit.

    Parameters:
    temp (float): The temperature value to convert.
    unit (str): 'F' if input is in Fahrenheit, 'C' if input is in Celsius.

    Returns:
    float: The converted temperature rounded to 2 decimal places.
    """
    if unit.upper() == 'F':
        # Fahrenheit to Celsius
        converted = (temp - 32) * 5 / 9
    elif unit.upper() == 'C':
        # Celsius to Fahrenheit
        converted = (temp * 9 / 5) + 32
    else:
        raise ValueError("Invalid unit! Use 'F' for Fahrenheit or 'C' for Celsius.")

    return round(converted, 2)


# --- Example Usage ---
if __name__ == "__main__":
    print("Temperature Converter")
    print("---------------------")
    try:
        # Take user input
        temperature = float(input("Enter the temperature: "))
        unit = input("Enter the unit (F for Fahrenheit, C for Celsius): ")

        # Perform conversion
        result = convert_temperature(temperature, unit)

        # Display result
        if unit.upper() == 'F':
            print(f"{temperature}°F is equal to {result}°C")
        else:
            print(f"{temperature}°C is equal to {result}°F")

    except ValueError as e:
        print("Error:", e)