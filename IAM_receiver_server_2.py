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

serverPort = 3398 #Make sure it matches the port number specified in the client side
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

def inser_data( username, cookie ):

    print("Calling insert_data()")

    my_cursor =  mydb.cursor()
    sql = "INSERT INTO userinfo (username, cookie) VALUES ( %s, %s )"
    val = (username, cookie)
    my_cursor.execute( sql, val )

    mydb.commit()

def user_registration( username, scores ):

    print("Calling user_registration()")

    scores = int(scores)
    my_cursor = mydb.cursor()
    sql = "INSERT INTO user_registration ( username, scores ) VALUES ( %s, %s )"

    val = ( username, scores )
    my_cursor.execute( sql, val )

    mydb.commit()


def update_user_score( scores, username ):

    print("Calling update_user_score() ")

    scores = int(scores)
    scores += 10
    my_cursor = mydb.cursor()
    sql = "UPDATE user_registration SET  scores = %s WHERE usermane = %s"

    val = ( scores, username )
    my_cursor.execute( sql,val )
    mydb.commit()

def generate_session_key():
	
     session_key = get_random_bytes(16)
     return session_key 

def write_session_key( my_session_key ):
	
     my_file = open("session_key.pem", "wb")
     my_file.write( my_session_key )
     my_file.close()

def session_key_session( connectionSocket ):
     
    encrptDecryptObj_2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    session_key = generate_session_key ()    
    session_key_info = "sessionkey" + "\t" + session_key
    
    print("Session key: ", session_key_info )

    padded_session_key = padding( session_key_info )
    encrypted_session_key = encrptDecryptObj_2.encrypt( padded_session_key )
    connectionSocket.send( encrypted_session_key )
def generate_public_key( ):

    key = RSA.generate(1024)
    #publicKey = key.publickey().exportKey()

    print("My public key: %s ", key )

    return key;

def generate_private_key():

    key = RSA.generate(1024)
    #privateKey = key.exportKey()

    return key

def write_private_key( my_key ) :

    my_file = open("my_private_key.pem", 'wb')
    my_file.write( my_key.exportKey('PEM'))

    my_file.close()

def write_public_key( my_key ):

    my_file = open("my_public_key.pem", "wb")
    my_file.write( my_key.exportKey("PEM") )

    my_file.close()

def write_received_session_key( my_session_key ):

    my_file = open("session_key_1.pem", "wb")
    my_file.write( my_session_key )

    print("We got the session key in a secure place")

    my_file.close()

def read_session_key(): 

    file_ =  open('session_key_1.pem', 'rb') 
    my_session_key = file_.read()
    return my_session_key

def read_iv(): 

   file_ = open('iv.pem', 'rb')
   my_iv = file_.read()

   #print("read_iv()", my_iv )

   return my_iv 

def read_from_file( my_file ) :

    my_file_ = open( my_file, 'r')
    key = RSA.importKey( my_file_.read() )
    my_file_.close()

    return key

def decrypt_session_key( session_key ):

    # Read the private key from the  file
    private_key = RSA.importKey( open("my_private_key.pem").read() )
    
    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new( private_key )
    session_key_2 = cipher_rsa.decrypt( session_key )
    write_received_session_key( session_key_2 )

#def decryption_using_session_key(): 

def send_public_to_IAM_client( request ): 
   
    print "Calling sending publickey"
    #if( user_information == "publickey" ):
    
    print("Test 2")
    private_key =  generate_private_key()
    write_private_key( private_key )
    print("Test 3")

    return True

def get_session_key( session_info ):

    #my_session_key = session_info.split("\t")[1].strip()
    #write_received_session_key( my_session_key )
    decrypt_session_key( session_info )
    print("got my_session_key")
    #check_connection(connectionSocket)
    print "listening to get the usre cookie"

   #return True


def get_iv( iv_info, connectionSocket ):

    #iv_info = iv_info.split("\t")[1].strip()
    #my_file = open("iv.pem", "wb")
    #my_file.write( iv_info )

    success = "Success"
    success = success.encode()
    connectionSocket.send(success)
    
    my_session = read_session_key()
    my_iv = read_iv()
    padded_iv = padding_message(iv_info)

    print("session key:",  my_session  )
    print("IV: ", padded_iv )
    encrpt_decrypt_msg = AES.new( my_session, AES.MODE_CBC, padded_iv )
    request = connectionSocket.recv(1024)
    login_information = encrpt_decrypt_msg.decrypt(request)
    checking = connectionProcessing(login_information)
   
    #check_connection(connectionSocket)

