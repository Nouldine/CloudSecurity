
#######################################################################################

# Server program for case transfer
# Created by:   Abdoul-Nourou Yigo
# Creation date:
# Notes: The main procedure for login request processing is already given, you need to:

# This program is used to communicate the IAM server. The IAM server would sent the
# necessary information that  would be saved in  a mysql database. This information 
# would be used to allow the accessibility of the user to the game the game platform

#######################################################################################



from socket import *
from thread import *
from Crypto import Random
from Crypto.Cipher import AES
import mysql.connector
import uuid
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import AES, PKCS1_OAEP

serverPort = 3410 #Make sure it matches the port number specified in the client side
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(30)

print ('The server is ready to receive')

mydb = mysql.connector.connect (
        host = "35.232.30.107",
        user = "root",
        passwd = "root",
        database = "gaminginfo"
)

def padding_message( sentence ):

    length = len(sentence)

    if(length == 0 ):

        return

    elif( length % 16 != 0 ):

        sentence += ' ' * ( 16 - length % 16 )

    else:

        print("Coding is fun")

    return sentence

# This function is used to  insert username 
# cookie and the user in a database
# when access the game this information 
# would be removed
def inser_data( username, cookie, status ):

    print("Calling insert_data()")

    my_cursor =  mydb.cursor()
    sql = "INSERT INTO userinfo (username, cookie, status) VALUES ( %s, %s, %s )"
    val = (username, cookie, status )
    my_cursor.execute( sql, val )

    mydb.commit()

# This function is used to insert the username 
# in  the database
def user_registration( username, scores, paid ):

    print("Calling user_registration()")
        
    scores = int(scores)
    my_cursor = mydb.cursor()
    sql = "INSERT INTO user_registration ( username, scores, paid ) VALUES ( %s, %s, %s)"

    val = ( username, scores, paid )
    my_cursor.execute( sql, val )

    mydb.commit()

# This function is used to update 
# the user information  score
def update_user_score( scores, username ):

    print("Calling update_user_score() ")

    scores = int(scores)
    scores += 10
    my_cursor = mydb.cursor()
    sql = "UPDATE user_registration SET  scores = %s WHERE username = %s"

    val = ( scores, username )
    my_cursor.execute( sql,val )
    mydb.commit()

def generate_session_key():
    
    print("Calling generate_session_key()")
    session_key = get_random_bytes(16)
    return session_key 

def write_session_key( my_session_key ):    

     print("Calling write_session_key( my_session_key )")
     my_file = open("session_key.pem", "wb")
     my_file.write( my_session_key )
     my_file.close()

def session_key_session( connectionSocket ):
     
    print("Calling session_key_session( connectionSocket )")
    encrptDecryptObj_2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    session_key = generate_session_key ()    
    session_key_info = "sessionkey" + "\t" + session_key
    
    print("Session key: ", session_key_info )

    padded_session_key = padding( session_key_info )
    encrypted_session_key = encrptDecryptObj_2.encrypt( padded_session_key )
    connectionSocket.send( encrypted_session_key )

def generate_public_key( ):
    
    print("Calling generate_public_key( )")
    key = RSA.generate(1024)
    #publicKey = key.publickey().exportKey()
    print("My public key: %s ", key )

    return key;

def generate_private_key():
    
    print("Calling Generate_private_key() ")
    key = RSA.generate(1024)
    #privateKey = key.exportKey()

    return key

def write_private_key( my_key ) :

    print("Calling write_private_key( my_key )")

    my_file = open("my_private_key.pem", 'wb')
    my_file.write( my_key.exportKey('PEM'))

    my_file.close()

def write_public_key( my_key ):

    print("Calling write_public_key( my_key )")
    
    my_file = open("my_public_key.pem", "wb")
    my_file.write( my_key.exportKey("PEM") )

    my_file.close()

def write_received_session_key( my_session_key ):
    
    print("Calling write_received_session_key( my_session_key )")

    my_file = open("session_key_1.pem", "wb")
    my_file.write( my_session_key )

    print("We got the session key in a secure place")

    my_file.close()

def read_session_key(): 

    print("Calling read_session_key()")
    file_ =  open('session_key_1.pem', 'rb') 
    my_session_key = file_.read()
    return my_session_key

def read_iv(): 

   print("Calling read_iv()") 
   file_ = open('iv.pem', 'rb')
   my_iv = file_.read()
   #print("read_iv()", my_iv )
   return my_iv 

def read_from_file( my_file ) :

    print("Calling read_from_file( my_file )")
    my_file_ = open( my_file, 'r')
    key = RSA.importKey( my_file_.read() )
    my_file_.close()

    return key

def decrypt_session_key( session_key ):

    print("Calling decrypt_session_key( session_key )")
    # Read the private key from the  file
    private_key = RSA.importKey( open("my_private_key.pem").read() )
    
    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new( private_key )
    session_key_2 = cipher_rsa.decrypt( session_key )
    write_received_session_key( session_key_2 )

def decrypt_iv( initial_vector ): 
    
    print("Calling decrypt_session_key( session_key )")
    # Read the private key from the  file
    private_key = RSA.importKey( open("my_private_key.pem").read() )

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new( private_key )
    my_iv = cipher_rsa.decrypt( initial_vector )

    return my_iv

