#This is a Dice Rolling Simulator which takes your name, number of rounds you want play, and has you compete with the computer to see who wins.
import json
import os
import random

#Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        
    #Stores the dice roll for the player
    def roll_dice(self, dice):
        roll = dice.roll()
        print(f"You rolled a {roll}.")
        return roll

    #Stores the dice roll for the computer
    def roll_dice_computer(self, dice):
        roll = dice.roll()
        print(f"The computer rolled a {roll}.")
        return roll
    
    #Updates the score
    def update_score(self, roll):
        self.score += roll

#Dice class
class Dice:
    def __init__(self, sides = 6):
        self.sides = sides
        
    #Rolls the dice
    def roll(self):
        return random.randint(1, self.sides)

#Game class
class Game:
    def __init__(self, player_name, rounds):
        self.dice = Dice()
        self.player = Player(player_name)
        self.computer = Player("Computer")
        self.rounds = rounds
        
    #Main function to play the game
    def play_game(self):
            for round_number in range(1, self.rounds + 1):
                print(f"\nRound {round_number} of {self.rounds}:")
                self.round()
                if round_number != self.rounds:
                    again = input("\nPress enter to play again: ")
                    if again == "":
                        round_number += 1
                elif round_number == self.rounds:
                    next = input("\nPress enter to show the results: ")
                    if next == "":
                        self.results()

    #Updates the score after each round
    def round(self):
        player_roll = self.player.roll_dice(self.dice)
        computer_roll = self.computer.roll_dice_computer(self.dice)

        if player_roll > computer_roll:
            print("You won this round!")
            self.player.update_score(1)
        elif player_roll < computer_roll:
            print("The computer won this round!")
            self.computer.update_score(1)
        else:
            print("It's a tie!")
            
    #Shows the final score for each game and announces the winner
    def results(self):
        print("\nFinal Results: ")
        print(f"{self.player.name}: {self.player.score}")
        print(f"Computer: {self.computer.score}")

        if self.player.score > self.computer.score:
            print(f"{self.player.name} wins the game!")
        elif self.player.score < self.computer.score:
            print("The computer wins the game!")
        else:
            print("You tied with the computer!")

#Loads the player's results from a JSON file
def load(player_name, file_name="results.json"):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            results2 = json.load(f)
            return results2.get(player_name, {"player_wins": 0, "computer_wins": 0, "ties": 0})
    return {"player_wins": 0, "computer_wins": 0, "ties": 0}

#Saves the player's results to a JSON file
def save(player_name, results, file_name="results.json"):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            results2 = json.load(f)
    else:
        results2 = {}

    results2[player_name] = results

    with open(file_name, "w") as f:
        json.dump(results2, f)

#Main function that carries out the program
def main():
    print()
    print("Welcome to my Dice Rolling Game!")
    print("In order to play, follow the instructions on screen when prompted.")
    player_name = input("What is your name? ")
    rounds = int(input("How many rounds would you like to play? "))
    game = Game(player_name, rounds)

    
    results = load(player_name)

    #Starts the game
    answer = 1
    while answer == 1:
        game.play_game()
        
        #Updates and saves the player's and computer's results
        if game.player.score > game.computer.score:
            results["player_wins"] += 1
        elif game.player.score < game.computer.score:
            results["computer_wins"] += 1
        else:
            results["ties"] += 1
        save(player_name, results)
        

        #Separates the game results from the player's match history using a for loop to create a line according to the length of the player's name
        print()
        number = ""
        for num in player_name:
            number += "-"
        print(f"{number}-----------------")
       
        #Displays the player's match history
        print(f"\n{player_name}'s Match History:")
        print(f"{player_name}'s Wins: {results['player_wins']}")
        print(f"Computer Wins: {results['computer_wins']}")
        print(f"Ties: {results['ties']}")

        #Takes user input to determine if another game will be played
        answer = int(input("\nDo you want to play again? (1 = yes, 0 = no) "))
        if answer == 0:
            exit()
        elif answer == 1:
            game.player.score = 0
            game.computer.score = 0

if __name__ == "__main__":
    main()
    
