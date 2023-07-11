from git import Repo
import os
import smtplib

#the repository's url
repo_url = None  

readme_reponse = ''
license_response = ''

#path to the local directory
local_dir = None

#actual repository
repo = None 

#will be set to 1 if the user wants to clone the repository and 0 if they don't
repo_choice = None

"""Asks the user if they want to clone the repository to a file 
or use an existing file that contains the repository.
Keeps running if the user doesn't input either y or n
"""
while True:

    #asks the user if they want to clone the repository
    clone_or_not = input('Would you like to clone the repository to a local directory? (y/n): ')

    #if the user choses to clone the repository then they enter both url of repository and path to local directory and their choice is set to 1
    if clone_or_not.lower() == 'y':
        
        repo_url = input('Enter the url of your repository: ')

        local_dir = input('Enter the path to your local directory: ')

        repo_choice = 1

        break

    
    #if the user choses not to clone the repository then they just enter path to local directory and their choice is set to 0
    elif clone_or_not == 'n':

        local_dir = input('Enter the path to your local directory: ') 

        repo_choice = 0

        break

    print('Entered incorrect input. Try again and enter either y/n.') 

#checks to ensure that inputted local path exists
if os.path.exists(local_dir):

    print('Inputted a valid path to your local directory.')

#if inputted local path is invalid then the program will stop running      
else:

    print('Inputted an invalid path to your local directory.')

    exit(1)

#if user chose to clone repository 
if repo_choice == 1:

    repo = Repo.clone_from(repo_url, local_dir)

#if user chose not to clone repository
else:

    repo = Repo(local_dir)

try:

    #gets file that contains license from the repository 
    license = repo.working_tree_dir + "/LICENSE.TXT"

    with open(license, "r") as license_file:

        #license_lines contains the repository's license file
        license_response = license_file.read()


    

#deals with the issue of no license file in the repository 
except FileNotFoundError: 

    license_response = 'No License in the directory'


try:

    #gets readme file of the repository and stores it in readme variable
    readme = repo.working_tree_dir + "/README.md"

    with open(readme, "r") as readme_file:

        #stores all lines of readme file in readme_lines variable
        readme_response = readme_file.read()

    


#deals with the issue of no license file in the repository
except FileNotFoundError:

    readme_response = 'No README in the directory'

#email account that the email is sent from which will be my own email
gmail_user = 'andrew.thynne@insight-centre.org'

#Password to my gmail account
gmail_password = input('Enter password: ')

#input the sender of the email
sent_from = gmail_user

#asks the user to input their own email which is where the email will be sent to
gmail_receiver = input("Enter your email:")

to = [gmail_receiver]

#subject of the email
subject = 'Whats Up'

#body of the email
body = 'License: {0} and README: {1}'.format(license_response, readme_response)

#sets up the entie email
email_text = """\

From: %s

To: %s

Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    smtp_server.ehlo()

    smtp_server.login(gmail_user, gmail_password)

    smtp_server.sendmail(sent_from, to, email_text)

    smtp_server.close()

    print ("Email sent successfully!")

#what will happen if the email fails to send
except Exception as ex:

    print ("Something went wrong….",ex)
