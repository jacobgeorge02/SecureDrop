import sys
import getpass
import json
from cmd import Cmd 
from cryptography.fernet import Fernet
import socket
import threading
import os

#global variable for onlineUsers
onlineUsers = []

# User and contact class for json file
class Contact: 
  def __init__(self):
    self.object = {}
class User:
  def __init__(self):
    self.object = {}
    self.list_of_contacts = {}

# Encrypt function for security purposes
def encrypt():
    # opening the key
  with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

  # using the generated key
  fernet = Fernet(key)

  # opening the original file to encrypt
  with open('database.json', 'rb') as file:
    original = file.read()
    
  # encrypting the file
  encrypted = fernet.encrypt(original)

  # opening the file in write mode and
  # writing the encrypted data
  with open('database.json', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
    
# MyPrompt will run on loop depending on user input, simulating a command-line tool
# Responsible for all main functions in login()
class MyPrompt(Cmd):
  prompt = "secure_drop> "
  intro = "Welcome to SecureDrop.\nType \"help\" For Commands. \n"
  # file_in = open("database.json", "r")
  # list_of_users = json.load(file_in) 
  def do_help(self, inp):
    print("   \"add\" -> Add a new contact")
    print("   \"list\" -> List all online contacts")
    print("   \"send\" ->Transfer file to contact")
    print("   \"exit\" -> Exit SecureDrop\n")

  # When the user logs out, database.json should encrypt to hide all sensitive information
  def do_exit(self, inp):
    encrypt()
    return True
  
  # Function executed when logged in user uses 'add' command
  def do_add(self, inp):
    file_in = open("database.json", "r")
    list_of_users = json.load(file_in) 
    fullname = input("   Enter Full Name: ")
    email = input("   Enter Email Address: ")
    # add contact
    contact1 = Contact()
    contact1.object["contactname"] = fullname
    contact1.object["contactemail"] = email
    # Appending a contact object into a list
    contactList = []
    for i in list_of_users:
      if i["email"] == userEmail:
        if "contact" in i:
          existingContact = False
          for j in i["contact"]:
            if j["contactemail"] == contact1.object["contactemail"]:
              j["contactname"] = contact1.object["contactname"]
              existingContact = True
              break
          if (existingContact == False):
            contactList.append(contact1.object)
            contactList.extend(i["contact"])
            i["contact"] = contactList
        else:
          contactList.append(contact1.object)
          i["contact"] = contactList
  
    whole_list = []
    whole_list.extend(list_of_users)
    file_in.close()
    file_in = open("database.json", "w")
    json.dump(whole_list, file_in)
    print("   Contact Added.")
    file_in.close()
    
  # Function executed when logged in user uses 'list' command
  def do_list(self, inp):
    # Iterate through the list of contacts and if they are online, print
    contactsExist = False
    file_in = open("database.json", "r")
    database = json.load(file_in)
    print("The following contacts are online: ")
    for i in database:
      if (i["email"] == currentEmail):
        if "contact" in i:
          list_of_contacts = i["contact"]
          contactsExist = True
          break
    if contactsExist == True:
      # Iterate through the list of contacts
      for contact in list_of_contacts:
        contact_email = contact["contactemail"]
        # Check that contactemail exists in database
        for j in database:
          # If Bob exists, go into Bob's contacts list and check if currentEmail exists
          if (j["email"] == contact_email):
            if "contact" in j:
              secondary_list_of_contacts = j["contact"]
              for k in secondary_list_of_contacts:
                  if k["contactemail"] == currentEmail:
                  # Because contacts match, check if user is online
                    # This function call will check if each matching user is online
                    checkUserOnline(j["email"], contact["contactname"])
    file_in.close()

    # Function executed when logged in user uses 'send' command
  def do_send(self,inp):
    hostIP = "127.0.0.1"
    file_in = open("database.json", "r")
    database = json.load(file_in)
    fileName = input("Name of the file you want to transfer: ")
    emailContact = input("Email you want to send file to: ")
    
    here = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(here, fileName)
    file_name = "/home/runner/SecureDrop-backup/Test.txt"
    filesize = os.path.getsize(file_name)
    existingContact = False
    for k in onlineUsers:
      if (emailContact == k["email"]):
        for i in database:
          if i["email"] == userEmail:
            if "contact" in i:
              for j in i["contact"]:
                if j["contactemail"] == k["email"]:
                  existingContact = True
    if (existingContact == False):
      print("Contact not available")
      return

  #IP to use: 127.0.0.1
  #create a TCP socket
    s = socket.socket()
    print(f"[+] Attempting to Connect to {hostIP}:{userPort}")
    s.connect((hostIP, userPort))
    print("Connection Successful")
    #sending File Name to server
    s.send(f"{file_name}{filesize}".encode())
    
    #read the file byte by byte to be sent to the server
    with open(file_name, "rb") as f:
      while True:
        # read the bytes from the file
        bytes_read = f.read(4096)
        if not bytes_read:
            # file transmitting is done
            break
        
        #use of sendall to assure file gets transferred throughout busy networks
        s.sendall(bytes_read)
        #close the socket
        s.close()

  # Lets user know input is invalid 
  def default(self, inp):
    if inp != "list" and inp != "send" and inp != "add" and inp != "exit":
      print("Invalid input")

#decrypt json file so it can be accessed by code
def decrypt():
   # opening the key
  with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
    # using the key
  fernet = Fernet(key)
    
  # opening the encrypted file
  with open('database.json', 'rb') as enc_file:
      encrypted = enc_file.read()
    
  # decrypting the file
  decrypted = fernet.decrypt(encrypted)
    
  # opening the file in write mode and
  # writing the decrypted data
  with open('database.json', 'wb') as dec_file:
      dec_file.write(decrypted)


  
# 'First' lines of code run at beginning of program
# Decrypts json file if it has been encrypted
user1 = User()
whole_list = []
lastRegistered = ""
isLastRegistered = False
file_in = open("database.json", "r")
data = file_in.read()
try:
  is_json = json.loads(data)
except:
	# else, not a json file
  decrypt()
  file_in = open("database.json", "r")
  list_of_users = json.load(file_in)
file_in = open("database.json", "r")
list_of_users = json.load(file_in)
userEmail = ""

# Helper function for login() to test credentials
def lookup(database, username, password):
  for i in database:
    if (i["email"] == username and i["password"] == password):
      return True
  return False
  # return True if database["username"] == password else False

# Helper function for creating a user that checks if created passwords match
def check_password(password1, password2):
  if password1 == password2:
      print("Passwords Match.")
  else:
    passwordsMatch = False
    while passwordsMatch == False:
      print("Passwords do not match.")
      password1 = getpass.getpass(prompt = "Enter Password: ")
      password2 = getpass.getpass(prompt = "Re-Enter Password: ")
      if password1 == password2:
        print("\nPasswords Match.")
        passwordsMatch = True
  return password1
      
# Creates a new user to the database if json file is empty or if email is unrecognized
def create_user(fullname, email, password):
  user1 = User()
  user1.object["fullname"] = fullname
  user1.object["email"] = email
  user1.object["password"] = password
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 0))
  user1.object["port"] = s.getsockname()[1]
  file_in = open("database.json", "r")
  whole_list.append(user1.object)
  list_of_users = json.load(file_in)
  whole_list.extend(list_of_users)
  file_in.close()
  file_in = open("database.json", "w")
  json.dump(whole_list, file_in)
  global lastRegistered
  lastRegistered = email
  file_in.close()
  print("User Registered.")

