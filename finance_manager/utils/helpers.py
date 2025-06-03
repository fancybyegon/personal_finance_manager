def input_float(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Invalid number.")
        return input_float(prompt)
