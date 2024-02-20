"""
This will be my main module. Using click to create the cli
"""

import click
from authentication import authentication, LogIn
from config import config
from file_handling import files
import setup
from getpass import getpass
from authentication.LogIn import sys_time
import re
from helpers import writer
from os.path import exists, join as save_path
from calendar_logic import booking


# validate if the user is in the organization
# mine
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

        if not exists("/tmp/elite.json"):
            cs = setup.decrypt_it(folders,'keys','elite','cs','elite')
            writer.write_to_json("/tmp",'elite',cs)

        if exists(save_path(folders['auth'],'.creds.token')):
            token = setup.decrypt_it(folders, "keys", "token", "creds", "token")
            writer.write_to_json("/tmp","creds",token)
            write_token = False
        else:
            write_token = True

        # token authentication
        creds = authentication.authenticate("/tmp/elite.json","/tmp/creds.json")

        # writing an encrypted version of the token
        if write_token:
            with open('/tmp/creds.json','r') as file:
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
@click.command(help= ': schedule a code clinic session.')
@click.option('-d','--day',prompt = "Enter the date on which you would like to book",help="The date you would want to book the meeting; [USECASE: -d/--day 24]")
@click.option('-t','--time',prompt ="Enter the time of the session you want to reserve",help = "When you want the session to take place; [USECASE: -t/--time 08:30]")
@click.option('-D','--desc',prompt = 'Provide a meeting summary',help = 'A short summary that explains the purpose off the meeting; [USECASE: -D/--Desc "summary"]')
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
    # I want to first run the preload and check to make sure that all the files are in place

    # I also want to run the click app, this is troubling because we cant combine the too
    # if I can not sort it, I will need ot run the cli in TR style
    # It will work and I will have more control but It will be more complex to write

    # now we can design the booking system using click
    # but then that means I will have to desert many functions

    # These includes the token function, unless I call all these functions in each app function
    # So we can call each individual function such as the checking of the token and cs in each function
    # that then builds redundancy, which is what we are avoiding

    # so either we build the cli manually and handle each flag and each arg s manually or use click 

    # Manual: Pro
    # better control on how the app runs
    # fluidity I guess, and less redundant code
    # an understanding structure to a certain extent
    
    # Manual: Cons
    # Help function, gotta make it myself
    # argument handling,I will have to handle that too
    
    # Click: Pro
    # It will handle the arguments being passed, thats a bonus
    # I do not need to control the flow of commands
    # 

    # Click: Cons
    # no control over code flow
    # can gotta discard many functions




#    if 'configure' in sys.argv or setup.pre_load() == True:
#         app()
#    else:
    #    print('blue')
    app()
    # make_booking()