def update_game_info( game_info ):

    user_name = game_info.split("\t")[1].strip()
    scores = game_info.split("\t")[2].strip()
    update_user_score( scores, user_name )

    print("Score updated")

def connectionProcessing(login_information):

    print("Calling connectionProcessing()")
    print("Encryption is here: ", login_information ) 

    user_information = login_information.split("\t")[0].strip()
    if( user_information == "game" ):

         user_name = login_information.split("\t")[1].strip()
         scores = login_information.split("\t")[2].strip()
         update_user_score( scores, user_name )

         print("Score updated")

         return True

    elif( user_information == "username" ):

          user_name = login_information.split("\t")[1].strip()
          scores = login_information.split("\t")[2].strip()
          user_registration(user_name, scores)
          print "Username insertion"
          return True

    elif( user_information == "cookie"):
          
          user_name = login_information.split("\t")[1].strip()
          cookie = login_information.split("\t")[2].strip()
          print("IAM is here")
          inser_data(user_name, cookie)
          print "Test1"
          #return True

    else:

          return False

def check_connection(connectionSocket):

    #encrpt_decrypt_msg = AES.new('This is a key456', AES.MODE_CBC, 'This is an IV123')
    #encrypt_decrypt_msg = AES.new( se
    print("Calling check_connection()")
    request_2 = connectionSocket.recv(1024).decode()
    
    #print("Request", request )
    #request_2 = encrpt_decrypt_msg.decrypt(request)
   
    print("request_2", request_2 ) 

    if( request.split("\t")[0].strip() == "game" ):

         update_game_info( request_2 )

    
    elif( request_2.strip() == "publickey" ): 

         print( "publickey" )
         send_public_to_IAM_client( request_2 )
         print("Test 6")
         #my_key = read_from_file("my_public_key.pem")
         my_key = read_from_file("my_private_key.pem")
         connectionSocket.send( my_key.publickey().exportKey( format = 'PEM', passphrase = None, pkcs =  1 ) )
         print("Test 7")

         session_ = connectionSocket.recv(1024) 
         get_session_key( session_ )
         iv_ = connectionSocket.recv(1024)
         get_iv( iv_, connectionSocket )

    #key_information.split("\t")[1].strip()
    elif( request_2.split("\t")[ 0 ].strip() == "session" ):

        get_session_key( request_2, connectionSocket )

    elif( request_2.split("\t")[ 0 ].strip() ==  "iv" ):

        get_iv( request_2, connectionSocket )


    else:

        my_session_key =  read_session_key()
        
        encrpt_decrypt_msg_2 = AES.new( my_session_key, AES.MODE_CBC, 'This is an IV123' )
        login_information = encrpt_decrypt_msg_2.decrypt(request)
        checking = connectionProcessing(request, connectionSocket )

        my_cookie = uuid.uuid1()
        my_cookie = str(my_cookie)

        if checking == True:

            print "Test2"
            #success = "Saved\t" + my_cookie
            #encryption_again = padding_message(success)
            #my_ciphtertext = encrpt_decrypt_msg.encrypt(encryption_again)
            #connectionSocket.send(my_ciphtertext)

	    print("Test 6")
            #my_key = read_from_file("my_public_key.pem")
            #my_key = read_from_file("my_private_key.pem")
	    #connectionSocket.send( my_key.publickey().exportKey( format = 'PEM', passphrase = None, pkcs =  1 ) )
            print("Test 7")

        else:

            consequence_of_failing = "The information is not saved\t" + "Failure to save information! Please  try again IAM"
            failure_padded = padding_message(consequence_of_failing)
            encrypt_failure = encrpt_decrypt_msg.encrypt(failure_padded)
            connectionSocket.send(encrypt_failure)

    connectionSocket.close()


# Manage the multi-thread processes
while 1:

     connectionSocket, addr = serverSocket.accept()
     print("From:", addr)
     start_new_thread(check_connection, (connectionSocket,))





