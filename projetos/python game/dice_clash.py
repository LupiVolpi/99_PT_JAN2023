import numpy as np

def clear_screen():
    print('\n' * 75)


class Player:

    def __init__(self, name="Jane Doe", matrix_size=3):
        self.name = str(name).capitalize()
        self.matrix = np.zeros((matrix_size, matrix_size))
        self.score = 0
        self.opponent = None

    def add_opponent(self, opponent):
        self.opponent = opponent

    def reset_matrix(self):
        self.matrix = np.zeros((self.matrix.shape[0], self.matrix.shape[1]))

    def roll_die(self):
        roll = np.random.randint(1, 7)
        print(f"Player {self.name}, you've rolled a {roll}!\n")
        return roll

    def place_die(self, die_roll):
        placed = False

        while not placed:
            # Ask for user input.
            col_to_place = int(input(
                f"Player {self.name}, in which column do you want to place your die? (0-{self.matrix.shape[0] - 1}): "
            ))

            # Check if chosen column has space to place die.
            there_are_empty_spaces = any(self.matrix[:, col_to_place] == 0)

            if not there_are_empty_spaces:
                print(f"The column you chose ({col_to_place}) is full. Choose another column.")
                print()
                continue

            # If there is at least 1 free space in column.
            else:
                for i in range(self.matrix.shape[0]):
                    if self.matrix[i][col_to_place] == 0:
                        self.matrix[i][col_to_place] = die_roll

                        placed = True
                        break

        if not self.opponent:
            raise ValueError(
                f"Player {self.name} needs to have an opponent for the game to work!"
            )

        else:
            self.remove_opponent_dice(die_roll, col_to_place)

    def remove_opponent_dice(self, die_roll, col_placed):
        for col in range(self.opponent.matrix.shape[0]):
            if col == col_placed:
                mask = self.opponent.matrix[:,col] == die_roll
                self.opponent.matrix[mask, col] = 0

    def calculate_score(self):
        self.score = 0

        for i in range(self.matrix.shape[1]):
            column = self.matrix[:, i]
            unique_numbers = np.unique(column)
            for number in unique_numbers:
                count = np.count_nonzero(column == number)
                if count == 1:
                    self.score += int(number)
                else:
                    self.score += int(number * count * count)


class Match:

    def __init__(self):
        name1 = input("Please enter the name for Player 1: ")
        print()
        name2 = input("Please enter the name for Player 2: ")
        print()
        matrix_size = int(input(f"How big do you want the board (3-5)?"))

        clear_screen()

        self.player1 = Player(name=name1.capitalize(), matrix_size=matrix_size)
        self.player2 = Player(name=name2.capitalize(), matrix_size=matrix_size)

        self.player1.add_opponent(self.player2)
        self.player2.add_opponent(self.player1)

        self.tutorial_player1 = Player(name="Tom", matrix_size=matrix_size)
        self.tutorial_player2 = Player(name="Jerry", matrix_size=matrix_size)

    def tutorial_stats(self):
        print(f"Player {self.tutorial_player1.name}'s matrix:")
        print(self.tutorial_player1.matrix, f"\nPlayer {self.tutorial_player1.name}'s score: {self.tutorial_player1.score}")
        print()
        print(f"Player {self.tutorial_player2.name}'s matrix:")
        print(self.tutorial_player2.matrix, f"\nPlayer {self.tutorial_player2.name}'s score: {self.tutorial_player2.score}")
        print()

    def tutorial(self):

        self.tutorial_player1.reset_matrix()
        self.tutorial_player2.reset_matrix()

        print(
            "In dice clash, each player's objective is to accumulate the most points with your dice"
            "\nwhile removing points from your opponent!"
            "\n"
            "\nEach player starts with their own empty grid, as such:\n"
        )

        self.tutorial_stats()

        input("Press ENTER to continue.")
        clear_screen()

        print("Taking turns, each player will roll a die from 1-6 and place it on a vacant space of their matrix.")
        print()

        self.tutorial_player1.matrix[0,0] = 3
        self.tutorial_player2.matrix[0,2] = 5

        self.tutorial_player1.calculate_score()
        self.tutorial_player2.calculate_score()

        self.tutorial_stats()

        input("Press ENTER to continue.")
        clear_screen()

        print("Each player's score is the sum of all dice they currently have on their own matrix.")
        print()
        print("If a player has two or more equal dice on the same column, \n"
              "these dice will be summed and multiplied by how many repeated dice they have!")
        print()

        self.tutorial_player1.matrix[1,0] = 3

        self.tutorial_player1.calculate_score()
        self.tutorial_player2.calculate_score()

        self.tutorial_stats()

        input("Press ENTER to continue.")
        clear_screen()

        print("But be careful! If your opponent places a dice you already have in the same column \n"
              "your dice of that value will disappear and your score will go down!")
        print()

        self.tutorial_player2.matrix[0,0] = 3
        self.tutorial_player1.matrix[0:2, 0] = 0

        self.tutorial_player1.calculate_score()
        self.tutorial_player2.calculate_score()

        self.tutorial_stats()

        input("Press ENTER to continue.")
        clear_screen()

        print("That's all you need to know about dice clash!")
        again = input("Do you want to read the tutorial again (y/n)? -> ")

        if again == "y":
            self.tutorial()

    def player_turn(self, player):
        print(f"Player {player.name}, your turn.")

        roll = player.roll_die()

        player.place_die(die_roll=roll)

        self.player1.calculate_score()
        self.player2.calculate_score()

    def display_game_stats(self):
        clear_screen()
        print(f"Player {self.player1.name}'s matrix:")
        print(self.player1.matrix, f"\nPlayer {self.player1.name}'s score: {self.player1.score}")
        print()
        print(f"Player {self.player2.name}'s matrix:")
        print(self.player2.matrix, f"\nPlayer {self.player2.name}'s score: {self.player2.score}")
        print()
        input("Press ENTER to continue the game.")
        print()

    def player_matrix_is_full(self, player):
        return player.matrix.all() != 0

    def both_matrixes_are_full(self):
        return self.player1.matrix.all() != 0 and self.player2.matrix.all() != 0

    def declare_winner(self):
        if self.player1.score > self.player2.score:
            print(f"Player {self.player1.name} wins! :)")
        elif self.player2.score > self.player1.score:
            print(f"Player {self.player2.name} wins! :)")
        elif self.player2.score == self.player1.score:
            print("It's a tie! Both players win! :)")

    def play(self):
        keep_playing = True

        print(f"Welcome to Dice Clash!")
        tutorial = input("Would you like a tutorial on how to play the game (y/n)? -> ")
        print()

        if tutorial == "y":
            self.tutorial()

        while keep_playing:
            if not self.player_matrix_is_full(self.player1):
                self.player_turn(self.player1)
                self.display_game_stats()

            elif self.both_matrixes_are_full():
                self.declare_winner()
                keep_playing = False

            if not self.player_matrix_is_full(self.player2):
                self.player_turn(self.player2)
                self.display_game_stats()

            elif self.both_matrixes_are_full():
                self.declare_winner()
                keep_playing = False

        print()
        print("Thank you for playing!")
        play_again = input("Would you like to play again (y/n)? -> ")

        if play_again == "y":
            clear_screen()
            self.player1.reset_matrix()
            self.player2.reset_matrix()

            self.play()

########################################################################################################################

match = Match()
match.play()