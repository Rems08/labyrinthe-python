import pyxel

# Constants
SPRITE_SIZE = 16
FRAME_COUNT = 3  # Nombre de frames par direction
FRAME_DELAY = 3  # Ticks entre chaque changement de frame
DIRECTIONS = {        # Mapping des directions vers la ligne dans la sprite sheet
    "down": 0,
    "right": 1,
    "up": 2,
    "left": 3
}


class App:
    def __init__(self):
        pyxel.init(160, 120)
        # Charge la banque de sprites (sheet 24×32) placée à (0,0) dans resources.pyxres
        pyxel.load("assets/my_resource.pyxres")

        # Variables de position et d’animation
        self.x = pyxel.width // 2
        self.y = pyxel.height // 2
        self.direction = "down"
        self.frame = 0
        self.frame_timer = 0

        # Démarre la boucle principale
        pyxel.run(self.update, self.draw)

    def update(self):
        dx, dy = 0, 0

        # Détection des touches et attribution de la direction
        if pyxel.btn(pyxel.KEY_LEFT):
            dx, self.direction = -2, "left"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            dx, self.direction = 2, "right"
        elif pyxel.btn(pyxel.KEY_UP):
            dy, self.direction = -2, "up"
        elif pyxel.btn(pyxel.KEY_DOWN):
            dy, self.direction = 2, "down"
        else:
            # Si aucune touche, on remet l'animation au frame initial
            self.frame = 0
            self.frame_timer = 0

        # Mise à jour de l’animation si déplacement
        if dx != 0 or dy != 0:
            self.frame_timer += 1
            if self.frame_timer >= FRAME_DELAY:
                self.frame = (self.frame + 1) % FRAME_COUNT
                self.frame_timer = 0

        # Mise à jour de la position avec confinement dans la fenêtre
        self.x = max(0, min(self.x + dx, pyxel.width - SPRITE_SIZE))
        self.y = max(0, min(self.y + dy, pyxel.height - SPRITE_SIZE))

    def draw(self):
        # Efface l’écran
        pyxel.cls(7)

        # Sélection du sprite dans la sprite sheet
        row = DIRECTIONS[self.direction]
        u = self.frame * SPRITE_SIZE
        v = row * SPRITE_SIZE
        pyxel.blt(self.x, self.y, 0, u, v, SPRITE_SIZE, SPRITE_SIZE, 0)

App()
