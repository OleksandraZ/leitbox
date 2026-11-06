from datetime import date, timedelta

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck

TODAY = date(2026, 11, 6)
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)




# Tests to write:

# add_card: after adding one card, len(deck.cards) == 1.
# AC-04.1: three cards, due yesterday, today and tomorrow, added in the order today, tomorrow, yesterday. Expect [yesterday's, today's]. Compare the questions with [c.question for c in result].
# AC-04.2: two cards due the same day in box 3 and box 1. Add the box 3 card first and expect box 1 first.
# Tie-break: same due date, same box, positions 2 and 1. Expect position 1 first.
# A retired card that's past its due date is left out.
# Nothing due: only a card due tomorrow → [].
# Two decks don't share a list: create Deck("A") and Deck("B"), add a card to A, and check that B still has 0 cards.


def test_add_card_to_deck_and_check_len():
    card = Card("question", "answer", TODAY, 1)
    deck = Deck('my_deck')
    deck.add_card(card)
    assert len(deck.cards) == 1 

def test_add_cards_check_due():
    card1 = Card("question1", "answer1", TODAY, 1)
    card2 = Card("question2", "answer2", TOMORROW, 1)
    card3 = Card("question3", "answer3", YESTERDAY, 1)

    deck = Deck('my_deck')

    deck.add_card(card1)
    deck.add_card(card2)
    deck.add_card(card3)

    assert deck.due_cards(TODAY) == [card3, card1]

def test_order_of_due_cards():
    card1 = Card("question1", "answer1", YESTERDAY, position=1, box=3)
    card2 = Card("question2", "answer2", YESTERDAY, position=2, box=1)

    deck = Deck('my_deck')
    
    deck.add_card(card1)
    deck.add_card(card2)

    assert deck.due_cards(TODAY) == [card2, card1]

def test_tie_break():
    card1 = Card("question1", "answer1", YESTERDAY, position=1, box=1)
    card2 = Card("question2", "answer2", YESTERDAY, position=2, box=1)

    deck = Deck('my_deck')
    
    deck.add_card(card2)
    deck.add_card(card1)

    assert deck.due_cards(TODAY) == [card1, card2]

def test_retired_card_not_shown():
    card1 = Card("question1", "answer1", YESTERDAY, position=1, box=1, status=CardStatus.RETIRED)
    card2 = Card("question2", "answer2", YESTERDAY, position=2, box=1)
    
    deck = Deck('my_deck')
        
    deck.add_card(card1)
    deck.add_card(card2)

    assert deck.due_cards(TODAY) == [card2]

def test_no_cards_due():
    card1 = Card("question1", "answer1", TOMORROW, position=1)
    card2 = Card("question2", "answer2", TOMORROW, position=2)

    deck = Deck('my_deck')
            
    deck.add_card(card1)
    deck.add_card(card2)
    
    assert deck.due_cards(TODAY) == []

def test_two_decks_do_not_share_a_list():
    card1 = Card("question1", "answer1", TOMORROW, 1)
    
    deck1 = Deck('my_deck_1')
    deck2 = Deck('my_deck_2')
                
    deck1.add_card(card1)
        
    assert len(deck1.cards) == 1
    assert len(deck2.cards) == 0
