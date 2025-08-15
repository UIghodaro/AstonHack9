# Solo Hackathon Project: One Skater Smashed
First videogame project I ever made, created in under 24 hours at the AstonHack9 Competition using python with pygame libraries

## Tech & setup
The game was built such that running game.py from the root should run the entire game.
- If python or pygame is not installed, run the following in bash for dependencies
```bash
pip install python
pip install pygame
```

Following this:
1. run game.py in an IDE or by typing ``python game.py`` in terminal of the repo root to access the game (controls are A and D for left and right movement respectively, spacebar to fly) OR 
2. run editor.py in an IDE or by typing ``python editor.py`` in terminal of the repo root to access the level editor and place your own blocks, changing the map.json file dynamically

### Possible issue
If, when attempting to run game.py or editor.py, an error comes up along the lines of ``The system cannot find specified path: 'gameRss/images/...'`` then it is highly likely the python file is not being run from the root or the folders are not in the root. 
Ensure all folders are in the root, alongside game.py, editor.py and map.json

## Game Scope
The game is a 2D platformer with a level editor included. The playable character is given infinite flight as the "Aston University Goose".
No proper mechanics other than collisions, movement flight and level editing have been implemented due to a lack of time to learn how to do such things as well as how to implement them.

### In-Game Controls
Character is **moved** via **WASD** keys, then using **spacebar** to **jump/fly**

### In-Editor Controls
Screen/camera is **moved** via **WASD** keys, **left-click** to **place a block** and *hold left-click* to place multiple. **right-click** to **delete a block** and *hold right-click* to delete multiple.

Use the **scroll wheel** to change **block type**; Then hold **shift** while using the **scroll wheel** to **Switch block kind**.

Press **'G'** *on the keyboard* to **toggle grid mode**. 

Press **'O'** *on the keyboard* to **save the map** to map.json. Extra map features to be added I guess

### Game('s) Vision
The vision was for the goose to be able to use its figure skating blades to attack incoming pedestrians in a snowy, Birmingham day. The end goal was making the goose perform a triple axel, which sadly did not end up happening.

Watchers and cloners are encouraged to rip anything and everything from this and improve on it! Game creation is fun!
