import pygame



class Player:
    def __init__(self, x, y, game, movement_speed, attacking_speed, attacking_range, defending_range, blocking_time):
        """
        Construit un objet Player

        Parameters
        ----------
        x : int
            Position du joueur en abscisse.
        y : int
            Position du joueur en ordonnée.
        game : object (matrix)
            Référence à l'objet game dans lequel se déroule la partie.
        movement_speed : int
            Nombre de frames pour faire un movement.
        attacking_speed : int
            Nombre de frames pour faire une attaque.
        attacking_range : int
            Longueur de l'épée lors d'une attaque.
        defending_range : int
            Nombre de blocs devant le joueur qui lui permet de bloquer un coup lorsqu'il se défend.
        blocking_time : int
            Nombre de frames durant lesquelles le block est actif.

        Returns
        -------
        None.

        """
        self.x = x
        self.y = y
        self.current_action = [] #liste d'actions servant à stocker les mouvements à exécuter pour les appeler dans la boucle de jeu
        self.sounds = [] #liste des sons à lancer en même temps que les actions
        self.game = game
        self.movement_speed = movement_speed
        self.attacking_speed = attacking_speed
        self.attacking_range = attacking_range
        self.blocking_time = blocking_time
        self.defending_range = defending_range
            
        
    #Effets sonores
    def hit_sound(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/hit.wav"))
          
    def jump_sound(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/jump.wav"))

    def block_sound(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/block.wav"))
        
               
        
        
    def update(self, inc):
        """
        Permet d'incrémenter ou décrémenter x de l'objet Player.

        Parameters
        ----------
        inc : bool
            True pour incrémenter x, False pour décrémenter x.

        Returns
        -------
        None.

        """
        self.x = self.x + 1 if inc else self.x - 1
        
        
        
        
    def update_diag(self, right, up):
        """
        Permet d'incrémenter ou décrémenter x et y en même temps

        Parameters
        ----------
        right : bool
            False ou True pour indiquer si on veut aller à droite ou à gauche.
        up : bool
            True ou False pour indiquer si on veut aller vers le haut ou le bas.

        Returns
        -------
        None.

        """
        self.x = self.x + 1 if right else self.x - 1
        self.y = self.y - 1 if up else self.y + 1