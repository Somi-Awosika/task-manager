def print_git_message():
    """Print a message indicating Git's awesomeness."""
    print("Git is awesome!")

def get_user_name():
    """Prompt the user to enter their name."""
    return input("Enter your name: ")

def greet_user(user_name):
    """Greet the user with their name."""
    print("Hello,", user_name)

# Call functions to execute the program
if __name__ == "__main__":
    print_git_message()
    user_name = get_user_name()
    greet_user(user_name)

