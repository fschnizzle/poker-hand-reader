# Poker Hand Evaluator

This program is designed to evaluate a given hand of cards in the game of poker. The user inputs their own hand and the community cards (flop, turn, and river) and the program will determine the highest possible hand type the user can make given the cards they have.

The program includes the following hand type functions:

- Royal flush
- Straight flush
- Four of a kind
- Full house
- Flush
- Straight
- Three of a kind
- Two pair
- Pair
- High card
  The program also includes a function for inputting and validating the cards in the user's hand and the community cards.

## Usage

1. Run the program and input your hand using the format "rank of suit" (e.g. "ah" for "Ace of Hearts", "7d" for "Seven of Diamonds").
2. Input the community (river) cards, if any, in the same format.
3. The program will output the highest possible hand type the user can make with their given cards.

## Areas for Improvement

- Adding more user input validation to ensure all inputs are valid card inputs
- Adding more functionality to the program such as the ability to input multiple hands to compare
- Expanding the program to include more variations of poker such as Omaha or Texas Hold'em
- Instead of using the input() function, use a GUI to make the input more user-friendly, or alternatively allow for a single line entry of card details to speed up the process
- Instead of using a long list of if-else statements, use a more efficient method such as a hash table to check for the highest hand type.
