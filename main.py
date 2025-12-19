def check_content(sequance, password):
    includes = False
    for s in sequance:
        if s in password:
            includes = True
    return includes


def check_password(password):
    message = ""
    symbols = "!@#$%^&*()"
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "1234567890"

    if len(password) < 8:
        message += "Password must be at least 8 characters long. \n"

    if not check_content(symbols, password):
        message += "Password must include at least one special character: " + symbols + "\n"
    if not check_content(letters, password):
        message += "Password must include at least one of these letters: " + letters + "\n"
    if not check_content(digits, password):
        message += "Password must include at least one of these numbers: " + digits + "\n"

    print(message )
        


res = check_password("*234567b")