# task_manager.py
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# Importing libraries
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# Login Section
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def reg_user():
    '''Add a new user to the user.txt file'''

    # Request input of a new username
    new_username = input("New Username: ")

    # Check if the username already exists in user.txt
    if new_username in username_password.keys():
        print("Error: Username already exists. Please try again.")
        return

    # Request input of a new password
    new_password = input("New Password: ")

    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")

    # Otherwise, present a relevant message.
    else:
        print("Passwords do not match")


def generate_reports():
    '''Generate reports and write them to task_overview.txt and user_overview.txt'''

    # Perform necessary calculations to generate reports
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.now())
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    with open("task_overview.txt", "w") as task_report_file:
        task_report_file.write("Task Overview Report\n")
        task_report_file.write(f"Total Tasks: {total_tasks}\n")
        task_report_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_report_file.write(f"Incomplete Tasks: {incomplete_tasks}\n")
        task_report_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_report_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
        task_report_file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")

    num_users = len(username_password)
    total_tasks_assigned = len([task for task in task_list if task['username'] == curr_user])
    completed_tasks_assigned = len([task for task in task_list if task['username'] == curr_user and task['completed']])
    incomplete_tasks_assigned = total_tasks_assigned - completed_tasks_assigned
    overdue_tasks_assigned = len([task for task in task_list if task['username'] == curr_user and not task['completed'] and task['due_date'] < datetime.now()])
    incomplete_percentage_assigned = (incomplete_tasks_assigned / total_tasks_assigned) * 100
    overdue_percentage_assigned = (overdue_tasks_assigned / total_tasks_assigned) * 100

    with open("user_overview.txt", "w") as user_report_file:
        user_report_file.write("User Overview Report\n")
        user_report_file.write(f"Total Users: {num_users}\n")
        user_report_file.write(f"Total Tasks: {total_tasks}\n")
        user_report_file.write(f"Tasks Assigned to Me: {total_tasks_assigned}\n")
        user_report_file.write(f"Percentage of My Tasks: {(total_tasks_assigned / total_tasks) * 100:.2f}%\n")
        user_report_file.write(f"Percentage of My Completed Tasks: {(completed_tasks_assigned / total_tasks_assigned) * 100:.2f}%\n")
        user_report_file.write(f"Percentage of My Incomplete Tasks: {incomplete_percentage_assigned:.2f}%\n")
        user_report_file.write(f"Percentage of My Overdue Tasks: {overdue_percentage_assigned:.2f}%\n")


def add_task():
    '''Allow a user to add a new task to tasks.txt file'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Ensure due date input is in the correct format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current date
    curr_date = date.today()

    # Create the new task dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add the new task to the task list
    task_list.append(new_task)

    # Write the updated task list to tasks.txt file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print("Task successfully added.")


def view_mine():
    '''Reads the tasks from tasks.txt file and prints to the console only the tasks assigned to the current user'''
    for index, task in enumerate(task_list):
        if task['username'] == curr_user:
            print(f"\nTask {index + 1}:")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
 
 #Allow the user to select a task or return to the main menu
   
    while True:
        try:
            choice = int(input("Enter the number of the task to mark as complete or edit (enter -1 to return to the main menu): "))
            if choice == -1:
                return  # Return to the main menu
            elif choice < 1 or choice > len(task_list):
                print("Invalid task number. Please enter a valid number.")
                continue
            else:
                selected_task = task_list[choice - 1]
                task_completed = selected_task['completed']
                if not task_completed:
                    action = input("Do you want to mark this task as complete (C) or edit it (E)? ").lower()
                    if action == 'c':
                        selected_task['completed'] = True
                        print("Task marked as complete.")
                    elif action == 'e':
                        new_username = input("Enter the new username for the task: ")
                        new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
                        selected_task['username'] = new_username
                        selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        print("Task edited successfully.")
                    else:
                        print("Invalid choice. Please enter 'C' to mark as complete or 'E' to edit.")
                else:
                    print("This task is already completed and cannot be edited.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")

def view_all():
    '''Reads the tasks from tasks.txt file and prints to the console all the tasks'''
    for index, task in enumerate(task_list):
        print(f"\nTask {index + 1}:")
        print(f"Assigned to: {task['username']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed: {'Yes' if task['completed'] else 'No'}")


# Update the main menu to include the option to generate reports
while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
        print("Reports generated successfully.")
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")