# Run at start of program if json file isnt empty
# If email address unrecognized will suggest new user to be created
# Runs shell upon successful login
def login():
  email = input("Enter Email Address: ")
  # Valide that email address exists in the database
  userExists = False
  file_in = open("database.json", "r")
  list_of_users = json.load(file_in)  
  for i in list_of_users:
    if i["email"] == email:
      userExists = True
      userEmail = i["email"]
      # Set global variables for current user
      global currentEmail
      currentEmail = userEmail
      global userIP
      userIP = "127.0.0.1"
      global userPort
      break
  if userExists == True:
    password = getpass.getpass(prompt = "Enter Password: ")
    if lookup(list_of_users, email, password) == False:
      print("Email and Password Combination Invalid.\n")
      login()
     # Bind to a free port provided by the host
    userPort = i["port"]
    global isLastRegistered
    if userEmail == lastRegistered:
      isLastRegistered = True
    return userEmail
    #check to see if password and emails match in the database
  else:
    print("No users are registered with this client.")
    new_user = input("Do you want to register a new user (y/n)? ")
    if new_user == "y" or new_user == "Y":
      # If y, go through user registration
      fullname = input("\nEnter Full Name: ")
      email = input("Enter Email Address: ")
      password = getpass.getpass(prompt = "Enter Password: ")
      password2 = getpass.getpass(prompt = "Re-Enter Password: ")
      create_user(fullname, email, check_password(password, password2))
      file_in = open("database.json", "r")
      list_of_users = json.load(file_in) 
      login()
    else:
      #encrypt
      encrypt()
      print("Exiting SecureDrop.")
      sys.exit()
      
# This function is called everytime a user logs in to open their port
def makeHostConnection(ip, port):
  sock = socket.socket()
  # host = socket.gethostname()
  sock.bind((ip, port))
  sock.listen(10)
  while True:
    #while True:
    connection, addr = sock.accept()
    # confirm = connection.recv(1024)
    connection.close()
    break 
      
# This function locates the port number of the matched contact and checks its connection because the remote user would be listening (upon login as described in makeHostConnection())
def checkUserOnline(contactEmail, contactName):
  # Since two users are connecting at the same time, check there is a connection at XXXXX
  file_in = open("database.json", "r")
  database = json.load(file_in)
  contact = ""
  for i in database:
    if (i["email"] == contactEmail):
      userPort = i["port"]
      contact = i
      break

  s = socket.socket()
  host = socket.gethostbyname("localhost")
  result = s.connect_ex((host, int(userPort)))
  if (result == 0):
    onlineUsers.append(contact)
    print ("* " + contactName + " <" + contactEmail + ">")  
  file_in.close()

# First check if database contains any users
# If not progrem is in first time usage
# If so run login() function
if not list_of_users:
  print("No users are registered with this client.")
  new_user = input("Do you want to register a new user (y/n)? ")
  if new_user == "y" or new_user == "Y":
    # If y, go through user registration
    fullname = input("\nEnter Full Name: ")
    email = input("Enter Email Address: ")
    password = getpass.getpass(prompt = "Enter Password: ")
    password2 = getpass.getpass(prompt = "Re-Enter Password: ")
    create_user(fullname, email, check_password(password, password2))
    #encrypt first time
    key = Fernet.generate_key()
    # string the key in a file
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    encrypt()
  print("Exiting SecureDrop.")
    
else:
    #decrypt   
    #check to see if password and emails match in the database
    userEmail = login()
    if isLastRegistered == True:
      userEmail = lastRegistered
    H = threading.Thread(name='host', target=makeHostConnection, args=(userIP, int(userPort),))  
    H.start()
    MyPrompt().cmdloop()