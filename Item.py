import pygame
class Item(pygame.sprite.Sprite):

    def __init__(self, itemImgPath, posX, posY):
        super(Item, self).__init__()
        self.posX = posX
        self.posY = posY
        self.sprite = pygame.image.load(itemImgPath)
        self.image = pygame.image.load(itemImgPath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [posX, posY]
        self.isHolding = False

    def setVisibility(self, isVisible):
        self.isVisible = isVisible

    def setImage(self, itemImgPath):
        self.image = pygame.image.load(itemImgPath)

    def setImageWithoutPath(self, image):
        self.image = image

    def setPosition(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.rect.topleft = [posX, posY]

    def getPositionX(self):
        return self.posX

    def getPositionY(self):
        return self.posY

    def getImage(self):
        return self.image

    def getRect(self):
        return self.rect

    def setIsHolding(self, isHolding):
        self.isHolding = isHolding

    def getIsHolding(self):
        return self.isHolding

    def isCollidingOnCoords(self, point):
        return self.getRect().collidepoint(point[0], point[1])

