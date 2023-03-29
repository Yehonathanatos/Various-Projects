from datetime import datetime, date
import os

# gather the username and the password from the user
file = open('user.txt', 'r')
users = file.readlines()
file.close()

# Welcome message
print("Welcome to the Hyperion Task Management System!")

username = input("Enter your username: ")
password = input("Enter your password: ")

# open user.txt and store the usernames in a list, then close the file
usernames = []
passwords = []

for user in users:
    my_user = user.strip().split(", ")
    usernames.append(my_user[0])
    passwords.append(my_user[1])

# check to see if the entered username is in the usernames list, if it isn't re-enter
while username not in usernames:
    username = input("Error! Please re-enter your username: ")

# check if the entered password matches with the corresponding username
if password == passwords[usernames.index(username)]:
    print("Welcome, " + username + "!")
else:
    print("Incorrect password!")

# find the index of the usdername to compare it to the password
# when theentrerned name is the same as the username, save the index
index = ""
for position, name in enumerate(usernames):
    if name == username:
        index = position

while password != passwords[index]:
    password = input("Incorrect password! Please re-enter: ")

#Function to generate reports
def generate_reports():
    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.readlines()

    task_count = len(tasks)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    today = date.today()

    for task in tasks:
        task_data = task.strip().split(", ")
        if len(task_data) == 6:
            if task_data[5] == 'Yes':
                completed_tasks += 1
            else:
                uncompleted_tasks += 1
                due_date = datetime.strptime(task_data[4], "%d/%m/%Y").date()
                if due_date < today:
                    overdue_tasks += 1

    incomplete_percentage = (uncompleted_tasks / task_count) * 100
    overdue_percentage = (overdue_tasks / task_count) * 100

    with open('task_overview.txt', 'w') as task_overview_file:
        task_overview_file.write(f"Total number of tasks: {task_count}\n")
        task_overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n")

    user_task_counts = {}
    user_task_completed = {}

    for task in tasks:
        task_data = task.strip().split(", ")
        if len(task_data) == 6:
            username = task_data[0]
            completed = task_data[5] == 'Yes'

            if username not in user_task_counts:
                user_task_counts[username] = 0
                user_task_completed[username] = 0

            user_task_counts[username] += 1

            if completed:
                user_task_completed[username] += 1

    with open('user_overview.txt', 'w') as user_overview_file:
        user_overview_file.write(f"Total number of users: {len(usernames)}\n")
        user_overview_file.write(f"Total number of tasks: {task_count}\n")
        for username in user_task_counts:
            user_task_total = user_task_counts[username]
            user_task_complete = user_task_completed[username]
            user_task_incomplete = user_task_total - user_task_complete
            user_task_overdue = 0

            for task in tasks:
                task_data = task.strip().split(", ")
                if len(task_data) == 6 and task_data[0] == username and task_data[5] == 'No':
                    due_date = datetime.strptime(task_data[4], "%d/%m/%Y").date()
                    if due_date < today:
                        user_task_overdue += 1

            user_task_percentage = (user_task_total / task_count) * 100
            user_task_complete_percentage = (user_task_complete / user_task_total) * 100
            user_task_incomplete_percentage = (user_task_incomplete / user_task_total) * 100
            user_task_overdue_percentage = (user_task_overdue / user_task_total) * 100

            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Total tasks: {user_task_total}\n")
            user_overview_file.write(f"Percentage of total tasks: {user_task_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks completed: {user_task_complete_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks incomplete: {user_task_incomplete_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {user_task_overdue_percentage:.2f}%\n")

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    if username == 'admin':
        menu = input('''Select one of the following options:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - view my task
        gr - Generate reports
        ds - Display statistics
        e - Exit
        : ''').lower()
    else:
        menu = input('''Select one of the following options:
        a - Adding a task
        va - View all tasks
        vm - view my task
        e - Exit
        : ''').lower()

    # Add the new option 'gr' in the if-elif block
    if menu == 'gr' and username == 'admin':
        generate_reports()
        print("Reports generated successfully!")

    # Modify the 'ds' option to read data from the generated report files
    elif menu == 'ds' and username == 'admin':
        if not (os.path.isfile('task_overview.txt') and os.path.isfile('user_overview.txt')):
            generate_reports()

        with open('task_overview.txt', 'r') as task_overview_file:
            print("Task Overview:\n")
            print(task_overview_file.read())

        with open('user_overview.txt', 'r') as user_overview_file:
            print("User Overview:\n")
            print(user_overview_file.read())

    # if the user wants to register they have to use the admin name
    if menu == 'r' and username == 'admin':

        new_user = input("Enter the new username: ")
        new_pass = input("Enter the new password: ")
        confirm_password = input("Confirm your password: ")
        # the passwords will have to match the admin password which is sorted in the txt file
        while confirm_password != new_pass:
            print("Error! passwords don't match.")
            new_pass = input("Enter the new password: ")
            confirm_password = input("Confirm the new password: ")

        if new_pass == confirm_password:
            file = open('user.txt', 'a')
            file.write(f"\n{new_user}, {new_pass}")
            usernames.append(new_user)
            passwords.append(new_pass)
            file.close()

        with open('tasks.txt', 'r') as tasks_file:
            number_lines = len(tasks_file.readlines())

        print(f"The total number of tasks is:     {number_lines}")
        print(f"The total numbers of users is:    {len(usernames)}")
    # assign task to a user
    elif menu == 'a':

        user_task = input("Enter the username of the person whom the task is assigned to: ")
        title = input("Enter the title for this task: ")
        description = input("Enter a description of this task: ")
        due_date = input("Enter the due date of this task (dd/mm/yy): ")

        today = date.today()

        current_date = today.strftime("%d/%m/%Y")

        file = open('tasks.txt', 'a')
        file.write(f"\n{user_task}, {title}, {description}, {due_date}, {current_date}, No")
        file.close()


    # if user wants to view all task the option will come up to them
    elif menu == 'va':
        with open('tasks.txt', 'r') as file:
            for line in file:
                my_line = line.strip().split(", ")

                # Only print the task information if the line has all expected fields
                if len(my_line) == 6:
                    print(f"Task:           {my_line[1]}")
                    print(f"Assigned to:    {my_line[0]}")
                    print(f"Date assigned:  {my_line[3]}")
                    print(f"Due date:       {my_line[4]}")
                    print(f"Task complete?  {my_line[5]}")
                    print(f"Task Description:\n{my_line[2]}\n")
                else:
                    print(f"Error: Invalid line format: {line}")


    # if user wants to view all their own task the option will come upto them
    elif menu == 'vm':

        file = open('tasks.txt', 'r')
        for line in file:
            my_line = line.split(", ")
            if username == my_line[0]:
                print(f"Task:           {my_line[1]}")
                print(f"Assigned to:    {my_line[0]}")
                print(f"Date assigned:  {my_line[3]}")
                print(f"Due date:       {my_line[4]}")
                print(f"Task complete?  {my_line[5]}")
                print(f"Task Description:\n{my_line[2]}\n")
    # this will exit the program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")







