from glob import glob
import os
from pynput import keyboard
import time

import pygame

from LeftPlayer import LeftPlayer
from RightPlayer import RightPlayer


class Game:
    def __init__(self, param):
        """
        Classe Game qui permet de gérer l'affichage du jeu, l'attribution des points, les inputs, etc.
        Parameters
        ----------
        param : dict
            Contient les paramètres pour les joueurs (mouvement_speed...)

        Returns
        -------
        None.

        """
        self.param = param
        self.saved_params = self.get_scene()
        self.scene = self.saved_params[0] #string lue dans le fichier .txt
        self.screen = self.screen_creation() #matrice dans laquelle se déroule le jeu
        self.obstacle = [] #obstacles à afficher dans la matrice
        self.read_file() #récupère les obstacles de self.scene
        self.indexLeftPlayer = self.saved_params[3]
        self.indexRightPlayer = self.saved_params[4]
        
        #déclaration des deux objets LeftPlayer et RightPlayer dans l'instance de Game
        self.leftPlayer = LeftPlayer(self.indexLeftPlayer, 4, self, param["left_player"]["mouvement_speed"], param["left_player"]["attacking_speed"],
                                     param["left_player"]["attacking_range"], param["left_player"]["defending_range"], param["left_player"]["blocking_time"])
        self.rightPlayer = RightPlayer(self.indexRightPlayer, 4, self, param["right_player"]["mouvement_speed"], param["right_player"]["attacking_speed"],
                                       param["right_player"]["attacking_range"], param["right_player"]["defending_range"], param["right_player"]["blocking_time"])
        
        self.key_dict() #liste des controls
        self.score = [self.saved_params[1], self.saved_params[2]]
        self.rightPlayerAttacked = False
        self.leftPlayerAttacked = False
        self.leftPlayerAttacking = False
        self.rightPlayerAttacking = False
        self.rightPlayerBlocking = False
        self.leftPlayerBlocking = False
        
        self.menu = False #permet d'afficher le menu si True ou de le fermer si False
        self.game_loop = True #quitte la boucle principale si False
        
        self.start_music()
        self.m = True
        
        
    def start_music(self):
        pygame.mixer.music.load("sounds/music.wav")
        pygame.mixer.music.play(-1)
        

    def music(self):
        if self.menu:
            self.m = False if self.m == True else True
            if self.m:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            
        


    def get_scene(self):
        """
        Méthode appelée à la création de l'objet Game, permet de choisir entre plusieurs scènes dans les fichiers default*.ffscene ou la dernière partie sauvegardée.

        Returns
        -------
        tuple
            Les informations contenues dans les fichiers lus.

        """
        a = 0
        while(a != 1 and a != 2):
            print("Commencer une nouvelle partie : 1")
            print("Chargez la dernière partie sauvegardée : 2")
            a = int(input())
        if a == 1:
            l = []
            for file in glob("./ffscenes/default*.ffscene"):
                with open(file, 'r') as file :
                    l.append(file.read())
            for i in range(len(l)):
                print(f"{i+1} : {l[i]}")
            b = input("Entrer le numéro associé à la scène à charger: ")
            return l[int(b)-1], 0, 0, l[int(b)-1].index("1"), l[int(b)-1].index("2")
        
        else:
            with open("./ffscenes/to_load.ffscene", "r") as file:
                f = file.read().split()
            return f[0], int(f[1]), int(f[2]), int(f[3]), int(f[4])
            

    
    def read_file(self):
        """
        Récupère les obstacles à afficher.

        Returns
        -------
        None.

        """
        for i in range(len(self.scene)):
            if self.scene[i] == "x":
                self.obstacle.append(i)
    
    

    
    def save_game(self):
        """
        Méthode permettant de sauvegarder la partie en stockant dans le fichier to_load.ffscene la scène, le score et les index des joueurs au moment de la sauvegarde.

        Returns
        -------
        None.

        """
        to_save = self.scene + " " + str(self.score[0]) + " " + str(self.score[1])
        for i in range(1, len(self.scene)-1):
            if self.screen[-2][i] == "|" and self.screen[-2][i-1] == "/":
                    to_save += " " + str(i)
        for i in range(1, len(self.scene)-1):            
            if self.screen[-2][i] == "|" and self.screen[-2][i+1] == "\\":
                    to_save += " " + str(i)
        with open("ffscenes/to_load.ffscene", "w") as file:
            file.write(to_save)


    
    
    def load_game(self):
        """
        Méthode permettant de lire le fichier to_load.ffscene dans lequel est stocké la dernière sauvegarde avec le score et les positions des joueurs.

        Returns
        -------
        None.

        """
        with open("ffscenes/to_load.ffscene", "r") as file:
            f = file.read().split()

        self.scene = f[0]
        self.screen = self.screen_creation()
        self.obstacle = []
        self.read_file()
        self.indexLeftPlayer = int(f[3])
        self.indexRightPlayer = int(f[4])
        
        self.leftPlayer = LeftPlayer(self.indexLeftPlayer, 4, self, self.param["left_player"]["mouvement_speed"], self.param["left_player"]["attacking_speed"],
                                     self.param["left_player"]["attacking_range"], self.param["left_player"]["defending_range"], self.param["left_player"]["blocking_time"])
        self.rightPlayer = RightPlayer(self.indexRightPlayer, 4, self, self.param["right_player"]["mouvement_speed"], self.param["right_player"]["attacking_speed"],
                                       self.param["right_player"]["attacking_range"], self.param["right_player"]["defending_range"], self.param["right_player"]["blocking_time"])
        
        self.score = [int(f[1]), int(f[2])]
        self.menu = False
        self.key_dict()

                


    def get_indices(self):
        """
        Récupère les indices des caractères "1" et "2" pour les associer respectivement à leftPlayer et rightPlayer
        Returns
        -------
        (int, int)
            Index du joueur 1 et 2.

        """
        return self.scene.index("1"), self.scene.index("2")
                
        
        
        
    def screen_creation(self):
        """
        Retourne une matrice de caractères " " de hauteur 10 et largeur égale au nombre de caractères dans la scene

        Returns
        -------
        list
            Matrice affichée dans laquelle se déroule le jeu.

        """
        return [[" " for i in range(len(self.scene))] for j in range(10)]




    def print_ground(self):
        """
        Affichage du sol dans la matrice.

        Returns
        -------
        None.

        """
        self.screen[9] = ["#"]*(len(self.scene))
        for elem in self.obstacle:
            self.screen[8][elem] = "#"
        
        
        
        
        
    def flush_screen(self):
        """
        Efface re-affiche la matrice.

        Returns
        -------
        None.

        """
        os.system("cls" if os.name == "nt" else "clear")
        for i in range(len(self.screen)):
            for j in range(len(self.screen[0])):
                print(self.screen[i][j], end="")
            print()
            
            
            
            
    def clear_screen(self):
        """
        Remet la matrice à zero (seulement des caractères " ")

        Returns
        -------
        None.

        """
        self.screen = self.screen_creation()
        
            
    
    
    def key_dict(self):
        """
        Dictionnaire associant les touches avec les fonctions à exécuter.

        Returns
        -------
        None.

        """
        self.dico = {}
        self.dico["d"] = self.leftPlayer.moveRight
        self.dico["q"] = self.leftPlayer.moveLeft
        self.dico["a"] = self.leftPlayer.jump_left
        self.dico["e"] = self.leftPlayer.jump_right
        self.dico["z"] = self.leftPlayer.attack
        self.dico["s"] = self.leftPlayer.block
        
        self.dico["right"] = self.rightPlayer.moveRight
        self.dico["left"] = self.rightPlayer.moveLeft
        self.dico["l"] = self.rightPlayer.jump_left
        self.dico["m"] = self.rightPlayer.jump_right
        self.dico["o"] = self.rightPlayer.attack
        self.dico["p"] = self.rightPlayer.block
        
        self.dico["g"] = self.change_boolean_value
        self.dico["t"] = self.change_game_loop_value
        
        self.dico["h"] = self.load_game
        self.dico["b"] = self.save_game
        self.dico["v"] = self.music
        
        
        
        
    def change_boolean_value(self):
        """
        Change la valeur de menu lors de l'appel de la méthode.
        Lorsque menu est True, le menu est affiché.

        Returns
        -------
        None.

        """
        self.menu = True if self.menu == False else False
        
        
        
        
    def change_game_loop_value(self):
        """
        Change la valeur de game_loop à False et permet de quitter la boucle de jeu.

        Returns
        -------
        None.

        """
        if self.menu:
            self.game_loop = False
            self.change_boolean_value()
    
    
    
    def on_press(self, key):
        """
        Méthode utilisée dans le listener pour gérer les inputs et l'appel des méthodes associées dans le dictionnaire dico.

        Parameters
        ----------
        key : pynput.keyboard.object
            Les touches correpondants aux inputs.

        Returns
        -------
        None.

        """
        if len(str(key)) > 3 and str(key).split('.')[1] in dir(keyboard.Key) and str(key).split('.')[1] in self.dico:
            self.dico[str(key).split('.')[1]]()
        elif key.char in self.dico:
            self.dico[key.char]()
        
        
        
    
    def on_release(self, key):
        """
        Permet de gérer le relachement des touches dans le listener.

        Parameters
        ----------
        key : pynput.keyboard.object
            Les touches correpondants aux inputs.

        Returns
        -------
        bool
            Indique que la touche est relachée.

        """
        if key == keyboard.Key.esc:
            return False        
            
        
        
    def display_menu(self):
        """
        Permet d'afficher le menu dans lequel sont affichés les controls.
        Permet de quitter la partie ou de revenir sur le jeu.

        Returns
        -------
        None.

        """
        os.system("cls" if os.name == "nt" else "clear")
        print("Right player controls:\n  <- move left\n  -> move right\n  l jump left\n  m jump right\n  o attack\n  p block\n")
        print("Left player controls:\n  k move left\n  m move right\n  i jump left\n  p jump right\n  o attack\n  l block\n")
        print("Press g to exit menu")
        print("Press t to exit the game")
        print("Press v to pause / unpause music")
        print("Press b to save")
        print("Press h to load a saved game")
        
        while(self.menu):
            continue
            
        
    
    def print_score(self):
        """
        Affichage du score.

        Returns
        -------
        None.

        """
        self.screen[0][len(self.screen[0])//2-3] = str(self.score[0])
        self.screen[0][len(self.screen[0])//2+3] = str(self.score[1])
        self.screen[0][len(self.screen[0])//2] = "|"
        
        
        
        
    def pointsAllocation(self):
        """
        Attribution des points en vérifiant si les joueurs se touchent en même temps, s'il se défendent, en prenant en compte leur <defending_range>

        Returns
        -------
        None.

        """
        if not (self.leftPlayerAttacked and self.rightPlayerAttacked):
            if self.leftPlayerAttacked:
                if self.rightPlayer.x - self.leftPlayer.x > self.leftPlayer.defending_range:
                    self.score[1] += 1
                else:
                    if not (self.leftPlayerBlocking):
                        self.score[1] += 1
                        
            elif self.rightPlayerAttacked:
                if self.rightPlayer.x - self.leftPlayer.x > self.rightPlayer.defending_range:
                    self.score[0] += 1
                else:
                    if not (self.rightPlayerBlocking):
                        self.score[0] += 1
            

            
            
    def run(self):
        """
        Méthode dans laquelle est définie la boucle de jeu, le listener pour les inputs.
        Cette méthode gère les exécutions des mouvements des joueurs, l'affichage et le raffraichissement.

        Returns
        -------
        None.

        """
        
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        frames = 1/self.param["frames"]
        while(self.game_loop):
            time.sleep(frames)
            
            
            
            
            #exécution des actions de leftPlayer puis suppression de l'action de la liste
            if len(self.leftPlayer.current_action) != 0:
                al = self.leftPlayer.current_action.pop(0)
                if al != ():
                    if len(al) == 1:
                        al[0]()
                    elif len(al) == 2:
                        al[0](al[1])
                    else:
                        al[0](al[1], al[2])
            if len(self.leftPlayer.sounds) != 0:
                self.leftPlayer.sounds.pop(0)()
                
            #exécution des actions de rightPlayer puis suppression de l'action de la liste
            if len(self.rightPlayer.current_action) != 0:
                ar = self.rightPlayer.current_action.pop(0)
                if ar != ():
                    if len(ar) == 1:
                        ar[0]()
                    elif len(ar) == 2:
                        ar[0](ar[1])
                    else:
                        ar[0](ar[1], ar[2])
            if len(self.rightPlayer.sounds) != 0:
                self.rightPlayer.sounds.pop(0)()
            
            
            self.clear_screen()
            self.print_score()
            self.print_ground()
            
            #affiche les joueurs en position attack ou block selon la valeur de ces paramètres.
            self.leftPlayer.print(True if self.leftPlayerAttacking else False, True if self.leftPlayerBlocking else False)
            self.rightPlayer.print(True if self.rightPlayerAttacking else False, True if self.rightPlayerBlocking else False)
            
            self.flush_screen()
            
            #Attributions des points
            self.pointsAllocation()
                    
            #on positionne les deux joueurs lorsqu'au moins un des deux à touché l'autre
            if (self.leftPlayerAttacked and not self.leftPlayerBlocking) or (self.rightPlayerAttacked and not self.rightPlayerBlocking):
                self.leftPlayer.x = self.get_indices()[0]
                self.rightPlayer.x = self.get_indices()[1]
                
                self.leftPlayer.print(False, False)
                self.rightPlayer.print(False, False)
                self.clear_screen()
                self.flush_screen()
            
                
            self.leftPlayerAttacking = False
            self.rightPlayerAttacking = False
            self.leftPlayerBlocking = False
            self.rightPlayerBlocking = False
            self.rightPlayerAttacked = False
            self.leftPlayerAttacked = False
            
            if self.menu:
                self.display_menu()