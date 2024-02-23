"""
This will be my main module. Using click to create the cli
"""

"""
This will be my main module. Using click to create the cli
"""

import click
from authentication import authentication, LogIn
from config import config
from file_handling import files
import setup
from helpers import writer
from os.path import exists, join as save_path
from calender_logic import booking
import sys


# pusg this code: added a dot(.),to make files hidden
def gen_creds():
    """
    Generates the Google credentials object via oauth2 authentication.
    The credentials (creds) is then used for viewing, creating and deleting events

    Returns:
        object: google object
    """

    folders = setup.secure_folder()
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")

    if LogIn.check_token("/tmp/.logIn_token.json",data):

        if not exists("/tmp/.elite.json"):
            cs = setup.decrypt_it(folders,'keys','elite','cs','elite')
            writer.write_to_json("/tmp",'.elite',cs)

        if exists(save_path(folders['auth'],'.creds.token')):
            token = setup.decrypt_it(folders, "keys", "token", "creds", "token")
            writer.write_to_json("/tmp",".creds",token)
            write_token = False
        else:
            write_token = True

        # token authentication
        creds = authentication.authenticate("/tmp/.elite.json","/tmp/.creds.json")

        # writing an encrypted version of the token
        if write_token:
            with open('/tmp/.creds.json','r') as file:
                data = file.read()
            setup.encrypt_it(data,folders,"keys","token","SOS","token","creds","token")

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
    setup.encrypt_it(cs,folders,'keys','elite','SOS','recon','cs','elite')


#login
@click.command()
def login():
    folders = setup.secure_folder()
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")
    LogIn.code_clinic_login(data)


# booking
# add meeting area to the volunteer function and pass it as param
@click.command(help= ': schedule a code clinic session.')
@click.option('-d','--day',prompt = "Enter the date on which you would like to book",help="The date you would want to book the meeting; [USECASE: -d/--day 24]")
@click.option('-t','--time',prompt ="Enter the time of the session you want to reserve",help="When you want the session to take place; [USECASE: -t/--time 08:30]")
@click.option('-D','--Desc',prompt = 'Provide a meeting summary.',help = 'A short summary that explains the purpose off the meeting; [USECASE: -D/--Desc "summary"]')
def make_booking(day,time,desc):

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

@click.command()
def volunteer():
    print('vol')
    pass


# view calendar

@click.command(help = "Displays the calenders")
@click.option('-p','--personal',default=False,help = "Display personal calendar only; [default = FALSE] [USECASE: -p True]")
@click.option('-c','--clinic',default = False, help = "Display code-clinic calendar only; [default = FALSE]  [USECASE: -c True]")
def view_calendar(personal: bool,clinic: bool):

    if personal == True:
        print("pass")
    if clinic == True:
        print("cc")
    else:
        print("show all")


    pass

app.add_command(configure)
app.add_command(make_booking)
app.add_command(cancel_booking)
app.add_command(volunteer)
app.add_command(view_calendar)
app.add_command(login)



if __name__ == '__main__':

    success, message = setup.pre_load()
    if success == False and not 'configure' in sys.argv:
        print(message)
        exit('Run: code-clinic configure')
    elif 'configure' in sys.argv or '--help' in sys.argv or '-h' in sys.argv:
        app()

    folders = setup.secure_folder()
    data = setup.decrypt_it(folders, "keys", "creds", "config", "creds")
    if 'login' in sys.argv or LogIn.check_token("/tmp/.logIn_token.json",data):
        app()