def send_public_to_IAM_client(  ): 
    
    print("Calling  send_public_to_IAM_client()")
    print "Calling sending publickey"
    #if( user_information == "publickey" ):
    
    print("Test 2")
    private_key =  generate_private_key()
    write_private_key( private_key )
    print("Test 3")

    return True

def get_session_key( session_info ):

    print("Calling get_session_key( session_info )")
    #my_session_key = session_info.split("\t")[1].strip()
    #write_received_session_key( my_session_key )
    decrypt_session_key( session_info )
    print("got my_session_key")
    #check_connection(connectionSocket)
    print "listening to get the usre cookie"

   #return True

#def get_session_key( initial_vector ): 

#    decrypt_session_key( intial_vector )


def get_iv( iv_info, connectionSocket ):

    #iv_info = iv_info.split("\t")[1].strip()
    #my_file = open("iv.pem", "wb")
    #my_file.write( iv_info )
    
    print("Calling get_iv( iv_info, connectionSocket )")

    success = "Success"
    success = success.encode()
    connectionSocket.send(success)
    
    my_session = read_session_key()
    my_iv =  decrypt_iv( iv_info )
    #padded_iv = padding_message(my_iv)

    print("session key:",  my_session  )
    print("IV: ", my_iv )
    encrpt_decrypt_msg = AES.new( my_session, AES.MODE_CBC, my_iv )
    request = connectionSocket.recv(1024)
    login_information = encrpt_decrypt_msg.decrypt(request)
    
    if( login_information.split("\t")[ 0 ].strip() == "cookie" ):

        checking = get_user_name_cookie(login_information)
    
        if( checking ==  True ):
        
            print("Insertion was a success") 
            return True

        else:

            #print("Insertion failed")
            return False
    elif( login_information.split("\t")[ 0 ].strip() == "username" ):
        
        print("User information", login_information )

        checking_2 = update_user_information( login_information )

        if( checking_2 ==  True ):

            print("Registration was a success")
            success = "Success"
            success = success.encode()
            connectionSocket.send(success)

            return True

        else:

            print("Registration failed")
            return False



    #check_connection(connectionSocket)


def  get_information( login_information ):

     #checking = connectionProcessing(request, connectionSocket )

        if( login_information.split("\t")[ 0 ].strip() == "game" ):

            update_game_info( login_information )

        elif( login_information.split("\t")[ 0 ].strip() == "username" ):

            update_user_information( login_information )



def update_game_info( game_info ):
    
    print("Calling  update_game_info( game_info )")
    user_name = game_info.split("\t")[1].strip()
    scores = game_info.split("\t")[2].strip()
    update_user_score( scores, user_name )

    print("Score updated")

def update_user_information( username ): 

    print("Calling update_user_information( username )")
    user_name = username.split("\t")[1].strip()
    scores = username.split("\t")[2].strip()
    paid = username.split("\t")[ 3 ].strip()

    user_registration(user_name, scores, paid )
    print "Username insertion"
    return True

def get_user_name_cookie(login_information):

    print("Calling connectionProcessing()")
    print("Encryption is here: ", login_information ) 

    user_information = login_information.split("\t")[0].strip()

    if( user_information == "cookie"):
          
        user_name = login_information.split("\t")[1].strip()
        cookie = login_information.split("\t")[2].strip()
        status = login_information.split("\t")[3].strip()
        print("IAM is here")
        inser_data( user_name, cookie, status )
        print "Test1"
        #return True

    else:

        return False

def check_connection(connectionSocket):

   print("Calling check_connection()")
   #encrpt_decrypt_msg = AES.new('This is a key456', AES.MODE_CBC, 'This is an IV123')
   #encrypt_decrypt_msg = AES.new( se
   request_2 = connectionSocket.recv(1024).decode()
   #request_2 = encrpt_decrypt_msg.decrypt(request_2)

   print("Printing Request")
   
   print("request_2", request_2 ) 
    
   if( request_2.strip() == "publickey" ): 

         print( "publickey" )
         send_public_to_IAM_client()
         print("Test 6")
         #my_key = read_from_file("my_public_key.pem")
         my_key = read_from_file("my_private_key.pem")
         connectionSocket.send( my_key.publickey().exportKey( format = 'PEM', passphrase = None, pkcs =  1 ) )
         print("Test 7")

         session_ = connectionSocket.recv(1024) 
         get_session_key( session_ )
         iv_ = connectionSocket.recv(1024)
         get_iv( iv_, connectionSocket )

   else:

        my_session_key =  read_session_key()
        my_iv   = read_iv()        
        encrpt_decrypt_msg_2 = AES.new( my_session_key, AES.MODE_CBC, my_iv )
        login_information = encrpt_decrypt_msg_2.decrypt(request_2)
        #checking = connectionProcessing(request, connectionSocket )

        if( login_information.split("\t")[ 0 ].strip() == "game" ):

            update_game_info( login_information )

        elif( login_information.split("\t")[ 0 ].strip() == "username" ):

            update_user_information( login_information )

        else:

            consequence_of_failing = "The information is not saved\t" + "Failure to save information! Please  try again IAM"
            failure_padded = padding_message(consequence_of_failing)
            encrypt_failure = encrpt_decrypt_msg.encrypt(failure_padded)
            connectionSocket.send(encrypt_failure)

    #connectionSocket.close()


# Manage the multi-thread processes
while 1:

     connectionSocket, addr = serverSocket.accept()
     print("From:", addr)
     start_new_thread(check_connection, (connectionSocket,))





