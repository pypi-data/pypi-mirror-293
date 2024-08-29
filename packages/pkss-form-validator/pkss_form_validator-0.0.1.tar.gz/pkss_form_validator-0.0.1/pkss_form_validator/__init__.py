import re

def validate_name(name):
    # Check if the name is empty or only whitespace
    if not name.strip():
        return False, "Name cannot be empty or just spaces."

    # Check the length of the name
    if len(name) < 2 or len(name) > 50:
        return False, "Name must be between 2 and 50 characters long."

    # Check if the name contains only allowed characters (letters, spaces, dots)
    if not re.match("^[A-Za-z\s.]+$", name):
        return False, "Name can only contain alphabetic characters, spaces, and dots."

    # Check for leading or trailing spaces
    if name != name.strip():
        return False, "Name cannot have leading or trailing spaces."

    return True, "Name is valid."

def validate_email(email):
    # Check if the email matches a standard pattern
    if not re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", email):
        return False, "Invalid email format."
    
    return True, "Email is valid."

def validate_phone(phone):
    # Check if the phone number is valid (10-15 digits, optional '+' prefix, and spaces allowed)
    if not re.match(r"^\+?\d[\d\s]{9,14}$", phone):
        return False, "Invalid phone number format. It should contain 10-15 digits, and can include spaces."

    return True, "Phone number is valid."

def validate_password(password):
    # Check if the password is strong (at least 8 characters, including letters, numbers, and special characters)
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, "Password is valid."

def validate_address(value):
    # Check if the input is empty
    if value == "" or value is None:
        return False, "Address cannot be empty."

    # Regular expression to match valid address characters (letters, numbers, spaces, commas, periods, hyphens, and apostrophes)
    if not re.match(r"^[A-Za-z0-9\s,.\'-]+$", value):
        return False, "Invalid address. Only letters, numbers, spaces, commas, periods, hyphens, and apostrophes are allowed."

    # Check if the length is within the specified range
    if len(value) < 10:
        return False, "Address must be at least 10 characters long."

    if len(value) > 200:
        return False, "Address must be no more than 200 characters long."

    return True, "Address is valid."

def validate_integer(value, min_value=None, max_value=None, allow_negative=True):
    # Check if the input can be converted to an integer
    try:
        int_value = int(value)
    except ValueError:
        return False, "Invalid input. Please enter a valid integer."
    
    return True, "Integer is valid."

def validate_string(value, min_length=None, max_length=None, allow_empty=False):
    # Check if the input is a string
    if not isinstance(value, str):
        return False, "Invalid input. Please enter a valid string."

    # Check for empty strings if not allowed
    if not allow_empty and not value.strip():
        return False, "String cannot be empty."
    
    return True, "String is valid."