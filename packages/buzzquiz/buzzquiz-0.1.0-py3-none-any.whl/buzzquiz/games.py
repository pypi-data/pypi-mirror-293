# Python 3.10
# 26/08/2024
"""Common games for Buzz! controllers"""

from buzzquiz import buzz
from buzzquiz.controllers import Button, Controller


def buzz_and_answer(
    expected_answer: str | Button,
    time_to_answer: float = 8,
    chances: int = 1,
    penalty: bool = False,
) -> Controller | None:
    """Press BUZZ and answer a question

    The expected answer must be a color, either as a string or as a Button.

    'time_to_answer' sets the time, in seconds, to answer the question once
    the player has pressed the BUZZ button.

    'chances' sets the number of chances one player has to answer the question.
    After exhausting all chances, the player is removed from the game. If
    'penalty' is True, the player won't be able to answer in the next round
    every time they fail to answer correctly.

    """
    buzz.init()

    players = [controller.id for controller in buzz.controllers]
    players_chances = {player: chances for player in players}
    in_penalty = None

    while True:
        # Buzz press
        round_players = [player for player in players if player != in_penalty]
        print("Press BUZZ to answer!")
        buzz.lights.blink(0.67, targets=round_players)
        event = buzz.get_event(
            trigger="on_press",
            buttons=["buzz"],
            controllers=round_players,
        )
        player = event.controller_id

        # Answer
        print(f"Player {player}! Press a color!")
        buzz.lights.timeout(time_to_answer, targets=[player], clear=True)
        event = buzz.get_event(
            trigger="on_press",
            buttons=["colors"],
            controllers=[player],
            timeout=time_to_answer,
        )
        buzz.lights.off([player])

        # Checking answer
        failed = False
        if not event:
            print("Timeout! Try again!")
            failed = True
        elif event.button != expected_answer:
            print(f"{event.button}! Wrong! Try again!")
            failed = True
        else:
            print(f"{event.button}! Correct! You win!")
            break
        if failed:
            players_chances[player] -= 1
            if players_chances[player] == 0:
                print("No more chances!")
                players.remove(player)
            if penalty:
                in_penalty = player

        # Checking if no players left
        if len(players) == 0:
            player = None
            print("No more players!")
            break

        print()

    buzz.lights.off()
    if player:
        print(f"Player {player} wins!")
    else:
        print("No winner!")
    return player
