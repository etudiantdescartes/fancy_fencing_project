# About the project
As part of an assignment, I had to do this project which is a game called Fancy Fencing written in Python that you can play in the terminal.
The structure is simple, there are 4 files corresponding to 4 classes, and a main.py file.
- The class Game handles the .ffscene files which contains the different stages to play in as well as the display (with the framerate), the inputs and the point allocation.
- The Player class contains methods to change the x and y coordinates of the players and methods to play sounds for attacks blocks and jumps.
- LeftPlayer and RightPlayer  are subclasses of Player that handle every movement a player can do : jumping, attacking, blocking, and moving right and left.



# Getting started
## Prerequisites
Before running the program, you first need to install 2 libraries for this project with:
- ```pip install pynput```
- ```pip install pygame```

## Installation
- First download the project files or clone the repo :
	```git clone https://github.com/etudiantdescartes/project_name.git```
- And run it with:
    ```python project.py```



This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Usage
After launching the program, you will see several « scenes » that you can choose from in your terminal.

![image1](/Image1.png?raw=true)

Each scene describes the map in which you will be playing.
The caracter « _ » shows the ground, « x » the obstacles, « 1 » the player 1 and « 2 » the player 2.
You will be asked to type a number to select the desired scene and press Enter.
The game then starts and the chosen scene is displayed.

![image2](/Image2.png?raw=true)

Both player can jump right and left to avoid obstacles (screens), move right and left, attack and block.
Here are the controls for both players :

| | Left player | Right plater |
|-| :-: | :-: |
|Move left|```q```|```Left arrow```|
|Move right|```d```|```Right arrow```|
|Jump left|```a```|```l```|
|Jump right|```e```|```m```|
|Attack|```z```|```o```|
|Block|```s```|```p```|

You can go to the menu by typing « g », in which you can see the controls for both players.
See what you can do in the menu:

![image3](/Image3.png?raw=true)

When you are in the menu, it is possible to pause / unpause the music, to save the game and load the last save.

## Rules
The goal is to make contact with the other player with your sword, without being attacked yourself.
If both players attack at the same time, they are put back into their starting place and no point is distributed.
If a player attacks the other one who is defending himself, the attacking player gets the point only if the defending player is further of the attacking player than his <defending_range>.
It is possible to set the framerate, the number of frame each action will take, the defending range and the attacking range in the « param.json » file.
