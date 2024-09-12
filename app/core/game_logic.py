# simple function to checks who win
# decided a whole class would be overkill for this purposes
def determine_winner(choice1, choice2):
    pull =['rock', 'paper', 'scissors']
    if choice1 not in pull or choice2 not in pull:
        return None

    if choice1 == choice2:
        return 0
    elif (
        (choice1 == "rock" and choice2 == "scissors") or
        (choice1 == "paper" and choice2 == "rock") or
        (choice1 == "scissors" and choice2 == "paper")
    ):
        return 1
    else:
        return 2

