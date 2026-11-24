from datetime import date, timedelta

import pytest

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck

TODAY = date(2026, 11, 6)
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
IN_3_DAYS = TODAY + timedelta(days=3)

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

def test_deck_with_spaces_only_name_is_refused():
    with pytest.raises(ValueError):
        Deck('   ')
        
def test_deck_empty_name_is_refused():
    with pytest.raises(ValueError):
        Deck('')

def test_deck_trimmed_name():
    deck = Deck(" A1 verbs ")
    assert deck.name == "A1 verbs"

def test_cards_count_due_today():
    card1 = Card("question1", "answer1", YESTERDAY, 1)
    card2 = Card("question2", "answer2", TODAY, 1)
    card3 = Card("question3", "answer3", TOMORROW, 1)
    card4 = Card("question4", "answer4", YESTERDAY, position=1, box=5, status=CardStatus.RETIRED)
    deck = Deck('my_deck')
            
    deck.add_card(card1)
    deck.add_card(card2)
    deck.add_card(card3)
    deck.add_card(card4)

    due_today = deck.due_count(TODAY)

    assert due_today == 2

def test_empty_deck_gives_zero_due_count():
    deck = Deck('my_deck')
    due_today = deck.due_count(TODAY)
    
    assert due_today == 0

def test_next_due_for_retired_is_none():
    deck = Deck('my_deck')

    card1 = Card("question1", "answer1", YESTERDAY, position=1, box=1, status=CardStatus.RETIRED)
    card2 = Card("question2", "answer2", YESTERDAY, position=2, box=1, status=CardStatus.RETIRED)
    deck.add_card(card1)
    deck.add_card(card2)
    
    assert deck.next_due() is None

def test_next_due_date():
    deck = Deck('my_deck')

    card1 = Card("question1", "answer1", IN_3_DAYS, position=1, box=1)
    card2 = Card("question2", "answer2", TOMORROW, position=2, box=1)
    deck.add_card(card1)
    deck.add_card(card2)
    
    assert deck.next_due() == TOMORROW

