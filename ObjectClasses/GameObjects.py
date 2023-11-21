from AppCore.Managers import GameManager
from Objects import GameObject

class Player(GameObject):
    def __init__(self, typeObject='player'):
        self.typeObject = typeObject
    def onCollision(self, collide_object):
        if (isinstance(collide_object, Food)):
            collide_object.onCollision(self)
        elif (isinstance(collide_object, Ghost)):
            if (GameManager.player_is_boosted == False):
                self.Death()
            if (GameManager.player_is_boosted):
                collide_object.onCollision(self)
        elif (isinstance(collide_object, BigFood)):
            collide_object.onCollision()
            GameManager.boost_player()
        elif (isinstance(collide_object, Wall)):
            pass

    def Death(self):
        pass



class Ghost(GameObject):
    def __init__(self, typeObject='ghost'):
        self.typeObject = typeObject
        self.Frightened = False
        self.Timeout = False

    def onCollision(self, collide_object):
        if (isinstance(collide_object, Player)):
            if (self.Frightened):
                self.Death()
            else:
                collide_object.onCollision()

    def Death(self):
        self.Frightened = False
        self.Timeout = True
        pass



class Food(GameObject):
    def __init__(self, typeObject='food'):
        self.typeObject = typeObject
        self.active = True

    def onCollision(self):
        if (self.active):
            GameManager.addScore(self.typeObject)
            self.active = False

class BigFood(Food):
    def __init__(self, typeObject='big_food'):
        self.typeObject = typeObject

class Wall:
    pass


