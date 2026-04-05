import pygame
import subprocess

from elements import *
import conf

#working on the vpn directory, getting it put in .config
#need to make updateDatabase.sh workable through a flag or something.
#maybe have a gooeyplate.sh that runs gooeyplate.py but if -u flag then it runs updateDatabase.sh and asks for password.

#perhaps add a script in the future that automaticlly installs everything in the proper places.
#ie. sudoers.d wg-quick file, maybe more idk.


#maybe add updateDatabase.sh to bin on first build, or just tell people to do so and name it gp-update-database

def draw(win):
    win.fill(conf.backCol)

    currentConnection.draw(win)
    for butt in vpnButts:
        butt.draw(win)


    pygame.display.update()



if __name__ == '__main__':
    pygame.init()    
    win         = pygame.display.set_mode(conf.winSize, pygame.RESIZABLE)

    pygame.display.set_caption('Gooey Plate')

    createVpnButts()

    run     = True
    cock    = pygame.time.Clock()
    while run:


        for event in pygame.event.get():
            conf.winSize    = pygame.display.get_surface().get_size()
            pos             = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if conf.scroll > 0:
                        conf.scroll -= conf.scrollMod
                    else: 
                        conf.scroll = 0
                if event.button == 5:
                    vb = vpnButts[-1]
                    if 0 < vb.scaledSize[1] + vb.scaledSize[3] > conf.winSize[1]:
                        conf.scroll += conf.scrollMod
                    else:
                        pass


            for butt in vpnButts:
                butt.hover(pos)


        getCurrentVpn(event, pos)


        BigCock = cock.tick(144) / 1000
        draw(win)


    pygame.quit()

