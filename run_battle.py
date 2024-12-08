"""Test script."""
from pykmn.engine.gen1 import Battle, Player, Choice, Pokemon
from pykmn.engine.common import ResultType, Slots
from pykmn.engine.protocol import parse_protocol
import random
from pykmn.engine.libpkmn import libpkmn_trace


# Need to 'translate'
# - moves
# - weird pokemon names such as nido f nido m


# https://pokepast.es/cc9b111c9f81f6a4
team1 = [
    Pokemon(species="Starmie", moves=("Psychic", "Blizzard", "Thunder Wave", "Recover"),extra={'level': 1}),
    Pokemon(species="Exeggutor", moves=("Sleep Powder", "Psychic", "Double-Edge", "Explosion"),extra={'level': 1}),
    Pokemon(species="Alakazam", moves=("Psychic", "Seismic Toss", "Thunder Wave", "Recover"),extra={'level': 1}),
    Pokemon(species="Chansey", moves=("Ice Beam", "Thunderbolt", "Thunder Wave", "Soft-Boiled"),extra={'level': 1}),
    Pokemon(species="Snorlax", moves=("Body Slam", "Reflect", "Earthquake", "Rest"),extra={'level': 1}),
    Pokemon(species="Tauros", moves=("Body Slam", "Hyper Beam", "Blizzard", "Earthquake"),extra={'level': 1}),
]

team2 = [
    Pokemon(species="Magikarp", moves=("Tackle",),extra={'level': 100}),
    Pokemon(species="Chansey", moves=("Tackle",),extra={'level': 1}),

]

# https://pokepast.es/7f1c2e78e6ba3194
team3 = [
    Pokemon(species="Jynx", moves=("Lovely Kiss", "Blizzard", "Psychic", "Rest")),
    Pokemon(species="Starmie", moves=("Psychic", "Thunderbolt", "Thunder Wave", "Recover")),
    Pokemon(species="Alakazam", moves=("Psychic", "Seismic Toss", "Thunder Wave", "Recover")),
    Pokemon(species="Chansey", moves=("Seismic Toss", "Reflect", "Thunder Wave", "Soft-Boiled")),
    Pokemon(species="Snorlax", moves=("Body Slam", "Reflect", "Self-Destruct", "Rest")),
    Pokemon(species="Tauros", moves=("Body Slam", "Hyper Beam", "Blizzard", "Earthquake")),
]


def run_battle(log: bool = False) -> None:
    """Runs a Pokémon battle.

    Args:
        log (`bool`, optional): Whether to log protocol traces. Defaults to `True`.
    """
    battle = Battle(
        p1_team=team1,
        p2_team=team2,
    )
    slots: Slots = Slots(([p[0] for p in team1], [p[0] for p in team2]))

    (result, trace) = battle.update(Choice.PASS(), Choice.PASS())

    if log:
        print("---------- Battle setup ----------\nTrace: ")
        for msg in parse_protocol(trace, slots):
            print(f"* {msg}")
    # initialise pokemon with slot 1
    choice = 1
    while result.type() == ResultType.NONE:
        if log:
            print(f"\n------------ Choice {choice} ------------")
        choice += 1

        p1_choices = battle.possible_choices_raw(Player.P1, result)
        print(battle.possible_choices(Player.P1, result)) # Need to map these choices
        p1_choice = p1_choices[random.randrange(len(p1_choices))]
        p2_choices = battle.possible_choices_raw(Player.P2, result)
        print(battle.possible_choices(Player.P2, result)) # When a battle choice is chosen, potentially change 
        p2_choice = p2_choices[random.randrange(len(p2_choices))]
        if log:
            print(f"Player 1: {p1_choice}\nPlayer 2: {p2_choice}")
        (result, trace) = battle.update_raw(p1_choice, p2_choice)

        if log:
            print("\nTrace:")
            for msg in parse_protocol(trace, slots):
                print("* " + msg)

run_battle(log=True)