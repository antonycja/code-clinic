"""
This will be my main module. Using click to create the cli
"""

"""
This will be my main module. Using click to create the cli
"""

import click
from authentication import authentication, LogIn
from config import config
import setup
from file_handling import files
from helpers import writer
from os.path import exists, join as save_path
from calendar_logic import booking, volunteer as volunteering, view_calendar as viewing
import sys


def gen_creds(username):
    """
    Generates the Google credentials object via oauth2 authentication.
    The credentials (creds) is then used for viewing, creating and deleting events

    Returns:
        object: google object
    """

    folders = setup.secure_folder(username)
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")

    # custom user dir
    dir = folders["usertmp"]



    if LogIn.check_token(save_path(dir,".logIn_token.json"),data):

        if not exists(save_path(dir,".elite.json")):
            cs = setup.decrypt_it(folders,'keys','elite','cs','elite')
            writer.write_to_json(dir,'.elite',cs)

        if exists(save_path(folders['auth'],'.creds.token')):
            token = setup.decrypt_it(folders, "keys", "token", "creds", "token")
            writer.write_to_json(dir,".creds",token)
            write_token = False
        else:
            write_token = True

        # token authentication
        creds = authentication.authenticate(save_path(dir,".elite.json"),save_path(dir,".creds.json"))

        # writing an encrypted version of the token
        if write_token:
            with open(save_path(dir,'.creds.json'),'r') as file:
                enc_data = file.read()
            setup.encrypt_it(enc_data,folders,"keys","token","SOS","token","creds","token")

    return creds, data

def get_profile():
    """
    Checks whether the given username contains a profile in the system.
    If the user does have a profile and dir it will return the username.

    Returns:
        str: the username of the user
    """

    username = input("Enter your username: ")
    if files.check_user_profile(username):
        pass
    else:
        exit(f"profile '{username}' does not exists. run code-clinic configure")

    return username


def current_logged_profile():
    """
    Returns the profile that is currently/ previously logged-in on the system

    Returns:
        dict: current/previously logged in user if any.
    """

    path = save_path(files.get_home(),'.elite')

    return writer.load_pickle(path,'.systems.log')

# groups the click command to the specific app
@click.group
def app():
    pass


# configuration
@click.command(help = ": reconfigures/resets the code-clinic application.")
@click.option('-n','--name',help = 'Your username; [USECASE: -n/--name "username"]')
@click.option('-e','--email',help = 'Your cooperate email address; [USECASE: -e/--email "email"]')
def configure(name: str = None,email: str = None):
    data = config.generate_logIn_cred(name,email)
    folders = setup.secure_folder(data["username"])
    setup.encrypt_it(data,folders,'keys','creds','creds','recon','config','creds')
    cs = authentication.get_credentials()
    setup.encrypt_it(cs,folders,'keys','elite','cs','recon','cs','elite')


#login
@click.command(context_settings=dict(ignore_unknown_options=True,allow_extra_args = False))
def login(log_file = save_path(files.get_home(),'.elite','.systems.log')):

    log_data = dict()
    if exists(log_file):
        log_data = writer.load_pickle(save_path(files.get_home(),'.elite'),'.systems.log')
        if log_data["username"] == None:
            exit("""No active user found. Please login using

  code-clinic signin""")
        username = log_data["username"]

    else:
        username = get_profile()
        log_data["username"] = username


    folders = setup.secure_folder(log_data["username"])
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")
    # added folders to this function so we can know where to write the token to
    access = LogIn.code_clinic_login(data,folders)

    # saving the last signed in users
    if access:
        log_data["username"] = username
    else:
        log_data["username"] = None
    writer.capture_pickle(folders["main"],".systems","log",log_data)

@click.command(help=": Allows a new user to sign-in. Signs out the currently logged on user.")
@click.pass_context # allows me to invoke a click command without its decorations
def signin(ctx):

    # log_data = dict()
    username = get_profile()
    # if the user does have a folder in the system we write the username to log
    writer.capture_pickle(save_path(files.get_home(),'.elite'),".systems","log",{"username":f'{username}'})

    # then we call the login function o log them in
    ctx.invoke(login)


# booking
# add meeting area to the volunteer function and pass it as param
@click.command(help= ': schedule/book a code clinic session.')
@click.option('-d','--day',prompt = "Enter the date on which you would like to book",help="The date you would want to book the meeting; [USECASE: -d/--day 24]")
@click.option('-t','--time',prompt ="Enter the time of the session you want to reserve",help="When you want the session to take place; [USECASE: -t/--time 08:30]")
@click.option('-D','--desc',prompt = 'Provide a meeting summary.',help = 'A short summary that explains the purpose off the meeting; [USECASE: -D/--Desc "summary"]')
def make_booking(day,time,desc):

    "TODO: fix booking of an already booked session. Check if booker is allowed to cancel a session that a volunteer is in."

    user_input = f'{day}T{time}'
    date_time = booking.get_start_date_time(user_input)
    booking_info = {"dateTime": f"{date_time}","description" : f"{desc}"}

    username = current_logged_profile()["username"]
    creds,user_data = gen_creds(username)
    signal, message = booking.book_slot(creds,booking_info,user_data['email'])

    exit(message)


