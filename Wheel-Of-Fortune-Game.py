from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    dF = open('dictionary.txt', 'r')
    dictionary = (dF.readlines())
    for i in range(len(dictionary)):
        dictionary[i] = str(dictionary[i]).strip().lower()
    # Read dictionary file in from dictionary file location **DONE**
    # Store each word in a list. **DONE**
      
    
def readTurnTxtFile():
    global turntext 
    ttF = open('turntext.txt', 'r')
    turntext = (ttF.read())
    #read in turn intial turn status "message" from file **DONE**

        
def readFinalRoundTxtFile():
    global finalroundtext
    frF = open('finalround.txt', 'r')
    finalroundtext = frF.read()
    #read in turn intial turn status "message" from file **DONE**

def readRoundStatusTxtFile():
    global roundstatus
    rsF = open(roundstatusloc, 'r')
    roundstatus = (rsF.read())
    # read the round status  the Config roundstatusloc file location **DONE**

def readWheelTxtFile():
    global wheellist
    wF = open(wheeltextloc, 'r')
    wheellist = (wF.readlines())
    for i in range(len(wheellist)):
        wheellist[i] = str(wheellist[i]).strip().lower()
    # read the Wheel name from input using the Config wheelloc file location **DONE**
    
def getPlayerInfo():
    global players
    players[0]["name"] = input("Hello Player 1! What is your name?: ")
    players[1]["name"] = input("Hello Player 2! What is your name?: ")
    players[2]["name"] = input("Hello Player 3! What is your name?: ")
    # read in player names from command prompt input **DONE**
    print(players)


def gameSetup():
    # Read in File dictionary **DONE**
    # Read in Turn Text Files **DONE**
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    #choose random word from dictionary **DONE**
    #print(dictionary)
    global roundWord
    roundWord = random.choice(dictionary)
    #print(roundWord)
    #make a list of the word with underscores instead of letters. **DONE**
    global roundUnderscoreWord
    roundUnderscoreWord = ['_' for i in roundWord]
    return roundWord,roundUnderscoreWord
    

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0 **DONE**
    players[0]["roundtotal"] = 0
    players[1]["roundtotal"] = 0
    players[2]["roundtotal"] = 0
    # Return the starting player number (random) **DONE**
    initPlayer = random.randrange(0,3)
    # Use getWord function to retrieve the word and the underscore word (blankWord) **DONE**
    getWord()

    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels

    stillinTurn = True

    # Get random value for wheellist
    spinResult = random.choice(wheellist)
    # Check for bankrupcy, and take action.
    if spinResult == "bankrupt":
        print("You landed on bankrupt, you lose all round earnings.")
        players[playerNum]["roundtotal"] = 0
        stillinTurn = False
    # Check for lose turn
    elif spinResult == "loseturn":
        print("You landed on loseturn, you lose your turn.")
        stillinTurn = False
    # Get amount from wheel if not lose turn or bankruptcy
    else:
        while True:
            print(f"You landed on {spinResult}")
        # Ask user for letter guess
            global letterGuess
            letterGuess = input("Please guess a consonant: ")
            if letterGuess in vowels:
                print("Sorry, that is not a consonant. Try again.")
            else:
                # Use guessletter function to see if guess is in word, and return count
                goodGuess, count = guessletter(letterGuess, playerNum)
                # Change player round total if they guess right.
                if goodGuess == True:
                    players[playerNum]["roundtotal"] += int(spinResult)
                    print(players)
                    print(f"{spinResult} has been added to your bank.")
                    stillinTurn = True
                    break
                else:
                    print("Letter you guessed is not in the word.")
                    stillinTurn = False
                    break

    return stillinTurn


