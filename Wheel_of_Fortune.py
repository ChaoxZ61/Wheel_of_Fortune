from unicodedata import name
from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players = {0: {"roundtotal": 0, "gametotal": 0, "name": ""},
           1: {"roundtotal": 0, "gametotal": 0, "name": ""},
           2: {"roundtotal": 0, "gametotal": 0, "name": ""},
           }

dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""
# Prevent duplicate word be selected
wordList = []


def readDictionaryFile():
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    global dictionary
    with open(dictionaryloc, "r") as wordDict:
        # make sure every words only contains lower case letters.
        readDict = wordDict.read().lower()
        dictionary = list(map(str, readDict.split("\n")))


def readTurnTxtFile():
    global turntext
    with open(turntextloc, "r") as turn:
        turntext = turn.read()


def readFinalRoundTxtFile():
    global finalroundtext
    # read in turn intial turn status "message" from file
    with open(finalRoundTextLoc, "r") as final:
        finalroundtext = final.read()


def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location
    with open(roundstatusloc, "r") as round:
        roundstatus = round.read()


def readWheelTxtFile():
    # init the Wheel name and store it in txt using the Config wheelloc file location 
    global wheellist
    wheellist.append("BANKRUPT")
    wheellist.append("LOSE A TURN")
    for i in range(100, 950, 50):
        wheellist.append(i)
    with open(wheeltextloc, "w") as wheelFile:
        for i in range(len(wheellist)):
            wheelFile.write(f"{wheellist[i]}\n")


def getPlayerInfo():
    global players
    # read in player names from command prompt input
    for i in players:
        # Check if name input is valid
        while True:
            name = input(f"\nPlease enter the name for player {i}:")
            if name.replace(" ", "").isalpha() and any(x.isspace() for x in name):
                break
            else:
                print("""\nInvalid input, please enter the participant\'s legel first name
                and last name and separate them by a space.\n""")
        players[i].update({"name": name})


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
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
    global blankWord
    global roundWord
    global wordList
    # reset blankWord to empty
    blankWord = []
    # choose a random word from the dictionary that are not composed of only vowel letters.
    while True:
        roundWord = dictionary[random.randint(0, len(dictionary) - 1)]
        if all(i in vowels for i in roundWord) == False and roundWord not in wordList:
            break
    wordList.append(roundWord)
    # make a list of the word with underscores instead of letters.
    for i in range(len(roundWord)):
        blankWord.append("_")


def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    for i in players.keys():
        players[i].update({"roundtotal": 0})
    # Return the starting player number (random)
    initPlayer = random.randint(0, 2)
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    getWord()
    return initPlayer


def guessletter(letter):
    global players
    global blankWord
    global roundWord
    # A trigger to check whether the player guess on a letter that is already revealed.
    repeated = False
    # Change position of found letter in blankWord to the letter instead of underscore.
    if letter in roundWord:
        # Penalize players for guessing the correct letter that is already revealed by ending their turn.
        if letter in blankWord:
            print(f"The letter {letter} is already revealed. Your turn is terminated as a penalty.\n")
            repeated = True
            goodGuess = True
        else:
            # find positions of all letters in the word.
            pos = [i for i in range(len(roundWord)) if roundWord.startswith(letter, i)]
            for i in pos:
                blankWord[i] = letter
            goodGuess = True
    else:
        goodGuess = False
    # return goodGuess= true if it was a correct guess 

    return goodGuess, repeated


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global roundWord
    # Get random value for wheellist
    wheelResult = wheellist[random.randint(0, len(wheellist) - 1)]
    print(f"The result of spin is: {wheelResult}\n")
    # Check for bankrupcy, and take action.
    if wheelResult == "BANKRUPT":
        print("It is so unfortunate, but you are bankrupted for this round.\n")
        players[playerNum].update({"roundtotal": 0})
        stillinTurn = False
    # Check for loose turn
    elif wheelResult == "LOSE A TURN":
        print("Unlucky, but better than bankrupcy, your turn is ended now.\n")
        stillinTurn = False
    # Get amount from wheel if not loose turn or bankruptcy
    else:
        print(f"Your award would be {wheelResult} if you guess a cononant correctly.\n")
        # Ask user for letter guess, ensure the input letter is a consonant
        while True:
            playerGuess = input("\nPlease Guess a consonant:").lower()
            if len(playerGuess) != 1 or playerGuess.isalpha() == False:
                print("Wrong input, please input a single cononant letter.\n")
            elif playerGuess in vowels:
                print("Please do not guess vowel letters, try again.\n")
            else:
                letter = playerGuess
                break
        # Use guessletter function to see if guess is in word
        guessedRight = guessletter(letter)
        # Change player round total if they guess right.
        if guessedRight[0] == True:
            if guessedRight[1] == False:
                newTotal = players[playerNum]["roundtotal"] + int(wheelResult)
                players[playerNum].update({"roundtotal": newTotal})
                print(f"""You got it! {wheelResult} has been added to your bank.
                Your new round total is:{players[playerNum]['roundtotal']}.
                The new hinted word is {''.join(blankWord)}\n""")
                stillinTurn = True
            else:
                stillinTurn = False
        else:
            print(f"The letter you guessed, {letter}, is not in the word. Your turn is ended.\n")
            stillinTurn = False

    return stillinTurn


