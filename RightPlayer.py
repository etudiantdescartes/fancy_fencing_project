from Player import Player

class RightPlayer(Player):
    def __init__(self, x, y, game, movement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        """
        Sous classe de Player permettant de créer un objet RightPlayer.
        Possède les même paramètres que la classe Player.
        Possède les mêmes méthodes que LeftPlayer (adaptées pour RightPlayer)
        Permet de gérer les mouvements du joueur 2.
        """
        super().__init__(x, y, game, movement_speed, attacking_speed, attacking_range, defending_range, blocking_time)
        
        
        
        
        
        
    def jump_left(self):
        """
        Méthode qui permet d'effectuer un saut vers la gauche.
        Ajoute à la liste d'actions du joueur (current_action) des tuples contenants une référence à la méthode
        udpate et les deux paramètres pour choisir x ou y, incrémenter ou décrémenter.
        Vérifie s'il peut bien avancer (obstacles et limites du board) avant de stocker les mouvements.
        La liste d'actions ne peut contenir que les mouvements qui permettent de faire une action (on ne peut pas ajouter de nouveaux mouvements si les mouvements pour faire le saut n'ont pas tous été exécutés).
        Lorsque <mouvement_speed> est supérieur à 1, on ajoute des tuples vide () pour lesquels aucun mouvement ne sera exécuté.
        Les méthodes stockées dans cette liste seront appelées dans la boucle de jeu.

        Returns
        -------
        None.

        """
        if self.game.menu == False:
            if len(self.current_action) == 0 and self.x >= 5 and self.game.screen[-2][self.x-3] != "#" and self.game.screen[-2][self.x-2] != "#":
                for i in range((self.movement_speed-1)*3):
                    self.current_action.append(())
                if self.movement_speed == 1:
                    self.current_action.append((self.update_diag, False, True))
                    self.current_action.append((self.update, False))
                else:
                    self.current_action.insert(0, (self.update_diag, False, True))
                    self.current_action.insert(len(self.current_action)//2, (self.update, False))
                    
                self.current_action.append((self.update_diag, False, False))
                self.sounds.append(self.jump_sound)
        
        
        
        
        
                 
                 
                 
    def jump_right(self):
        """
        Méthode qui permet d'effectuer un saut vers la droite.
        Mêmes caractéristiques que jump_left.

        Returns
        -------
        None.

        """
        if self.game.menu == False:
            if len(self.current_action) == 0 and self.x <= len(self.game.screen[0])-5 and self.game.screen[-2][self.x+4] != "#" and self.game.screen[-2][self.x+3] != "#":
                for i in range((self.movement_speed-1)*3):
                    self.current_action.append(())
                if self.movement_speed == 1:
                    self.current_action.append((self.update_diag, True, True))
                    self.current_action.append((self.update, True))
                else:
                    self.current_action.insert(0, (self.update_diag, True, True))
                    self.current_action.insert(len(self.current_action)//2, (self.update, True))
                    
                self.current_action.append((self.update_diag, True, False))
                self.sounds.append(self.jump_sound)
        
        
        
        
    def print(self, attack, block):
        """
        Permet de représenter le personnage associé à l'objet LeftPlayer dans la matrice à afficher
        
        Parameters
        ----------
        attack : bool
            Si attack == True, alors on change l'affichage de l'épéé avec <attacking_range> fois le caractère "_" (l'affichage s'arrête au 2e joueur s'il y a collision).
        block : bool
            Si block == True, alors on change l'affichage de l'épéé avec le caractère "|".

        Returns
        -------
        None.

        """
        self.game.screen[self.y][self.x-1] = "<"
        self.game.screen[self.y][self.x] = "O"
        self.game.screen[self.y][self.x+1] = ">"
        self.game.screen[self.y+1][self.x] = "|"
        self.game.screen[self.y+2][self.x] = "|"
        self.game.screen[self.y+3][self.x] = "|"
        self.game.screen[self.y+1][self.x-1] = "_"
        self.game.screen[self.y+4][self.x+1] = "\\"
        self.game.screen[self.y+4][self.x] = "|"
        self.game.screen[self.y+1][self.x-2] = "\033[0;31m" + "\\" + "\033[00m"
        if attack:
            self.game.screen[self.y+1][self.x-2] = "\033[0;31m" + "_" + "\033[00m"
            for i in range(1, self.attacking_range):
                if self.x-2-i < 0:
                    break
                if self.game.screen[self.y+1][self.x-2-i] == " ":
                    self.game.screen[self.y+1][self.x-2-i] = "\033[0;31m" + "_" + "\033[00m"
        if block:
            self.game.screen[self.y+1][self.x-2] = "\033[0;31m" + "|" + "\033[00m"
            
            
            
            
            
    def update_attack(self):
        """
        Méthode permettant d'indiquer que le joueur est en train d'attaquer, et vérifie s'il touche l'autre joueur

        Returns
        -------
        None.

        """
        self.game.rightPlayerAttacking = True
        for i in range(1, self.attacking_range):
            if self.x-2-i < 0: # or self.game.screen[self.y+1][self.x-2-i] == "\033[0;32m" + "|" + "\033[00m":
                break
            if self.game.screen[self.y+1][self.x-2-i] == "_" or self.game.screen[self.y+1][self.x-2-i] == "|":
                self.game.leftPlayerAttacked = True
        
        
        
        
        
    def attack(self):
        """
        Méthode permettant d'effectuer une attaque et stocke des références à la méthode update_attack dans current_action.

        Returns
        -------
        None.

        """
        if self.game.menu == False:
            if len(self.current_action) == 0:
                for i in range(self.attacking_speed-1):
                    self.current_action.append(())
                self.current_action.append((self.update_attack,))
                self.sounds.append(self.hit_sound)
                 
                 
                 
                 
    
    
    def moveLeft(self):
        """
        Méthode qui permet d'avancer d'un bloc vers la gauche.
        Mêmes caractéristiques que moveRight.

        Returns
        -------
        None.

        """
        if self.game.menu == False:
            if len(self.current_action) == 0 and self.x >= 3 and self.game.screen[self.y+4][self.x-1] != "#":
                for i in range(self.movement_speed-1):
                    self.current_action.append(())
                self.current_action.append((self.update, False))
            





    def moveRight(self):
        """
        Méthode qui permet d'avancer d'un bloc vers la droite.
        Vérifie les collisions avant de stocker les élément dans la liste current_action.

        Returns
        -------
        None.

        """
        if self.game.menu == False:
            if len(self.current_action) == 0 and self.x <= len(self.game.screen[0])-3 and self.game.screen[self.y+4][self.x+2] != "#":
                for i in range(self.movement_speed-1):
                    self.current_action.append(())
                self.current_action.append((self.update, True))

        



    
    def update_block(self):
        """
        Permet d'indiquer que le joueur est en train de bloquer

        Returns
        -------
        None.

        """
        self.game.rightPlayerBlocking = True
        
        
        
        
        
    def block(self):
        """
        Stocke les actions de block dans current_action.

        Returns
        -------
        None.

        """
        if self.game.menu == False:
            if len(self.current_action) == 0:
                for i in range(self.blocking_time):
                    self.current_action.append((self.update_block,))
                self.sounds.append(self.block_sound)