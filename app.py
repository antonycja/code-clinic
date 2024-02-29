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
from helpers import writer
from os.path import exists, join as save_path
from calendar_logic import booking, volunteer as volunteering, view_calendar as viewing_calendar
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

# groups the click command to the specific app
@click.group
def app():
    pass


# configuration
@click.command(help = ": reconfigures/resets the code-clinic application.")
@click.option('-n','--name',help = 'Your username; [USECASE: -n/--name "username"]')
@click.option('-e','--email',help = 'Your cooperate email address; [USECASE: -e/--email "email"]')
def configure(name: str = None,email: str = None):
    folders = setup.secure_folder()
    data = config.generate_logIn_cred(name,email)
    setup.encrypt_it(data,folders,'keys','creds','creds','recon','config','creds')
    cs = authentication.get_credentials()
    setup.encrypt_it(cs,folders,'keys','elite','cs','recon','cs','elite')


#login
@click.command()
def login():
    folders = setup.secure_folder()
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")
    LogIn.code_clinic_login(data)


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

    creds,user_data = gen_creds()
    signal, message = booking.book_slot(creds,booking_info,user_data['email'])

    exit(message)



@click.command(help = ': cancel a code clinic session')
@click.option('-d','--day',prompt = "Enter the date you want to cancel the booking",help="The date of the presently booked meeting that you wish to cancel; [USECASE: -d/--day 24]")
@click.option('-t','--time',prompt ='Enter the time of the session you wish to cancel',help = "The time of the currently planned meeting that you wish to cancel; [USECASE: -t/--time 08:30]")
def cancel_booking(day,time):

    user_input = f'{day}T{time}'
    date_time = booking.get_start_date_time(user_input)
    booking_info = {"dateTime": f"{date_time}"}

    creds,user_data = gen_creds()
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

    # just need to fix prompts, run through quill bot
    creds, user_data = gen_creds()
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

    creds, user_data = gen_creds()

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
@click.option('-f','--filtered',default = None, prompt= 'Enter the filter keywords ("," separated for multiple keywords)',help = "Display only the data that contains the filter keywords; [USECASE: -f/--filtered cpt,not booked,10:00]")

# TODO: Think about making creds and data a global variable 
def view_calendar(personal: bool,clinic: bool, days:str, filtered:str=None):
    creds, data = gen_creds()
    if personal == True and clinic == False: # Only personal is True
        calendar_id = 1
    elif clinic == True and personal == False: # Only clinic is True
        calendar_id = 2
    
    else: # If both of them are the same then just show both calendars
        calendar_id = 0
        
    viewing_calendar.get_calendar_results(creds, filtered, calendar_id, days)
        

app.add_command(configure)
app.add_command(make_booking)
app.add_command(cancel_booking)
app.add_command(volunteer)
app.add_command(cancel_volunteering)
app.add_command(view_calendar)
app.add_command(login)



if __name__ == '__main__':

    success, message = setup.pre_load()
    if 'configure' in sys.argv or '--help' in sys.argv or '-h' in sys.argv or len(sys.argv):
        app()
    elif success == False and not 'configure' in sys.argv:
        print(message)
        exit('Run: code-clinic configure')

    folders = setup.secure_folder()
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")
    if 'login' in sys.argv or LogIn.check_token("/tmp/.logIn_token.json",data):
        app()


### after math: 23 Feb 16:05