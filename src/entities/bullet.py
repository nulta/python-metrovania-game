from .entity import Entity

class Bullet(Entity):
    def __init__(self, isEnemy=True):
        super().__init__()
        self._isEnemy = isEnemy
    
    def update(self):
        # Check collision every tick
        # Check isEnemy & isPlayer and Deal damage
        pass