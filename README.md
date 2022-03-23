# SecureDrop
SecureDrop is a Secure File Transfer program that I as well two other group members, Jacob Leboeuf & Sofya Chow developed for our semester project for COMP.2300 Intro to Computer Security at the Universtiy of Massachusetts Lowell from August 2021 - December 2021. 

This can be used for any users that need to transfer files between other online users through the use of open sockets.

# How SecureDrop works
User Registration:
The user first puts in their basic information which gets stored in a database we created (if they were not in the database already). Each user is stored as a JSON object within an array. When we find said user, we iterated through a list until that specific email is found. Each user was given a unique identifier to help locate their email.

User Login:
When the user attempts to login, the program will parse through the database.json file to find a matching password. We implemented basic security features where we decrypt user information at the beginning of the program. As soon as the user exits the program, all information in the database.json file will be encrypted.

Adding Contacts:
Adding contacts was similiar to user registration where the program appends new contacts to a list of new JSON objects.

Listing Contacts:
Each contact had to be listed whether or not they were online and avaliable to transfer files between each other. For example, if two users have each other on their contact list, the first user will log in on their machine and create a unique socket to listen for other connections. This is done with the function makeHostConnection(). The second user will log into their own machine listen for open sockets. If the second user types the command list, that user will find the first users unique port. They can then call the socket function connet_ex to verify whether the connection was successful.

Secure File Transfer
This is the part that I was tasked with completing. After setting up a socket, a connection betweem the client program and the server, the client code receives a file and user id to send as input. This will then get stored in a list of online users and checks to see if other users are online. The socket then gets opened on the client side and uses its own IP and port. Finally, the client code will read the entire file and send it over to the server. The server will open its own socket to receieve the transmitted file.

# Acknowledgements & Contribution
Thank you to Jacob Leboeuf and Sofya Chow for your help contributing with the project. Sofya worked on the User Registration & User Login. Jacob Leboeuf worked on adding contact and listing contacts.

You can contact Sofya at Sofya_Chow@student.uml.edu
You can contact Jacob Leboeuf at Jacob_Leboeuf@student.uml.edu
