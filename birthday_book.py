'''
Nishka Shah                                   HW 9 - Birthday Book Manager                               3 April 2024

This program keeps track of birthdays in an automated birthday book, and allows for manipulation of the inputted birthdays 
through specified commands. The input could be either a command to add a birthday, to print the list of added birthdays,
to delete an added birthday, to search for an added birthday, to save the list of birthdays to a file, to load the saved
file, to ask for help, to turn echo on, or to turn echo off. The output is an action corresponding to the 
inputted command. 

'''
import os

# Here's one function for you. No reason for everyone to write this one.
def print_help(): 
    """This function can be used to print out the help message."""
    print("Allowed commands:")
    print("add firstName lastName month day year")
    print("list") 
    print("delete number")
    print("search name")
    print("save filename")
    print("load filename")
    print("help")
    print("echo on")
    print("echo off")

class BirthdayEntry:
    ''' This class holds a name (first and last) and date (month, day, year) for the birthday entry.'''
    def __init__(self, first_name, last_name, month, day, year):
        self.first_name = first_name
        self.last_name = last_name
        self.month = month
        self.day = day
        self.year = year

    def __str__(self):
        ''' This function formats the class'''
        return f"{self.first_name} {self.last_name}, {self.month}/{self.day}/{self.year}" 
    
class BirthdayBook:
    '''This class holds the birthday entries. Methods are called on this class.'''
    def __init__(self):
        ''' This holds the birthday entries list and the default setting of echo.'''
        self.birthday_entries = []
        self.echo = False
    
    def get_echo(self):
        '''Getter method checks if echo is on or off'''
        return self.echo
    
    def set_echo(self, state):
        ''' Setter method sets echo to either on or off'''
        self.echo = state

    def add_birthday(self, verified_input):
        '''Function converts input into birthday entry format and adds it to the birthday entries list.'''
        first_name = verified_input[1]
        last_name = verified_input[2]
        month = verified_input[3]
        day = verified_input[4]
        year = verified_input[5]
        bd = BirthdayEntry(first_name, last_name, month, day, year)
        self.birthday_entries.append(bd)
        print(f'Added "{bd}" to birthday book.')

    def print_list(self):
        ''' Function prints entries in the birthday entries list.'''
        if not self.birthday_entries:
            print("The birthday book is empty.")
        else:
            # The index is so the list is printed with corresponding numbers
            index = 1
            for bday in self.birthday_entries:
                print(f'{index}. {bday.first_name} {bday.last_name}, {bday.month}/{bday.day}/{bday.year}')
                index += 1 

    def delete_entry(self, verified_input):
        '''Function deletes an entry in the list.'''
        num_to_delete = int(verified_input[1])
        length_list = len(self.birthday_entries)
        # Ensures that number to delete exists in the list
        if num_to_delete > 0 and num_to_delete <= length_list:
            # Finds corresponding name to the delete number
            name_delete = self.birthday_entries[num_to_delete - 1]
            confirm = input(
                f'Really delete {name_delete.first_name + " " + name_delete.last_name} '
                f'from the birthday book? (y/n) ')
            # Prompts for input until user enters "y" or "n"
            while confirm not in ["n", "y" ]:
                confirm = input('Please enter "y" or "n" (y/n) ')
            if confirm == "y":
                self.birthday_entries.pop(num_to_delete - 1)
        else:
            print("I'm sorry, but there is no such entry in the book.")

    def search_name(self, verified_input):
        '''Function searches for a name in the list and outputs a birthday entry with that name.'''
        name = verified_input[1]
        # found tracks if a match has been found
        found = False
        # match ensures 'Entries with a name of "{name}"' only prints for the first match
        match = True
        # Loops through all entries in the birthday entries list to find a possible match
        for i in range (len(self.birthday_entries)):
            first_name = self.birthday_entries[i].first_name
            last_name = self.birthday_entries[i].last_name
            # First and last name in the birthday entries list are converted to lower case
            # as well as the name that is being searched, to allow for case insensitive comparison
            if first_name.lower() == name.lower() or last_name.lower() == name.lower():
                found = True
                if first_name.lower() == name.lower():
                    name_match = self.birthday_entries[i]
                    # Only runs for first match to print the "Entries..." message
                    if match:
                        print(f'Entries with a name of "{name}"')
                        print(f'   {name_match}')
                        match = False
                    else: 
                        print(f'   {name_match}')
                if last_name.lower() == name.lower():
                    name_match = self.birthday_entries[i]
                    if match:
                        print(f'Entries with a name of "{name}"')
                        print(f'   {name_match}')
                        match = False
                    else: 
                        print(f'   {name_match}')
        if not found:  
            print(f'I\'m sorry, but there are no entries with a name of "{name}".')


    def save_list(self, verified_entry):
        '''Function saves list to a file.'''
        file_name = verified_entry[1]
        # User specified file is opened
        with open (file_name,'w') as my_bday_book:
            # Each entry in the list is written on a new line in the file
            for entry in self.birthday_entries:
                my_bday_book.write(str(entry) + '\n')
            # Last line in the file has 'bd' written to it, to allow for a check in load_file
            my_bday_book.write('bd')
        print(f'Saved birthdays to "{file_name}".')
    
    def load_file(self, verified_entry):
        '''This function loads the saved file.'''
        file_name = verified_entry[1]
        # Checks if file exists
        file_exists = os.path.isfile(file_name)
        if file_exists:
            with open(file_name, 'r') as my_bday_book:
                file_entries = my_bday_book.read().splitlines()
                # Checks that the file that exists is the same as the file saved in this program
                # by checking that the last line is 'bd'
                if 'bd' in file_entries:
                    print(f"Birthdays in \"{file_name}\" added to birthday book.")
                    # The last line of 'bd' is removed after the check
                    file_entries.pop()

                    # Converting string entries in saved file to a list to allow for appending to list
                    for line in file_entries:
                        arr = line.split(' ')
                        date = arr[2].split('/')
                        entry = BirthdayEntry(arr[0], arr[1].removesuffix(','), date[0], date[1], date[2])
                        self.birthday_entries.append(entry)
                else:
                    print(f"I'm sorry, but \"{file_name}\" is not in the correct")
                    print("format. You can only load files saved by this same program.")
        else:
            print(f"I'm sorry, but \"{file_name}\" does not exist.")
        
        