def buyVowel(playerNum):
    global players
    global vowels
    global blankWord
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    if players[playerNum]["roundtotal"] < vowelcost:
        print("You don't have enough to buy vowel. Please get more from wheel spin first.\n")
        goodGuess = True
    else:
        while True:
            playerBuy = input("\nYou have enough to buy vowel, please pick a vowel to buy (a/e/i/o/u)").lower()
            if playerBuy.isalpha() == False or len(playerBuy) != 1:
                print("You did not enter a letter. Please try again.\n")
                continue
            elif playerBuy not in vowels:
                print("You did not enter a vowerl. Please try again.\n")
                continue
            else:
                newTotal = players[playerNum]["roundtotal"] - vowelcost
                players[playerNum].update({"roundtotal": newTotal})
                guessedRight = guessletter(playerBuy)
                if guessedRight[0] == True:
                    if guessedRight[1] == False:
                        print(f"""The vowel you bought,{playerBuy}, is in the word. 
                        The new hinted word looks like {''.join(blankWord)}.
                        Your new total is {newTotal}.\n""")
                        goodGuess = True
                        break
                    else:
                        goodGuess = False
                        break
                else:
                    print(f"""Sorry, but the vowel you bought,{playerBuy}, is not in the word. 
                    The hinted word,{''.join(blankWord)}, remains unchanged. 
                    You turn is ended and your new total is {newTotal}.\n""")
                    goodGuess = False
                    break

    return goodGuess


def guessWord(playerNum):
    global players
    global blankWord
    global roundWord

    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    playerGuess = input("\nPlease Enter the Word You Believe is the Word for this Round:")
    if playerGuess == roundWord:
        for i in range(len(roundWord)):
            blankWord[i] = roundWord[i]
        print("You Got It!\n")
    else:
        print("Sorry, the word you guessed is not right, your turn is ended.\n")
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  

    return False


def wofTurn(playerNum):
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (S)pin the wheel, (B)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    print(turntext.format(name=players[playerNum]["name"], word=''.join(blankWord)))
    stillinTurn = True
    while stillinTurn:

        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        choice = input("""\nPlease Choose an option from (S)pin, (B)uy vowel, and (G)uess 
        by entering the first letter of the option:""").lower()
        if (choice.strip().lower() == "s"):
            stillinTurn = spinWheel(playerNum)
        elif (choice.strip().lower() == "b"):
            stillinTurn = buyVowel(playerNum)
        elif (choice.lower() == "g"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option\n")


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    currentPlayer = initPlayer
    # Keep doing things in a round until the round is done ( word is solved)
    # While still in the round keep rotating through players
    # Use the wofTurn fuction to dive into each players turn until their turn is done.
    print(f"\nA new round with {players[initPlayer]['name']} goes first begins!\n")
    while True:
        wofTurn(currentPlayer)
        print(
            f"After {players[currentPlayer]['name']}'s turn, the current hinted word looks like: {''.join(blankWord)}\n")
        if "".join(map(str, blankWord)) == roundWord:

            # update each player's round total into their game totals.
            for i in players.keys():
                newGameTotal = players[i]["gametotal"] + players[i]["roundtotal"]
                players[i].update({"gametotal": newGameTotal})
            break
        if (currentPlayer == 0 or currentPlayer == 1):
            currentPlayer += 1
        else:
            currentPlayer = 0
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
    print(roundstatus.format(word=roundWord, name=players[currentPlayer]["name"]))


def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    checkList = {"R", "S", "T", "L", "N", "E"}

    # Find highest gametotal player and the player's respective game total.  They are playing.
    for i in players.keys():
        if players[i]["gametotal"] > players[winplayer]["gametotal"]:
            winplayer = i
    amount = players[winplayer]["gametotal"]
    # Print out instructions for that player and who the player is.
    print(finalroundtext.format(name=players[winplayer]['name'], total=amount))
    print(f"""In the final round, {', '.join(checkList)} will be automatically revealed.
    You would have a chance to guess 3 additional consonants and 1 additional vowel for free.
    After that, you will have only 1 chance to guess the word.
    If you get it right, {finalprize} will be added to your current game total. 
    If you don't, you will get nothing.""")
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    for i in checkList:
        guessletter(i.lower())
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(f"The current hinted word is: {''.join(blankWord)}.\n")
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    for i in range(3):
        guessedConsonant = []
        while True:
            consonant = input(f"\nPlease enter No.{i + 1} consonant you would like to guess:").lower()
            if consonant.isalpha == False or len(consonant) != 1:
                print("You did not enter a letter. Please try again.\n")
            elif consonant in vowels:
                print("You will have a chance to guess a vowel later. Please try again.\n")
            elif consonant in blankWord:
                print("The letter you guessed is already revealed. Please try again.\n")
            elif consonant in guessedConsonant:
                print("You already guessed thie letter. Please try again.\n")
            else:
                guessletter(consonant)
                guessedConsonant.append(consonant)
                break

    while True:
        vowel = input("\nPlease enter a vowel you would like to guess:").lower()
        if vowel.isalpha == False or len(vowel) != 1:
            print("You did not enter a letter. Please try again.\n")
        elif vowel not in vowels:
            print("You already used all the chances to guess consonants. Please try again.\n")
        elif vowel in blankWord:
            print("The letter you guessed is already revealed. Please try again.\n")
        else:
            guessletter(vowel)
            break

    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    print(f"After your guesses, the current hinted word looks like this: {''.join(blankWord)}.\n")
    # Get user to guess word
    finalGuess = input(
        "\nPlease take your final guess of the word. You only have five seconds to do so (theoratically):").lower()
    # If they do, add finalprize and gametotal and print out that the player won
    if finalGuess == roundWord:
        finalAward = finalprize + amount
        print(f"Congratulations! You guessed the word correctly. Your total prize is {finalAward}")
    else:
        print(f"Sorry you missed the word. The word is {roundWord}. Good luck Next Time!")


def main():
    gameSetup()

    for i in range(0, maxrounds):
        if i in [0, 1]:
            wofRound()
        else:
            wofFinalRound()


if __name__ == "__main__":
    main()
