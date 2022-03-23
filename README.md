# SecureDrop
SecureDrop is a Secure File Transfer system that I as well two other group members, Jacob Leboeuf & Sofya Chow developed for our semester project for COMP.2300 Intro to Computer Security at the Universtiy of Massachusetts Lowell from August 2021 - December 2021.

# How SecureDrop works
User Registration:
The user first puts in their basic information which gets stored in a database we created (if they weren't in the database already). Each user is stored as a JSON object within an array. When we find said user, we iterated through a list until that specific email is found. Each user was given a unique identifier to help locate their email.

User Login:
When the user attempts to login, the program will parse through the database.json to find a matching password. We implemented basic security features where we decrypt user information at the beginning of the program. As soon as the user exits the program, all information in the database.json file will be encrypted.

Adding Contacts:
Adding contacts was similiar to user registration where the program appends new contacts as a list of new JSON objects.

Listing Contacts:
When listing contacts, we had to list which contacts were online and avaliable to transfers between each other. For example, if two users have each other on their contact list, one user will log in onto his machine and create a unique socket to listen for other connections this is done with the function makeHostConnection(). The other user will log into her own machine and her socket will be listening as well. If the other user calls the command list, that user will find the first users unique port. They can then call the socket function connet_ex to verify whether the connection was successful.

Secure File Transfer
This is the part that I was tasked with completing. After establishing which users are avaliable to transfer files to, users can list the name of which files they want transfered, which is done through the a series of open sockets, a connection bewteen the client program and the server. The client code gets a file and the user to send as input. The client code will read the entire file and send it over to the server. The server will open its own socket and attempt to recieve the transmitted file by rereading it.

# Acknowledgements & Contribution
Thank you to Jacob Leboeuf and Sofya Chow for your help contributing with the project. Sofya worked on the User Registration & User Login. Jacob Leboeuf worked on adding contact and listing contacts.

You can contact Sofya at Sofya_Chow@student.uml.edu
You can contact Jacob Leboeuf at Jacob_Leboeuf@student.uml.edu