@click.command(help = ': cancel a code clinic session')
@click.option('-d','--day',prompt = "Enter the date you want to cancel the booking",help="The date of the presently booked meeting that you wish to cancel; [USECASE: -d/--day 24]")
@click.option('-t','--time',prompt ='Enter the time of the session you wish to cancel',help = "The time of the currently planned meeting that you wish to cancel; [USECASE: -t/--time 08:30]")
def cancel_booking(day,time):

    user_input = f'{day}T{time}'
    date_time = booking.get_start_date_time(user_input)
    booking_info = {"dateTime": f"{date_time}"}

    username = current_logged_profile()["username"]
    creds,user_data = gen_creds(username)
    signal, message = booking.cancel_booking(creds,booking_info,user_data['email'])
    exit(message)


# volunteering

@click.command(help = ': volunteer to host a code clinic session')
@click.option('-d','--day',prompt = 'Enter the date on which you would like to volunteer',help ='A date that you are available and able to help others; [USECASE: -d/--day 24]')
@click.option('-t','--time',prompt= 'Enter the time of the session you want to volunteer',help = "When you want the session to take place; [USECASE: -t/--time 08:30]")
@click.option('-c','--campus',prompt = 'Enter the name of the campus that you attend (optional)', help = 'The campus you attend, (CPT, JHB, DBN, CJC); [USECASE: -c/--campus CPT]')
def volunteer(day,time,campus):

    user_input = f'{day}T{time}'
    gen_end_time = volunteering.end_time(time)
    campus = volunteering.campus_abb(campus)

    start_time = booking.get_start_date_time(user_input)
    end_time = booking.get_start_date_time(f'{day}T{gen_end_time}')

    username = current_logged_profile()["username"]
    creds,user_data = gen_creds(username)
    message = volunteering.create_volunteer_slot(creds,user_data['email'],start_time,end_time,campus)
    exit(message)

# push this tomorrow first, added body for canceling
@click.command(help = ": cancel a code clinic session hosted by you. NB booked sessions can't be canceled.")
@click.option('-d','--day',prompt = 'Enter the date on which you would like to volunteer',help ='A date that you are available and able to help others; [USECASE: -d/--day 24]')
@click.option('-t','--time',prompt= 'Enter the time of the session you want to volunteer',help = "When you want the session to take place; [USECASE: -t/--time 08:30]")
def cancel_volunteering(day,time):

    user_input = f'{day}T{time}'
    gen_end_time = volunteering.end_time(time)

    start_time = booking.get_start_date_time(user_input)
    end_time = booking.get_start_date_time(f'{day}T{gen_end_time}')

    username = current_logged_profile()["username"]
    creds,user_data = gen_creds(username)

    message = volunteering.cancel_event(creds,start_time,end_time)
    exit(message)



# view calendar
''' TODO: fix the break if user does not have a token created
delete the token to find out'''

@click.command(help = ": displays the calenders")
@click.option('-p','--personal',default=False,help = "Display personal calendar only; [default = FALSE] [USECASE: -p True]")
@click.option('-c','--clinic',default = False, help = "Display code-clinic calendar only; [default = FALSE]  [USECASE: -c True]")

# Authored by Antony
@click.option('-d','--days', default = 7, prompt= 'Enter the number of days to view, leave empty for [default = 7 days]',help = "The number of days you would like to view from today [default = 7]; [USECASE: -d/--days 10]")
@click.option('-f','--filtered',default ="", prompt= 'Enter the filter keywords ("," separated for multiple keywords)',help = "Display only the data that contains the filter keywords; [USECASE: -f/--filtered cpt,not booked,10:00]")
def view_calendar(personal: bool,clinic: bool, days:str, filtered:str=""):

    username = current_logged_profile()["username"]
    creds,user_data = gen_creds(username)

    if personal == True and clinic == False: # Only personal is True
        calendar_id = 1
    elif clinic == True and personal == False: # Only clinic is True
        calendar_id = 2
    
    else: # If both of them are the same then just show both calendars
        calendar_id = 0
        
    viewing.get_calendar_results(creds, filtered, calendar_id, days)

@click.command(help= ": displays the current logged in user.")
def current_user():
    user = current_logged_profile()

    if user == None:
        exit("No user is currently logged-in")
    exit(f'The current logged-in user is: {user["username"]}')

app.add_command(configure)
app.add_command(make_booking)
app.add_command(cancel_booking)
app.add_command(volunteer)
app.add_command(cancel_volunteering)
app.add_command(view_calendar)
app.add_command(login)
app.add_command(signin)
app.add_command(current_user)



if __name__ == '__main__':

    usern = current_logged_profile()["username"]
    if usern == None and not 'signin' in sys.argv:
        exit("""No active user found. Please login using

  code-clinic signin""")

    if usern == None and 'signin' in sys.argv:
        # only if user name is none and user wants to signin 
        app()


    success, message, folders = setup.pre_load(usern)
    if 'configure' in sys.argv or '--help' in sys.argv or '-h' in sys.argv or len(sys.argv) < 2:
        app()
    elif success == False and not 'configure' in sys.argv:
        print(message)
        exit('Run: code-clinic configure')


    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")
    if 'login' in sys.argv or 'signin' in sys.argv or LogIn.check_token(save_path(folders["tmp"],f'.{usern}',".logIn_token.json"),data,folders):
        app()


### after math: 23 Feb 16:05