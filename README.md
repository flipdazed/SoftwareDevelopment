# Motivation
The module, "Software Development", consists of deliberately badly written code providing the basis for a series of good coding practices. The attempt was to clean up the code to a useable state using methods learned through lectures and tutorials.

# Repository Contents

The game is run from:

- `cardgame.py` : The debug output level can be adjusted in this file

The settings are configured in:

- `config.py` : Containing a dictionary of game parameters

Other relevant files for the running of the game:

- `test.py` : Unit tests for the base classes and settings
- `game_engine.py` : Contains the `game()` class that instantiates players from `actors.py`
- `actors.py` : The classes for the players and central deck
- `common.py` : Common routines inherited by the player and deck classes
- `logs.py` : Logging routines
- `game_art.py` : Game art including an alternative welcome message
- `logging_colorer.py` : Colouring parameters for the logger
- `logging_formatter.py` : Formatting for the logger

Other folders in this directory:

- `docs/modifiedcode/` : Modified code flow diagrams and dependencies
- `docs/originalcode/` : Original code flow diagrams
- `docs/usertests/` : User feedback summary and response sheets


# Improved Code Structure
!["File Relationships"](docs/modifiedcode/relationships.png?raw=True "File Relationships")

# Game Overview 
To introduce the game, and for simplicity, we will assume certain settings and will denote in *italics* that a parameter can be adjusted by the file `config.py`.

## Setting up the game
 - The game is played by two **Players**: the real-life user, **The Player**, competing against the computer, **The AI**.
 - Each Player is assigned a **Player Deck** that is individual to each player consisting of *10* Cards, *2 Squires and 8 Serfs*.
 - Each Player is assigned a **Discard Pile (Discard Deck)**, which starts empty.
 - Each Player is assigned an **Active Hand**, which starts empty.
 - Each Player is assigned a **Player Hand**, which starts empty.
 - A **Central Deck** of *36* Cards is also created that consists of *a variety* of different Cards.
 - A **Central Active Deck** will begin empty.
 - Players are both assigned *30* **Health** at the beginning of a **Game** instance.
 - A **Supplement** is identical to a normal Card in this game and has no special functionality at this stage. However, they are treated as separate entities in the code and UI to allow for future development. They are played and bought as normal Cards.

The game is set up through the function `new()` within the class `Game()` in `game_engine.py`.
Players are managed by the `User()` and `Computer()` classes found in `Actors.py`.
The Central Deck and Central Active Deck are managed by the class, `Central()` also found in `Actors.py`

### Settings
The settings available to configure for gameplay are:

 - The properties of Cards (Attack, Name, Cost, Money and define custom variants)
 - The variety of Cards in the Player Deck for each Player
 - The variety of Cards Cards in the Central Deck
 - Supplements in the Central Deck
 - The number of Cards that constitute a Player Hand for each Player
 - The starting Health for each Player
 - The Name of each Player

These can be configured in the file `config.py`.

#### Cards
Each **Card** has the properties which will be used in the following discussion:
 
 - **Name** (e.g. Archer)
 - **Cost**
 - **Attack**
 - **Money**

This is managed by the class `Card()` found in `common.py`.
 
## Game Instances
A **Game** consists of **Rounds**, described later, which continue until either player has below 1 health or there are no remaining Cards in the Central Deck. A Game instance will begin with the Central Active Deck being filled with *5* Cards at random, selected from the Central Deck. If there are less than *5* Cards remaining in the Central Deck, all remaining Cards in the Central Deck (i.e. a number less than *5*) will be moved to the Central Active Deck. The first **Round** will then be started.


A game instance is managed by `Game()` found in `game_engine.py`.

## Rounds
A **Round** consists of both Players taking a **Turn** in playing the game, one following the other. In the first Game Instance when the code runs, The Player will go first.
When it is either Player's Turn, they are referred to as an **Actor**. A Turn for an **Actor**, begins with The Player drawing *5 Cards* at random from their Player Deck.


Rounds are managed within `Game()` in `game_engine.py`.

## Turns
At the beginning of a Turn, the Actor has **Attack** and **Money** both set to zero and *5* Cards are drawn at random from the **Player Deck** and constitute **The Player Hand**. If the case that Player Deck is empty which may happen during a Game instance, the Discard Pile will be moved to the Player Deck and players will select Cards from the Player Deck.
The Active Hand is empty at the beginning of each turn.

An Actor then has several options in each turn presented by the **Actor UI**:

 - Play a Card (Play All Cards is a variant of this)
 - Buy Cards
 - Attack
 - End Turn
 - Quit Game (this is only relevant for The Player)

Turns are managed by `Turn()` which is similarly named function in both the `User()` and `Computer()` classes in the file `actors.py`.

### Playing Cards
The Actor may only **Play** Cards from their Player Hand. When an Actor **Plays** a Card, the **Attack** and **Money** values are added to the current respective totals. The Card is moved from the Player hand to the Active Hand and the Actor is then presented with the **Actor UI** again. Playing All Cards is the same as playing each *5* Cards one at a time.

Playing Cards is managed by: `play_all_cards()`; `play_a_cards()` within the class `CommonUserActions()` in the file `common.py`

### Buying Cards
An Actor may **Buy Cards**, and is presented with a UI which we will denote, **The Shop** *(as explicitly named in the new code)*.
In The Shop, the Actor may **Purchase Cards** or return to the **Actor UI**.

**Purchasing Cards** is when the Actor successfully selects a Card from the Central Active Hand and it is moved to the Actor's own Discard Pile, subtracting the Cost property of the Card from the Actor's Money in the process (denoted as **Buying** the Card). The Actor may only Purchase the Card if the action of Buying the Card will leave the Actor with positive Money.

(Remark: By Purchasing Cards, the Actor then gains a probability of selecting this Card from the Player Deck at the beginning of their Turn when populating their Active Hand. This will occur only when the Player Deck has been emptied since the Purchase, as described in the section describing the beginning of a Turn.)

The Shop for The Player is defined by `card_shop()` within the class `User()`.
The Shop for The AI is defined by `purchase_cards()` within the class `Computer()`.
Both in the file `actors.py`

### Attack
An Actor may **Attack** the other Player, now denoted **The Defender** for clarity.

 1. The Defender's Health becomes the Actor's current Attack, subtracted from the Defenders current Health
 2. The Actor's Attack is set to zero

After an Attack, the Actor returns to the Actor UI.

Attacking is managed by `attack_player()` within the class `CommonUserActions()` in `common.py`

### End Turn
The action of **Ending the Turn** consists of appending both the Active Hand and the Player Hand to the Player Deck.

*(Note that here we do not randomly then select a new set of Cards for the Player Hand but in fact as we have already defined this process, however, the code will conduct this process here)*

Ending the Turn is managed by `end_turn()` within the class `CommonUserActions()` in `common.py`

### Quit Game
Only applicable to The Player: this will exit the program.

Quitting the game is managed by `exit()` within the class `Game()` in `game_engine.py`
Note that should the player force-close the game `hostile_exit()` will manage the process smoothly.

## The Winner
The **Winnner** is then determined as the Player with positive Health if they other Player has met the condition of negative or zero Health. In the condition that the Central Deck is empty, the winner is determined as the Player with the greatest Health, else the outcome is a Draw. The Game will then **End**.

The winner is determined by `end()` in the class `Game()` which is in the file  `game_engine.py`.

## Game End
Upon Ending, The Player is asked if they would like to **Replay**. A Replay will start with the Actor that would have come next, should the previous Game instance not have ended.

The End of the Game is also managed by `end()` in the class `Game()` which is in the file  `game_engine.py`.
