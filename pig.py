import random
import argparse

class Player:
    """
        The Player class represents a player in the Pig game.

        Attributes:
            name (str): The name of the player.
            score (int): The player's current score, initialized to 0.

        Methods:
            resetScore(): Resets the player's score to 0.
            addToScore(points): Adds the given points to the player's score.
            getName(): Returns the player's name.
        """
    def __init__(self, name):
        """
               Initializes a new Player object with the given name and sets the score to 0.

               Args:
                   name (str): The name of the player.
               """
        self.name = name
        self.score = 0

    def resetScore(self):
        """Resets the player's score to 0."""

        self.score = 0

    def addToScore(self,points):
        """
                Adds the given number of points to the player's current score.
                Args:
                    points (int): The number of points to add.
        """
        self.score += points

    def getName(self):
        """Returns the player's name."""

        return self.name




class Game:
    """
        The Game class represents the Pig dice game.

        Attributes:
            players (list of Player): A list of Player objects participating in the game.
            scoreToWin (int): The score required to win the game (default is 100).
            current_player (int): The index of the current player in the players list.
            rulesMessage (str): A message displaying the rules of the game.

        Methods:
            rollDie(): Rolls a die and returns a random number between 1 and 6.
            switchPlayer(): Switches to the next player in the list.
            turn(player): Handles the player's turn, including rolling the die and deciding to hold or continue.
            is_winner(player, turnScore=0): Checks if the player has won the game.
            printScores(): Displays the current scores of all players.
            play(): Starts the game loop where players take turns until a winner is determined.
        """
    rulesMessage = '''The rules of Pig are simple. The game features two players, whose goal is to reach 100 points first. 
    Each turn, a player repeatedly rolls a die until either a 1 is rolled or the player holds and scores the sum of the
rolls (i.e. the turn total). At any time during a player's turn, the player is faced with two decisions:
- roll: If the player rolls a
    1: the player scores nothing and it becomes the opponent's turn.
    2 - 6: the number is added to the player's turn total and the player's turn continues.
- hold: The turn total is added to the player's score and it becomes the opponent's turn.'''
    def __init__(self,player_names):
        """
                Initializes a new Game object with the given player names.

                Args:
                    player_names (list of str): A list of player names.
                """
        self.players = [Player(name) for name in player_names]
        self.scoreToWin = 100
        self.current_player = 0

    def rollDie(self):
        """
               Simulates rolling a six-sided die and returns the result.

               Returns:
                   int: A random number between 1 and 6 (inclusive).
               """
        maxNumber = 6
        minNumber = 1
        number = random.randint(minNumber,maxNumber)
        return number

    def switchPlayer(self):
        """
                Switches to the next player in the list. Cycles back to the first player if necessary.
                """
        #Using module to cycle back to the beginning of the list
        self.current_player = (self.current_player + 1) % len(self.players)

    def turn(self,player):
        """
                Handles the player's turn by rolling the die or holding.

                The player can keep rolling until a 1 is rolled (in which case their turn ends with no points)
                or decide to hold and add the accumulated points to their score.

                Args:
                    player (Player): The player whose turn it is.
                """
        print("It's {0} player's turn".format(player.getName()))
        turn_score = 0

        while True:
            roll = self.rollDie()
            print("You rolled: {0}".format(roll))
            if roll == 1:
                print("No points for you!")
                print("Your turn is over")
                break
            else:
                turn_score += roll
                print("Your turn score is: {0}".format(turn_score))
                print("Your total score is: {0}".format(turn_score+player.score) )

                #Ask user if they want to hold or continue rolling
                if self.is_winner(player,turn_score):
                    print("Winner")
                    break
                while True:
                    userInput = input("Do you want to Hold or Roll the die again? Enter 'h' or 'r': ").strip()
                    if userInput.lower() in ['h', 'r', 'hold', 'roll']:
                        #we want to exit the while loop
                        break
                    else:
                        print('Your input is invalid. Enter "h", "hold" to hold or "r", "roll" to roll the die again.')

                if userInput.lower() in ['h','hold']:
                    player.addToScore(turn_score)
                    print("{0} is holding. Total Score is: {1}".format(player.name,player.score))
                    break

    def is_winner(self,player,turnScore=0):
        """
                Checks if the player has reached or exceeded the score required to win.

                Args:
                    player (Player): The player whose score is being checked.
                    turnScore (int, optional): The score accumulated during the current turn. Default is 0.

                Returns:
                    bool: True if the player has won, otherwise False.
                """
        if player.score >= self.scoreToWin:
            return True
        elif (turnScore+player.score) >= self.scoreToWin:
            player.score = turnScore+player.score
            return True
        else:
            return False

    def printScores(self):
        """Prints the current scores of all players."""

        print("*********** Score Card ***********")

        for player in self.players:
            print("{0} : {1} points".format(player.name,player.score))

        print("*********** Score Card ***********")


    def play(self):
        """Starts the game, allowing players to take turns until a winner is determined."""

        print("Starting game of Pig.............")
        print("-"*50)
        print(self.rulesMessage)
        print("-"*50)
        keepGoing = True
        while keepGoing:
            currentPlayer = self.players[self.current_player]
            self.turn(currentPlayer)

            if self.is_winner(currentPlayer):
                keepGoing = False
            #if no winner yet
            self.printScores()

            self.switchPlayer()


def main(numPlayers = 0):
    """
        Handles the setup for the game, including player input.

        Args:
            numPlayers (int, optional): The number of players in the game. Default is 0 (prompt the user for input).

        Returns:
            list: A list of player names.
        """
    players = []
    while True:
        try:
            if numPlayers == 0 or numPlayers < 2:
                numPlayers = int(input("Enter number of players: "))
            # we need a minimum number of players of 2 start the game
            if numPlayers < 2:
                print("Minimum number of players to start the game is 2. Please retry.")
                continue
            break
        except ValueError:
            print("That is not a number. Please enter a number")
    for i in range(1, numPlayers+1):
        while True:
            name = input("Enter name of player {0} ".format(i))
            if name:
                players.append(name)
                break
            else:
                print("Enter a valid name")
    return players

if __name__ == "__main__":
    """
        Main entry point for the game. Handles command-line arguments and game loop.
        """
    #Getting players info
    parser = argparse.ArgumentParser()
    parser.add_argument("--numPlayers", help="URL to the datafile", type=str, required=False)
    args = parser.parse_args()
    numPlayers = 0
    try:
        if args.numPlayers:
            numPlayers = int(args.numPlayers)

    except ValueError:
        print("Value provided not a number")
        raise SystemExit
    keepPlaying = True
    while keepPlaying:

        players = main(numPlayers)


        game = Game(players)
        game.play()
        userInput = input("Do you want to start a new game? y/n").strip().lower()
        if userInput not in ["y","yes"]:
            print("Good Bye.........")
            print("See you soon-------------------")
            keepPlaying = False



    
