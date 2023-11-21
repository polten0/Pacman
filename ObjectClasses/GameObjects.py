from AppCore.Managers import GameManager

class GameObject:
    # typeObject может быть: 'wall', 'player', 'food', 'big_food', 'ghost'. typeObject задавайте каждому классу по умолчанию в конструкторе
    def __init__(self, typeObject='none'):
        self.typeObject = typeObject

    # хитбокс
    def rec(self):
        pass


class Player(GameObject):
    def __init__(self, typeObject='player'):
        self.typeObject = typeObject
    def onCollision(self, collide_object):
        if (collide_object.typeObject == 'food'):
            collide_object.onCollision(self)
        elif (collide_object.typeObject == 'ghost'):
            if (GameManager.player_is_boosted == False):
                self.Death()
            if (GameManager.player_is_boosted):
                collide_object.onCollision(self)
        elif (collide_object.typeObject == 'big_food'):
            collide_object.onCollision()
            GameManager.boost_player()
        elif (collide_object.typeObject == 'wall'):
            pass

    def Death(self):
        pass



class Ghost(GameObject):
    def __init__(self, typeObject='ghost'):
        self.typeObject = typeObject
        self.Frightened = False
        self.Timeout = False

    def onCollision(self, collide_object):
        if (collide_object.typeObject == 'player'):
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


