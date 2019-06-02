            '''
            guess = str(guess).encode('utf-8')
            guessed = guess.split("\t")[0].strip()

            if(guessed == "game"):

                    user_name = guess.split("\t")[1].strip()
                    scores = guess.split("\t")[2].strip()
                    update_user_score( user_name, scores, connectionSocket )
            '''

            if(attempts != 0):

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
                    #play_again = False
                    response = connectionSocket.recv(1024)

                    response = str(response).decode('utf-8')
                    print("Response", response )

                    if response == 'yes':
                        print("I am here")
                        #play_again = True

                        game( connectionSocket, paid  )
                    else:
                        play_again = False
                        checking = False
                        print("GAME IS DONE")
                        break
                        #connectionSocket.close()


                else:
                    blank_word_data1 = bytes(blank_word_data1).encode('utf-8')
                    connectionSocket.send(blank_word_data1)
                    print("updated list sent")




# Manage the multi-thread processes
try:
    while 1:

        connectionSocket, addr = serverSocket.accept()
        print("From:", addr)
        start_new_thread(check_connection, (connectionSocket,))

except:

    print("They kill me")
