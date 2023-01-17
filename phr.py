from collections import Counter

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))

def get_card_input(deck, existing_cards):
    card_input = input("Enter the card (e.g. 'AH' for Ace of Hearts): ")
    suit_input = card_input[-1].lower()
    rank_input = card_input[:-1].upper()
    suits = {'c': 'Clubs', 'd': 'Diamonds', 'h': 'Hearts', 's': 'Spades'}
    ranks = {'A': 'Ace', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King'}
    if suit_input not in suits:
        print("Invalid suit input. Please enter a valid suit (c, d, h, s).")
        return None
    if rank_input not in ranks:
        print("Invalid rank input. Please enter a valid rank (2-10, J, Q, K, A).")
        return None
    suit_input = suits[suit_input]
    rank_input = ranks[rank_input]
    card_to_add = Card(rank_input, suit_input)
    if card_to_add in deck and card_to_add not in existing_cards:
        return card_to_add
    elif card_to_add in existing_cards:
        print(f"{card_to_add} already in the existing cards.")
        return None
    else:
        print(f"{card_to_add} not in the deck.")
        return None

def get_user_hand(deck):
    existing_cards = set()
    while len(existing_cards) < 2:
        card = get_card_input(deck, existing_cards)
        if card:
            existing_cards.add(card)
            deck.remove(card)
            print(f"{card} added to your hand.")
    return existing_cards

def get_river(deck):
    river = set()

    # Flop Input
    input_flop = input("Enter flop details (y/n) ?").lower()
    if input_flop == "y":
        while len(river) < 3:
            card = get_card_input(deck, river)
            if card:
                river.add(card)
                deck.remove(card)
                print(f"{card} added to the flop.")

        # Turn Input
        input_turn = input("Enter turn details (y/n) ?").lower()
        if input_turn == "y":
            while len(river) < 4:
                card = get_card_input(deck, river)
                if card:
                    river.add(card)
                    deck.remove(card)
                    print(f"{card} added to the turn.")

            # River Input
            input_river = input("Enter river details (y/n) ?").lower()
            if input_river == "y":
                while len(river) < 5:
                    card = get_card_input(deck, river)
                    if card:
                        river.add(card)
                        deck.remove(card)
                        print(f"{card} added to the river.")
    return river

"""
Hand Type Condition Functions
"""

def flush(hand, river):
    combined_hand = hand.union(river)
    flush_list = []
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    for suit in suits:
        suit_cards = [card for card in combined_hand if card.suit == suit]
        if len(suit_cards) >= 5:
            flush_list.append(sorted(suit_cards, key=lambda card: card.rank, reverse=True)[:5])
    return flush_list




def main():
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    deck = [Card(rank, suit) for suit in suits for rank in ranks]

    # User prompted to enter their card details
    print("User Hand Card Details\n")
    user_hand = get_user_hand(deck)
    print("\n")

    # User prompted to enter the river's card details
    print("River Card Details\n")
    river = get_river(deck)

    # Prints user hand
    print("\n")
    print("Your hand:")
    for card in user_hand:
        print(f"{card}")

    # Prints river
    print("\n")
    print("River:")
    for card in river:
        print(f"{card}")


    print(f"flush contains: ")
    print(len(flush(user_hand, river)))
    for card in flush(user_hand, river)[0]:
        # print(f"{card.rank}, {card.suit}")
        print(f"{card}")
    
if __name__ == "__main__":
    main()