def guessletter(letterGuess, playerNum): 
    global players
    global blankWord
    # parameters:  take in a letter guess and player number
    letter = letterGuess
    x = True
    count = 0
    # Change position of found letter in blankWord to the letter instead of underscore 
    #goodGuess = False
    #stillinTurn = True
    while x == True:
        if letter in roundWord:
            for i in range(len(roundWord)):
                if roundWord[i] == letter:
                    roundUnderscoreWord[i] = letter

            goodGuess = True
            count = roundWord.count(letter)
            print(f"Player {players[playerNum]['name']} guessed a correct letter! It is in the word {count} times!")
            print(roundUnderscoreWord)
                
        else:
            print(f"Player {players[playerNum]} guessed an incorrect letter, it is not in the word.")
            goodGuess = False
        x = False

 
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    
    # Ensure player has 250 for buying a vowel
    if players[playerNum]["roundtotal"] >= 250:
        while True:
            print("You have enough money to buy a vowel!")
            vowelGuess = input("Please enter a vowel: ")
            # Ensure letter is a vowel
            if vowelGuess in vowels:
                # Use guessLetter function to see if the letter is in the file
                guessletter(vowelGuess, playerNum)
                players[playerNum]['roundtotal'] -=250
            goodGuess = True
            break
    else:
        print("You don't have enough money to buy a vowel!")
        goodGuess = True
        
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    #print(roundWord)
    guessWord = input("Please enter the word you would like to guess: ")
    if guessWord == roundWord:
    # Fill in blankList with all letters, instead of underscores if correct 
        for i in range (len(roundWord)):
            if roundWord == guessWord:
                roundUnderscoreWord[i] = guessWord
            #print(roundUnderscoreWord)
            print(f"Congratulations! You guessed the word! The word was {roundWord}")
    # return False ( to indicate the turn will finish) 
    else:
        print("That word was not correct!")
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    
    # use the string.format method to output your status for the round
    readRoundStatusTxtFile()
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal ???????????????
    
    print(turntext.format(name = players[playerNum]["name"], word = roundUnderscoreWord))
    stillinTurn = True
    while stillinTurn:
        # Check to see if the word is solved, and return false if it is
        if '_' not in roundUnderscoreWord:
            stillinTurn = False
            break
        choice = input(f"Hello {players[playerNum]['name']}, would you like to (S)pin, (B)uy Vowel, or (G)uess the word?: ")
        
        # use the string.format method to output your status for the round
        readRoundStatusTxtFile()
        # Get user input S for spin, B for buy a vowel, G for guess the word
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundNum

    roundNum = roundNum +1
    print(f"This is round {roundNum}")

    initPlayer = wofRoundSetup()
    roundInProgress = True
    while roundInProgress:
        print(roundUnderscoreWord)
        if '_' not in roundUnderscoreWord:

            for i in players.keys():
                newGameTotal = players[i]["gametotal"] + players[i]["roundtotal"]
                players[i].update({"gametotal": newGameTotal})

            roundInProgress = False
            break

        # Begin the current players turn
        wofTurn(initPlayer)

        # Update so the next person gets to go
        initPlayer += 1
        if (initPlayer > 2):
            initPlayer = 0
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round
    print(roundstatus.format(word=roundWord))
    
    

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    givenLetters = {"R", "S", "T", "L", "N", "E"}

    # Find highest gametotal player and the player's respective game total.  They are playing.
    for i in players.keys():
        if players[i]["gametotal"] > players[winplayer]["gametotal"]:
            winplayer = i
    amount = players[winplayer]["gametotal"]
    # Print out instructions for that player and who the player is.
    print(finalroundtext.format(name = players[winplayer]['name'], total = amount))
    print("==============================================================================")
    print(f"""Congratulations {players[winplayer]['name']}, you have made it to the final round! You must guess one word, and the letters 
    R, S, T, L, N, and E will be given for free.
    Also free of charge, you will be able to guess 3 consonants and 1 vowel. 
    With these letters in place, you will have one opportunity to guess the final word.
    If your guess is right, you will get a final prize of $1,000,000 in addition to your previous earnings. 
    Of course, if you happen to guess wrong, you go home empty handed. Good luck!""")
    print("===============================================================================")
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    for i in givenLetters:
        guessletter(i.lower(), winplayer)
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(f"The current word is: {roundUnderscoreWord}.")
    # Gather 3 consonants and 1 vowel and use the guessletter function to see if they are in the word
    for i in range(3):
        guessedConsonant = []
        while True:
            consonant = input(f"Please enter number {i + 1} consonant you would like to guess:").lower()
            if consonant.isalpha == False or len(consonant) != 1:
                print("That is not a letter, try again.")
            elif consonant in vowels:
                print("You must only guess a consonant for now, try again.")
            elif consonant in roundUnderscoreWord:
                print("That letter is already showing, try again.")
            elif consonant in guessedConsonant:
                print("You already guessed that letter, try again.")
            else:
                guessletter(consonant, winplayer)
                guessedConsonant.append(consonant)
                break

    while True:
        vowel = input("Please enter a vowel you would like to guess:").lower()
        if vowel.isalpha == False or len(vowel) != 1:
            print("That is not a letter, try again.")
        elif vowel not in vowels:
            print("You must guess a vowel now, try again.")
        elif vowel in roundUnderscoreWord:
            print("That vowel is already showing, try again.")
        else:
            guessletter(vowel, winplayer)
            break

    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    print(f"After your guesses, the word now appears as this: {roundUnderscoreWord}")
    # Get user to guess word
    finalGuess = input("Now it is time to make your only guess of the final word...Good luck!: ").lower()
    # If they do, add finalprize and gametotal and print out that the player won
    if finalGuess == roundWord:
        finalAward = finalprize + amount
        print(f"Congratulations! You guessed the word correctly. Your total prize is ${finalAward}.")
    else:
        print(f"Sorry, that is not the correct word. The word is {roundWord}. You lose :(")


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()