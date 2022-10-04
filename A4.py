'''

Mukarram's Note-taking Program -- Allows users to create, save, and upload notes and posts.
- Features an online messaging functionality using public server
- Includes weather and music data from Web API's. Uses automatic keyword detection ("@weather", "@lastfm")
- Option to save files locally using .dsu format.

'''

# Mukarram A.
# A4.py

from pathlib import Path                                #imports pathlib library and functions from Profile/UI files, 
from profile import Profile
from profile import Post
from Ds_client import send
from OpenWeather import OpenWeather
from LastFM import LastFM

zipcode = None
profile = Profile()                                     #instantiates Profile class
post = Post()                                           #instantiates the Post class
lastfm1 = LastFM()
PORT = 3021

print("Enter 'C' to create a file")                     
print("Enter 'O' to load a file")
print("Enter 'Q' anytime to quit")
command = input("Select a command: ")
while command not in ['C', 'O', 'Q']:               
    command = input("Invalid input. Select a valid command: ")

if command == 'Q':                                      #quits program if Q is entered at the very beginning of the code
    exit()

file_path = input("Enter the file path: ")              #input for the file path, not including the filename.dsu portion
file_name = input("Enter the name of the file: ")       #asks for the name of the file, later appends '.dsu' to the end of the file


def run():
    '''
    Main program function
    Operates all different features of the program
    Allows user to use multiple features while the program runs
    Includes global variables
    
    '''
    global command
    global file_path
    global file_name
    global p
    global username
    global password
    global bio
    
    def return_format():
        '''
        Output an option menu to the user and run program after valid option is chosen
        Options are Edit, Print, and Quit

        '''
        print("-------------------------")
        print("Enter 'E' to edit a file")
        print("Enter 'P' to print data from a file")
        print("Enter 'Q' to quit the program")
        global command
        command = input("Select a new command: ")
        while command not in ['E', 'P', 'Q']:               #only excepts valid input and won't execute code until valid input is given
            command = input("Invalid input. Select a new command: ")
        run()                 

    def weather_format(post_param):
        '''
        Check function param for keyword and connect to OpenWeather API to transclude param
        Replaces keyword with current weather description for the zipcode
        return: transcluded parameter
        
        '''
        print('Keyword detected.')
        zipcode = input('Enter a US zipcode: ')
        openw = OpenWeather(zipcode)
        openw.set_apikey('d5c9b6d9426a12f20035ddbe1069f003')
        post_param = openw.transclude(post_param)
        return post_param


    def lastfm_format(post_param):
        '''
        Check function param for keyword and connect to LastFM API to transclude param
        Replaces keyword with top artist date
        return: transcluded parameter
        
        '''
        print('Keyword detected.')
        lastfm1.set_apikey('1212defc273ecfc3a7f141fa820d45fc')
        post_param = lastfm1.transclude(post_param)

        return post_param


    if command == 'Q':
        '''
        Quits the program
        
        '''
        exit()


    if command == 'C':
        '''
        Creates new file and asks for username, password, and bio
        If file path already exists, existing file will be opened instead

        '''
        p = Path(file_path) / f"{file_name}.dsu"                        #creates a file path to the dsu file

        if p.exists():
            print("File exists already.")
            profile.load_profile(p)
            print("File opened.")
            return_format()

        elif not p.exists():                                            #if the file path does not exist, create new dsu file
            username = input("Enter Username: ")                        #enter username (no whitespace)
            while ' ' in username:
                print("Username cannot contain whitespace")
                username = input("Enter Username: ")
            
            password = input("Enter Password: ")                        #enter password (no whitespace)
            while ' ' in password:
                print("Password cannot contain whitespace")
                password = input("Enter Password: ")

            bio = input("Enter Bio (brief description about yourself): ")   #asks for biography
            try:
                p.touch(exist_ok=True)
            except FileNotFoundError:
                print("Path does not exist.")
                file_path = input("Enter the file path: ")
                command == 'C'

            profile.username = username                                     #assigns the username, password, and bio to the method in the profile class in Profile.py
            profile.password = password
            profile.bio = bio
            profile.save_profile(p)                                         #saves the username, password, and bio to the method in the profile class in Profile.py
            return_format()
        

    if command == 'O':
        '''
        Loads a pre-existing file for editing information
        or outputting stored information.

        '''
        
        print("-------------------------")
        p = Path(file_path)
        p = p / f"{file_name}.dsu"
        profile.load_profile(p)
        print("File opened.")
        return_format()


    if command == 'E':
        '''
        Allows user to edit information stored in .dsu file
        
        Inlcudes editing username, password, bio, and posts

        '''
        
        print("-------------------------")
        print("Enter 'Username' if you want to edit the username")
        print("Enter 'Password' if you want to edit the password")
        print("Enter 'Bio' if you want to edit the Bio")
        print("Enter 'addpost' if you want to add a post")
        print("Enter 'delpost' if you want to delete a post")
        edit_input = input("Select an option: ")                       
        while edit_input not in ['Username', 'Password', 'Bio', 'addpost', 'delpost']:
            print('Invalid input. Try again.')
            edit_input = input("Select an option: ") 

        if 'Username' in edit_input:                                    
            profile.username = input("Enter your new username: ")
            print('Your new Username has been saved.')

        if 'Password' in edit_input:
            profile.password = input("Enter your new password: ")
            print('Your new Password has been saved.')
            
        if 'Bio' in edit_input:
            profile.bio = input("Enter your new bio: ")                       
            print('Your new Bio has been saved.')

        if 'addpost' in edit_input:
            print('Keywords are @weather and @lastfm')
            print()

            post_choice = input("Would you like to publish a post online? Enter Yes or No: ")       #asks the user if they want to create an online post
            while post_choice not in ['Yes', 'No']:
                print('Invalid input. Try again.')
                post_choice = input("Would you like to publish a post online? Enter Yes or No: ")

            if post_choice == 'Yes':
                online_post = input('Enter your new post: ')                                        #asks the user for input for the post they want to publish online
                if '@weather' in online_post:                                                       #checks for keyword and connects to OpenWeather API to replace keyword with API data
                    online_post = weather_format(online_post)
                if '@lastfm' in online_post:                                                        #checks for keyword and connects to LastFM API to replace keyword with API data
                    online_post = lastfm_format(online_post)

                send(profile.dsuserver, PORT, profile.username, profile.password, online_post, profile.bio)  #sends the post to the online server using the send() function
            
            elif post_choice == 'No':
                addpost = input("Enter the contents of the post: ")
                if '@weather' in addpost:                                                           #checks for keyword and connects to OpenWeather API to replace keyword with API data
                    addpost = weather_format(addpost)
                if '@lastfm' in addpost:                                                            #checks for keyword and connects to LastFM API to replace keyword with API data
                    addpost = lastfm_format(addpost)

                profile.add_post(Post(addpost))                                                     #asks the user for input for the post they would like to add and saves this input to the add_post method in the Profile class located in Profile.py
                print('Your new post has been saved.')

        if 'delpost' in edit_input:
            del_input = int(input("Enter the index of the post you would like to delete"))
            if type(del_input)==int:
                profile.del_post(del_input)
            print('The post has been deleted.')
            
        profile.save_profile(p)                                         #saves all the profile contents of the dsu file
        return_format()                                                 #returns the user to the main option menu with only the Print and Edit features since the file is in use


    if command == 'P':
        '''
        Prints a menu of options that shows what information 
        the user can print from the saved file
        
        User can print username, password, biography, post (by index),
        all posts, or all information stored
        
        '''
        
        print("-------------------------")
        print("Enter 'Username' if you would like to print your username")
        print("Enter 'Password' if you would like to print your password")
        print("Enter 'Bio' if you would like to print your Bio")
        print("Enter 'posts' if you would like to print all of your posts")
        print("Enter 'post' if you would like to print a specific post")
        print("Enter 'all' if you would like to print all of your information")
        print_input = input("Select an option: ")

        while print_input not in ['Username', 'Password', 'Bio', 'posts', 'post', 'all']:
            print('Invalid input. Try again.')
            print_input = input("Select an option: ") 

        if 'Username' in print_input:
            print(profile.username)
            return_format()
            
        if 'Password' in print_input:
            print(profile.password)
            return_format()
            
        if 'Bio' in print_input:
            print(profile.bio)
            return_format()

        if 'posts' in print_input:
            list1 = []
            x = profile.get_posts()
            print("Here are all of your posts:")
            print()
            for i in x:
                t = i['entry']                                          #filters the list of dictionaries so that only the post content is printed to the user
                list1.append(t)
            for i in list1:
                print(i)
    
            print()
            return_format()                                             #returns the user to the main option menu with only the Print and Edit features since the file is in use
            
        if 'post' in print_input:                                       #allows the user to print a specific post by using index
            def post_indexes():
                print_index = int(input("What is the index of the post you would like to print?: "))
                y = profile.get_posts()
                global d
                try:
                    d = y[print_index]
                except IndexError:
                    print('Index is out of range. ')
                    post_indexes()
            post_indexes()
            print(list(d.values())[0])                                  #filters the list of dictionaries for user-specified post index
            print()                                                     
            return_format()

        if 'all' in print_input:
            f = p.open()
            for i in f:
                print(i)
            f.close()
            print()
            return_format()

##########################################

run()                                                                   #after the program asks for the 3 intial inputs (file name, file path, comamnd), the program loop is initiatted with this line of code
