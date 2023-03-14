import pygame as pg

pg.init()

aken= pg.display.set_mode((800,400))
gameplay=True

class ruut:
    def __int__(self, kyljePikkus):
        self.kyljePikkus=kyljePikkus
xkoord=1



while gameplay:
    pg.time.delay(10)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            gameplay=False

    if xkoord==700:
        xkoord=0

    aken.fill((0,0,0))
    #kuhu, (värv), (asukoht ja suurus)
    pg.draw.rect(aken, (200, 100, 100), (xkoord, 30, 60, 60))

    pg.display.update()
    xkoord+=1
