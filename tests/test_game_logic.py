from app.core.game_logic import determine_winner

def test_determine_winner():
    assert determine_winner("rock", "scissors") == 1
    assert determine_winner("paper", "rock") == 1
    assert determine_winner("scissors", "paper") == 1
    assert determine_winner("rock", "paper") == 2
    assert determine_winner("paper", "scissors") == 2
    assert determine_winner("scissors", "rock") == 2
    assert determine_winner("rock", "rock") == 0
    assert determine_winner("paper", "paper") == 0
    assert determine_winner("scissors", "scissors") == 0
    assert determine_winner("qwerty", "ytrewq") == None
    assert determine_winner("", "") == None
