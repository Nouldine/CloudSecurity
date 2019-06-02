#######################################################
# Author: Abdoul-Nourou Yigo  & Pooja Seth

# Client-Cloud Program
# This program is used to interact with the Client 
# When The IAM server has given the necessary information 
# to the cloud. When the user cridential are validated 
# the user can access the game and start playing.
# All the communication would be encrypted

#######################################################



from socket import *
from thread import *
from Crypto import Random
from Crypto.Cipher import AES
import mysql.connector
import uuid
import numpy as np
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import AES, PKCS1_OAEP

serverPort = 3430 #Make sure it matches the port number specified in the client side
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(30)

print ('The server is ready to receive')

my_sql_connect = mysql.connector.connect (
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

def get_user_data( username, cookie, status ):

    print("Calling insert_data()")

    sql = "SELECT * FROM userinfo"
    my_cursor =  my_sql_connect.cursor()
    my_cursor.execute(sql)
    user_info  = my_cursor.fetchall()

    print("Number of users currently enrolled: ", my_cursor.rowcount )
    for info in user_info:

        print("User info: %s  %s ",  ( info[ 0 ], info[ 1 ], info[ 2 ] ) )
        print("Username, cookie  %s %s", ( username, cookie, status ))

        if username == str( info[ 0 ] ).strip() and cookie == str( info[ 1 ] ).strip() and status == str(info[ 2 ]):
            print("record match")

            delete_record( username, cookie )

            return True

    return False

    my_cursor.close()

def delete_record( username, cookie  ):

    print("Calling delete")
    #db_config = read_db_config()
    my_cursor =  my_sql_connect.cursor()
    my_sql = "DELETE FROM userinfo  WHERE username = %s AND cookie = %s"

    print("Deleted user: ", username,  cookie)
    val = ( username, cookie )
    my_cursor.execute( my_sql, val )
    my_sql_connect.commit()

    #game(connectionSocket)

def ranking( username ):

    print("Calling ranking()")
    my_cursor =  my_sql_connect.cursor()
    
    sql =  "SELECT * ,FIND_IN_SET( scores, ( SELECT GROUP_CONCAT( scores ORDER BY scores DESC ) FROM user_registration ) ) AS rank FROM user_registration WHERE username = %s"
    
    my_cursor.execute( sql, ( username, ) )
    user_ranking = my_cursor.fetchall()
    print("user_info", user_ranking )
    my_rank = user_ranking[ 0 ][ 3 ]

    return my_rank

def update_user_score( username, scores ):

    print("Calling update_user_score() ")
    my_cursor =  my_sql_connect.cursor()

    sql1 = "SELECT  username, scores FROM  user_registration WHERE username =  %s"

    my_cursor.execute( sql1, ( username, ))
    user_info = my_cursor.fetchall()
    print("user_info", user_info )
    scores += user_info[ 0 ][ 1 ]
    
    print("Given userinfo", username, scores )
    print("Userinfo DB", user_info )

    my_cursor = my_sql_connect.cursor()
    sql = "UPDATE user_registration SET scores = %s WHERE username = %s"
    val = ( scores, username )
    my_cursor.execute( sql,val )

    print("Info is updated")
    '''
    for info  in user_info:
        
        print("Username and score Given", username, scores )
        print("userinfo in the database",  user_info[ 0 ], user_info[ 1 ] )
        
        if username ==  str( user_info[ 0 ] ).strip():
            
            print("Got the user")
            user_score = user_info[ 1 ]
            user_score += scores
    
            my_cursor = my_sql_connect.cursor()
            sql = "UPDATE user_registration SET scores = %s WHERE username = %s"

            val = ( user_score, username )        
            my_cursor.execute( sql,val )
            print("Update was a success")
    '''

    my_sql_connect.commit()


def user_registration( username, scores ):

    print("Calling user_registration()")

    scores = int(scores)
    my_cursor = my_sql_connect.cursor()
    sql = "INSERT INTO user_registration ( username, scores ) VALUES ( %s, %s )"

    val = ( username, scores )
    my_cursor.execute( sql, val )

    my_sql_connect.commit()


def generate_session_key():

    print("Calling generate_session_key()")
    session_key = get_random_bytes(16)
    return session_key

def write_session_key( my_session_key ):

     print("Calling write_session_key( my_session_key )")
     my_file = open("session_key_client.pem", "wb")
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

    my_file = open("my_private_key_client.pem", 'wb')
    my_file.write( my_key.exportKey('PEM'))

    my_file.close()

def write_private_key( my_key ) :

    print("Calling write_private_key( my_key )")

    my_file = open("my_private_key_client.pem", 'wb')
    my_file.write( my_key.exportKey('PEM'))

    my_file.close()

def write_public_key( my_key ):

    print("Calling write_public_key( my_key )")

    my_file = open("my_public_key.pem", "wb")
    my_file.write( my_key.exportKey("PEM") )

    my_file.close()

def write_received_session_key( my_session_key ):

    print("Calling write_received_session_key( my_session_key )")

    my_file = open("session_key_1_client.pem", "wb")
    my_file.write( my_session_key )

    print("We got the session key in a secure place")

    my_file.close()

def read_session_key():

    print("Calling read_session_key()")
    file_ =  open('session_key_1_client.pem', 'rb')
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
    private_key = RSA.importKey( open("my_private_key_client.pem").read() )

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new( private_key )
    session_key_2 = cipher_rsa.decrypt( session_key )
    write_received_session_key( session_key_2 )

def decrypt_iv( initial_vector ):

    print("Calling decrypt_session_key( session_key )")
    # Read the private key from the  file
    private_key = RSA.importKey( open("my_private_key_client.pem").read() )

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new( private_key )
    my_iv = cipher_rsa.decrypt( initial_vector )

    return my_iv

def send_public_to_IAM_client(  ):

    print("Calling  send_public_to_IAM_client()")
    print "Calling sending publickey"
    
    print("Test 2")
    private_key =  generate_private_key()
    write_private_key( private_key )
    print("Test 3")

    return True

def get_session_key( session_info ):

    print("Calling get_session_key( session_info )")
    decrypt_session_key( session_info )
    print("got my_session_key")
    print "listening to get the usre cookie"

def get_iv( iv_info, connectionSocket ):

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
            
            username = login_information.split("\t")[ 1 ].strip()
            paid = login_information.split("\t")[ 3 ].strip()
            print("Insertion was a success")
            success = "Success"
            success = success.encode()
            connectionSocket.send(success)
            
            my_rank = ranking( username )
            print("I hope my rank  will improve! Test1", my_rank )
            my_rank = str(my_rank).encode()
            connectionSocket.send(my_rank)

            #game( connectionSocket, paid )
            game(connectionSocket, username, paid )
            
            return True

        else:
            
            return False
    

def get_user_name_cookie(login_information):

    print("Calling connectionProcessing()")
    print("Encryption is here: ", login_information )

    user_name = login_information.split("\t")[1].strip()
    cookie = login_information.split("\t")[2].strip()
    status = login_information.split("\t")[3].strip()
    print("client is here")
    get_user_data( user_name, cookie, status )
    print "Test1"
    return True


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
         my_key = read_from_file("my_private_key_client.pem")
         connectionSocket.send( my_key.publickey().exportKey( format = 'PEM', passphrase = None, pkcs =  1 ) )
         print("Test 7")

         session_ = connectionSocket.recv(1024)
         get_session_key( session_ )
         iv_ = connectionSocket.recv(1024)
         get_iv( iv_, connectionSocket )

   else: 

        consequence_of_failing = "The information is not saved\t" + "Failure to save information! Please  try again IAM"
        failure_padded = padding_message(consequence_of_failing)
        encrypt_failure = encrpt_decrypt_msg.encrypt(failure_padded)
        connectionSocket.send(encrypt_failure)

    #connectionSocket.close()


def select_word(coonnectionSocket,paid):

    paid_words = {
        "muzzled":"nose and mouth part of an animal",
        "palazzo":"a palace",
        "jackpot":"a high prize",
        "jumping":"bounce or spring from surface",
        "cumquat":"orange colored oval fruit",
        "mahjong":"chinese game",
        "pyjamas":"a piece of clothing",
        "showbiz":"show business",
        "boombox":"large radio",
        "mammock":"to break into pieces",
        "eczema":"skin disorder"
    }

    basic_words = {
        "jazzy":"lovely, showy",
        "pizza":"Italian food",
        "kanzu":"long white garment from Africa",
        "zombi":"half dead",
        "crazy":"insane or not mentally sound",
        "xerox":"used to copy material",
        "fjord":"long, narrow inlet of the sea between slopes",
        "waltz":"a ballroom dance for couples",
        "booze":"too much liquor",
        "mozo":"an assistant",
        "pluck":"grab or pick",
        "block":"square piece of material",
        "ninja":"warrior"}



    if paid == '1':
        level = connectionSocket.recv(1024)
        level = str(level).decode('utf-8')
        print("Level is",level)
        if level == '1':
            word,hint = random.choice(list(basic_words.items()))
            return word,hint
        else:

            word,hint = random.choice(list(paid_words.items()))
            return word,hint

    else:
        level = connectionSocket.recv(1024)
        level = str(level).decode('utf-8')
        print("Level is",level)
        print("You need to pay the game! Shame on YOU")
        word,hint = random.choice(list(basic_words.items()))
        return word,hint


def game(connectionSocket, username, paid ):
    
    #my_rank = ranking( username )
    #print("I hope my rank  will improve! Test1", my_rank )
    #my_rank = str(my_rank).encode()
    #connectionSocket.send(my_rank)

    print("paid game", paid )
    checking = True
    play_again = True
    while play_again:
        #chose a word and hint in random
        chosenword,hint = select_word( connectionSocket, paid )
        if len(chosenword) == 5:
            score = 10
        else:
            score = 50

        #hint =  str(hint).encode('utf-8')
        #send hint to client
        #hint = bytes(hint,'utf-8')
        hint  = bytes(hint).encode('utf-8')
        #connectionSocket.send(hint)
        #chosenword_bytes = bytes(chosenword,'utf-8')
        chosenword_bytes = bytes(chosenword).encode('utf-8')
        #connectionSocket.send(chosenword_bytes)
        guess = 0 #player guess input
        #list of all guessed letters
        guessed_letters = []
        #list of blanks in word
        blank_word = []
        #replacing all the letters of the word with dashes
        
        for letter in chosenword:
            
            blank_word.append("_ ")
        

        blank_word_data = ''.join(blank_word)
        #blank_word_data = bytes(blank_word_data,'utf-8')
        blank_word_data = bytes(blank_word_data).encode('utf-8')
        print(blank_word_data)
        #connectionSocket.send(blank_word_data)
        #number of attempts
        attempts = 6
        attemptsBytes = bytes(attempts)
        #connectionSocket.send(attemptsBytes)
        info  =  hint + '\t' + chosenword + '\t' + blank_word_data
        info = bytes(info).encode('utf-8')
        connectionSocket.send(info)
        while attempts > 0:
                print("Chosen", chosenword )
                '''
                guess = str(guess).encode('utf-8')
                guessed = guess.split("\t")[0].strip()
                if(guessed == "game"):
                    user_name = guess.split("\t")[1].strip()
                    scores = guess.split("\t")[2].strip()
                    update_user_score( user_name, scores, connectionSocket )
                '''
                #if(attempts != 0):
                try:
                    guess = connectionSocket.recv(1024)
                except:
                    print('The error is here')
                print("guess is: ", guess)
                #guess = str(guess).encode('utf-8')
                #guessed = guess.split("\t")[0].strip()
                '''
                if(guessed == "game"):
                    user_name = guess.split("\t")[1].strip()
                    scores = guess.split("\t")[2].strip()
                    update_user_score( user_name, scores, connectionSocket )
                '''
                #add guess to the list of guesses
                guessed_letters.append(guess)
                #print(guessed_letters)
                #if letter is not in the word
                if guess not in chosenword:
                    attempts -= 1
                else:
                #if letter is found in the word
                    searchMore = True
                    startSearchIndex = 0
                    while searchMore:
                        try:
                            #find the letter
                            foundAtIndex = chosenword.index(guess,startSearchIndex)
                            blank_word[foundAtIndex] = guess
                            startSearchIndex = foundAtIndex + 1
                        except:
                            searchMore = False
                #send the updated list
                blank_word_data1 = ''.join(blank_word)
                if( blank_word_data1 == chosenword ):
                    blank_word_data1 = bytes(blank_word_data1).encode('utf-8')
                    try:
                        connectionSocket.send(blank_word_data1)
                    except:
                        print("Love me ")
                    print("updated list sent")
                    print("You win the game")
                    
                    update_user_score( username, score )

                    #play_again = False
                    response = connectionSocket.recv(1024)
                    response = str(response).decode('utf-8')
                    print("Response", response )
                    if response == 'yes':
                        print("I am here")
                        attempts = -1
                        #play_again = True
                        #game( connectionSocket, username, paid  )
                    else:
                        print("Love me again again ")
                        play_again = False
                        
                        attempts = 0
                        #checking = False
                        print("GAME IS DONE")
                        my_rank = ranking( username )
                        print("Hope I am not the last! Test2", my_rank )
                        my_rank = str( my_rank ).encode()
                        connectionSocket.send(my_rank)
                        break
                        connectionSocket.close()
                else:
                    blank_word_data1 = bytes(blank_word_data1).encode('utf-8')
                    connectionSocket.send(blank_word_data1)
                    print("updated list sent")
                    if attempts == 0:
                       play_again = False
                       print("You loose")
                       response = connectionSocket.recv(1024)
                       response = str(response).decode('utf-8')
                       print("Response", response )
                       if response == 'yes':
                         print("I am here")
                       #play_again = True
                         game( connectionSocket, username, paid  )
                       else:
                         print("Love me again again ")
                         play_again = False

                         attempts = 0
                         #checking = False
                         print("GAME IS DONE")
                         my_rank = ranking( username )
                         print("I want to be the first! Test3", my_rank )
                         my_rank = str( my_rank ).encode()
                         connectionSocket.send(my_rank)

                         break
                         connectionSocket.close()




# Manage the multi-thread processes
while 1:

     connectionSocket, addr = serverSocket.accept()
     print("From:", addr)
     start_new_thread(check_connection, (connectionSocket,))

