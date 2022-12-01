import json

import pygame

from Game import Game

        
if __name__ == '__main__':
    with open(r"./param.json") as js:
        param = json.load(js)
        
    pygame.init()

    game = Game(param)
    game.run()