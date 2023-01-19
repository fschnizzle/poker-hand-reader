from collections import Counter

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = ranks.index(rank)
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
    ranks = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'}
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

def determine_hand_type(hand, river):
    hand_types = [royal_flush, straight_flush, four_of_a_kind, full_house, flush, straight, three_of_a_kind, two_pair, pair, high_card]
    for hand_type in hand_types:
        result = hand_type(hand, river)
        if result:
            hand_type_name = hand_type.__name__.replace("_", " ")
            print(f"\nHand type: {hand_type_name}")
            return result
    print("No hand detected")

"""
Helper Functions
"""
def value_count(N, hand, river= set([])):
    combined_hand = hand.union(river)
    ranks = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    value_count_list = []
    for rank in ranks:
        count = 0
        rank_cards = []
        for card in combined_hand:
            if card.rank == rank:
                count += 1
                rank_cards.append(card)
        if count == N:
            value_count_list.append(rank_cards)
    return value_count_list

def complete_hand(sig_hand, hand, river):
    combined_hand = hand.union(river)
    final_hand = sig_hand.copy()
    num_missing_cards = 5 - len(sig_hand)
    remaining_cards = combined_hand.difference(sig_hand)
    remaining_cards = sorted(remaining_cards, key=lambda card: card.value, reverse=True)
    final_hand.extend(remaining_cards[:num_missing_cards])
    return final_hand

"""
Hand type functions
"""
def high_card(hand, river=set([])):
    combined_hand = hand.union(river)
    sorted_hand = sorted(combined_hand, key=lambda card: card.value, reverse=True)
    final_hand = []
    final_hand.append(sorted_hand[0:5])
    return final_hand

def pair(hand, river=set([])):
    combined_hand = hand.union(river)
    rank_count = {}
    for card in combined_hand:
        if card.rank not in rank_count:
            rank_count[card.rank] = 1
        else:
            rank_count[card.rank] += 1
    final_list = []
    for rank, count in rank_count.items():
        if count >= 2:
            pair_cards = [card for card in combined_hand if card.rank == rank]
            other_cards = [card for card in combined_hand if card.rank != rank]
            other_cards = sorted(other_cards, key=lambda card: card.value, reverse=True)
            final_sort = pair_cards + other_cards[:3]
            if final_sort not in final_list:
                final_list.append(final_sort)
    return final_list

def two_pair(hand, river=set([])):
    combined_hand = hand.union(river)
    rank_count = {}
    for card in combined_hand:
        if card.rank not in rank_count:
            rank_count[card.rank] = 1
        else:
            rank_count[card.rank] += 1
    pair_list = []
    for rank, count in rank_count.items():
        if count >= 2:
            pair_cards = [card for card in combined_hand if card.rank == rank]
            other_cards = [card for card in combined_hand if card.rank != rank]
            pair_list.append(pair_cards)
    two_pair_list = []
    if len(pair_list) >= 2:
        for i in range(len(pair_list)):
            for j in range(i+1, len(pair_list)):
                two_pair_hand = pair_list[i][:2] + pair_list[j][:2]
                other_cards = [card for card in combined_hand if card not in two_pair_hand]
                other_cards = sorted(other_cards, key=lambda card: card.value, reverse=True)
                final_sort = two_pair_hand + [other_cards[0]]
                two_pair_list.append(final_sort)
    return two_pair_list

def three_of_a_kind(hand, river=set([])):
    three_of_a_kind_list = value_count(3, hand, river)
    for i in range(len(three_of_a_kind_list)):
        three_of_a_kind_list[i] = complete_hand(three_of_a_kind_list[i][:3], hand, river)
    return three_of_a_kind_list

def four_of_a_kind(hand, river=set([])):
    four_of_a_kind_list = value_count(4, hand, river)
    for i in range(len(four_of_a_kind_list)):
        four_of_a_kind_list[i] = complete_hand(four_of_a_kind_list[i][:4], hand, river)
    return four_of_a_kind_list

def flush(hand, river = set([])):
    combined_hand = hand.union(river)
    flush_list = []
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    for suit in suits:
        suit_cards = [card for card in combined_hand if card.suit == suit]
        if len(suit_cards) >= 5:
            flush_list.append(sorted(suit_cards, key=lambda card: card.value, reverse=True)[:5])
    return flush_list

def straight(hand, river = set([])):
    combined_hand = hand.union(river)
    straight_list = []
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    # Create a list of lists where each sublist contains all cards of a specific rank
    rank_cards = [[card for card in combined_hand if card.rank == rank] for rank in ranks]
    for i in range(len(ranks) - 4):
        straight = []
        for j in range(i, i + 5):
            straight += rank_cards[j]
        if len(straight) >= 5:
            cur_straight = sorted(straight, key=lambda card: (ranks.index(card.rank), card.suit), reverse=True)[:5]
            if cur_straight not in straight_list:
                straight_list.append(cur_straight)
            # Check for a straight where Ace is the low card
        if rank_cards[0] and rank_cards[-4]:
            straight = rank_cards[0] + rank_cards[-4] + rank_cards[-3] + rank_cards[-2] + rank_cards[-1]
        if len(straight) >= 5:
            cur_straight = sorted(straight, key=lambda card: (ranks.index(card.rank), card.suit), reverse=True)[:5]
            if cur_straight not in straight_list:
                straight_list.append(cur_straight)
    return straight_list

def full_house(hand, river=set([])):
    combined_hand = hand.union(river)
    rank_count = {}
    for card in combined_hand:
        if card.rank not in rank_count:
            rank_count[card.rank] = 1
        else:
            rank_count[card.rank] += 1
    three_of_a_kind = None
    pair = None
    for rank, count in rank_count.items():
        if count == 3:
            three_of_a_kind = [card for card in combined_hand if card.rank == rank]
        elif count == 2:
            pair = [card for card in combined_hand if card.rank == rank]
    if three_of_a_kind is not None and pair is not None:
        full_house_cards = three_of_a_kind + pair
        return [sorted(full_house_cards, key=lambda card: card.value, reverse=True)[:5]]
    else:
        return []
        
def straight_flush(hand, river):
    combined_hand = hand.union(river)
    flush_list = flush(combined_hand)
    straight_flush_list = []
    for flush_hand in flush_list:
        straight_list = straight(set(flush_hand))
        for consec in straight_list:
            if len(set([card.suit for card in consec])) == 1:
                straight_flush_list.append(consec)
    return straight_flush_list

def royal_flush(hand, river):
    combined_hand = hand.union(river)
    royal_flush_cards = {Card('Ace', 'Hearts'), Card('King', 'Hearts'), Card('Queen', 'Hearts'), Card('Jack', 'Hearts'), Card('10', 'Hearts')}
    
    for card in royal_flush_cards:
        if card not in combined_hand:
            return []
    return [list(royal_flush_cards)]




def main():
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    deck = [Card(rank, suit) for suit in suits for rank in ranks]

    # User prompted to enter their card details
    print("User Hand Card Details\n")
    user_hand = get_user_hand(deck)


    # User prompted to enter the river's card details
    print("River Card Details\n")
    river = get_river(deck)


    # OUTPUT
    best_hand = determine_hand_type(user_hand, river)[0]
    print("Containing: ")
    for card in best_hand:
        print(f"  - {card}")
    print("\n")
    
if __name__ == "__main__":
    main()