def initial_input():
    ''' The initial input is collected, as well as input every time users enters in the terminal'''
    # Input is turned to a list
    user_input = input("> ").split()
    bday_book = BirthdayBook()
    # Loop asks for input until the user enters quit
    while True:
        bday_book = check_recognized_commands(bday_book, user_input)
        # Loop stops if user enters quit
        if user_input[0] == 'quit' and len(user_input) == 1:
            break
        user_input = input("> ").split()
        
            

def check_recognized_commands(bday_book, user_input):
    ''' Function checks if command has correct arguments and if the command is recognized.'''
    recognized_commands = ["add", "list", "delete", "search", "save", "load", "help", "quit", "echo"]

    # Stores the lengths of each input associated with the command
    command_lengths = {
        "add": 6,
        "list": 1,
        "delete": 2,
        "search": 2,
        "save": 2,
        "load": 2,
        "quit": 1,
        "help": 1,
        "echo": 2
    }
    # Checks if birthday book is on or off 
    if bday_book.get_echo():
        separator = ' '
        print(f'You entered: "{separator.join(user_input)}"')

    # Returns method that calls methods if user_input is valid
    if user_input[0] in recognized_commands and len(user_input) == command_lengths[user_input[0]]:
        return call_methods_and_int_check(bday_book, user_input)
    else:
        if user_input[0] not in recognized_commands:
            print("I am sorry, but that is not a recognized command, or")
            print("you have entered an incorrect number of arguments.")
            print("You may enter 'help' to see a list of commands.")
            return bday_book
        if len(user_input) != command_lengths[user_input[0]]:
            print("I am sorry, but that is not a recognized command, or")
            print("you have entered an incorrect number of arguments.")
            print("You may enter 'help' to see a list of commands.")
            return bday_book
    
    

def call_methods_and_int_check(bday_book, verified_input):
    '''Function calls methods that are written in the Birthday Book class, and checks for valid user input.'''
    # Runs if user input is not quit
    if verified_input[0] != "quit":

        if verified_input[0] == "add":
            # Throws value error if an integer is not entered and returns same value that is passed
            # to ask for input again and check if it is a recognized command.
            try:
                int(verified_input[3])
                int(verified_input[4])
                int(verified_input[5])
                bday_book.add_birthday(verified_input)
            except ValueError:
                print("Error: Unable to add birthday to book. Please use integers for dates.")
                return bday_book
            
        # Calls print list method 
        if verified_input[0] == "list":
            bday_book.print_list()

        # Calls delete entry method 
        if verified_input[0] == "delete":
            # Throws value error if a non-integer is entered and returns same value that is passed
            # to ask for input again and check if it is a recognized command.
            try:
                int(verified_input[1])
                bday_book.delete_entry(verified_input)
            except ValueError:
                print("Error: Please specify the item to delete using an integer.")
                return bday_book

        # Calls search name method
        if verified_input[0] == "search":
            bday_book.search_name(verified_input)
        
        # Calls save list method
        if verified_input[0] == "save":
            bday_book.save_list(verified_input)

        # Calls load file method
        if verified_input[0] == "load":
            bday_book.load_file(verified_input)
        
        # Calls print help method
        if verified_input[0] == "help":
            print_help()

    
        if verified_input[0] == "echo":
            # If echo on entered, the echo in the setter method is set to true
            if verified_input[1] == "on":
                bday_book.set_echo(True)
                print('Echo turned on.')
            elif verified_input[1] == "off":
            # If echo off is entered, the echo in the setter method is set to false
                print('Echo turned off.')
                bday_book.set_echo(False)
            else:
                print("I am sorry, but that is not a recognized command, or")
                print("you have entered an incorrect number of arguments.")
                print("You may enter 'help' to see a list of commands.")

    return bday_book


def main():
    print("Welcome to the Birthday Book Manager")
    initial_input()

    """The main function of the Birthday Book program."""


# Do not modify the code below.  Write all of your code above.
if __name__ == "__main__":
    main()