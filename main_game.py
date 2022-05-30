
# NÄR KOMMER TBAX
# gör så gubben i fight kan kolla höger/vänster, fokusera på fight sen prat bubblor osånt för main map
#https://www.youtube.com/watch?v=UdsNBIzsmlI&t=28s&ab_channel=TechWithTim
#fixa enemy, skott och collide
#också ksk fixa hopp?

#gubbe kolla åt håll klart, nu fixa hor skottet och collision


# FIXA SKOTT OCH ATT GUBBEN KAN GÅ I FÖRSTA COLLISION



#lägg till så innan fight ska han prata av sig själv, text i 5 sek sen ny sen kan klicka vidare


#bugs: fixa första skottet, om man skjuter sen går vänster stannar skottet kvar och dödar!? pratbubblor osånt också

#improvement dubbel for x in range loop för att undvika global

import random

import pygame, sys
from pygame.locals import *
pygame.init() #initialize


clock = pygame.time.Clock() # FÖR FPS
bredd = 600
hojd = 600 # bredd och höjd på skärmen
resolution = pygame.display.set_mode((bredd, hojd)) # visa skärmen, gjort till en variabel för enklare blit
input = pygame.key.get_pressed() # tangent input
innan_fight_pratbubbla = pygame.image.load("pratbubbla.png") # ladda in bilden
enter_fight_press = pygame.image.load("press_to_enter.png") # ladda in bilden

#  GUBBE MAP 2
walk_right = pygame.image.load("gubbe_hoger.png")# ladda in bilden
walk_left = pygame.image.load("gubbe_vnster.png")# ladda in bilden
walkL_rect = walk_left.get_rect() # gör en rect av bilden (hitbox)
walkR_rect = walk_right.get_rect() # gör en rect av bilden (hitbox)
walkR_rect.x = 50
walkR_rect.y = 400 # kordinater för ena gubben, andra gubben sätts senare till samma

spelare_x = 30 # spelare i första mappen startpunkt, ändras senare med tangent input
spelare_y = 400 # spelare i första mappen startpunkt, ändras senare med tangent input
spelare_bredd = 20
spelare_hojd = 20
fartmap1 = 8 # gubbens fart i första mappen
fartmap2 = 10 # gubbens fart i andra mappen

#  SKOTT, map2
skottbild = pygame.image.load("bullet.png") # ladda in bilden
skottRect = skottbild.get_rect() # gör till rect
skottRect.y = walkR_rect.y # sätt rectens y till gubbens, ändras aldrig då skottet endast ändras på x axeln

def map1(): # funktion map1
    pygame.display.set_caption("Lobby") # ge namn på skärmen
    map1 = pygame.image.load("main_map_ritad.png") # ladda in bild
    obj = pygame.image.load("enemyface.png") # ladda in bild
    hotbar_map1 = pygame.image.load("hotbar_map1.png") # ladda in bild
    resolution.blit(map1, (0,0)) # lägg mappen på skärmen
    resolution.blit(hotbar_map1, (0, 0)) # lägg hotbar bilden på skärmen
    global obj_rect # gör så värdet kan ändras senare utanför funktionen (improvement kan fixas i en dubbel for x in range loop för att undvika global)
    obj_rect = obj.get_rect() # gör en rect av bilden
    obj_rect.x = 520 # koordinater där han ska vara
    obj_rect.y = 250
    resolution.blit(obj, obj_rect) # blit honom på skärmen
    #obj_rect= pygame.draw.rect(resolution, (5, 0, 0), objective)

#  FÖR MAP 2:

#  ZOMBIE PÅ MAP 2, utanför funtionen map2 då dessa grejer endast behöver läsas en gång
zombie1 = pygame.image.load("zombie_map2.png")
zombie1rect = zombie1.get_rect()
zombie1rect.y = 350
zombie1rect.x = 520
#zombie2 = pygame.image.load("zombie_map2.png")
#zombie2rect = zombie2.get_rect()
#zombie2rect.x = 600
#zombie2rect.y = 350
zombiefart = 5

#  FIREBALL
fireballbild = pygame.image.load("fireball.png")
fireballrect = fireballbild.get_rect()
fireballrect.x = 50
fireballrect.y = -10
fireballfart = 15 # första så att variablen sen kan ändras
fireballfart2 = 35 # första så att variablen sen kan ändras
kills = 0 # kill counter uppe till höger, för varje colission


text_x = 10
text_y = 10


def visa_score(x, y): # funktion för antal kills under map2
    font = pygame.font.Font("freesansbold.ttf", 20)
    score = font.render("Kills: " + str(kills), True, (255, 255, 255)) # gör om till string innan blit då font.render funktionen endast tar string som argument
    resolution.blit(score, (x, y))

def you_lost():
    youlost_bild = pygame.image.load("youlost_bild.png")
    resolution.blit(youlost_bild, (0, 0))
    global mellanmaps_live
    mellanmaps_live = True # bilden visar tryck c för att fortsätta, när denna är live kommer det hända något när man trycker c, annars hade man antingen aldrig kunnat trycka c eller trycka hela tiden
    # hade kunnat ha den i denna funktion men hade behövt använda flera globals om inte byta till for loops
    walkR_rect.x = 460
    walkR_rect.y = 500

def you_won(): # om du dödar 20 zombies
    youwon_bild = pygame.image.load("youwon_bild.png")
    resolution.blit(youwon_bild, (0, 0))
    global spelare_x # här är som ovan istället för att göra en if sats i while loopen la jag allt här, mycket globals ;(
    spelare_x = 30
    global spelare_y
    spelare_y = 400 # sätt spelare till spawn
    global prat2_y
    prat2_y = -100
    global inte_vunnit
    inte_vunnit = False # gör så du ej kan köra samma mission igen, den är avklarad, improvement göra en if sats i loopen if not inte_vunnit då if collide skriv att det är klart

def round2(x, y): # visar round2 bilden, improvement flytta hit clockan för finare kod
    round2bild = pygame.image.load("round2_autograf.png")
    resolution.blit(round2bild, (x, y))

def reset_map2(): # körs varje gång du går in i map2 efter att du har förlorat så du börjar om
    global kills
    kills = 0
    walkR_rect.x = 50
    zombie1rect.x = 600
    fireballrect.y = 0

def reward_bild(): #om du vunnit
    burger_reward_bild = pygame.image.load("burger_reward.png")
    resolution.blit(burger_reward_bild, (360, 531))
    burger_info = pygame.image.load("1x_burger.png")
    show_burger_info = False
    if mouse_x >= 360 and mouse_y >= 530: # om musen är på burgaren visa info om burgaren
        show_burger_info = True
    if mouse_x >= 404:
        show_burger_info = False
    if mouse_y >= 578:
        show_burger_info = False
    if show_burger_info:
        resolution.blit(burger_info, (358 ,468))

def map2(): # när map2live är true körs map2
    start_time1 = pygame.time.get_ticks()
  #  global zombie
    walkR_rect.y = 400
    pygame.display.set_caption("Fight") # namn på rutan
    map2 = pygame.image.load("grass_map.png")
    resolution.blit(map2, (0, 0))
    visa_score(text_x, text_y) # kör funktionen som visar dina kills på givna kordinater
    global zombiefart # global eftersom den ska ändras beroende på om de round 1 eller två
    zombie1rect.x -= zombiefart
    if zombie1rect.x <= 380:
        zombie1rect.y =320 # så det ser ut som att den går upp på blocket guben står på
    else:
        zombie1rect.y = 350
    resolution.blit(zombie1, zombie1rect)
    resolution.blit(fireballbild, fireballrect)
    global kills
    if kills < 7:
        global fireballfart
        fireballrect.y += fireballfart
        if fireballrect.y >= 415:
            fireballrect.y = -20
            fireballfart = random.randint(18, 27) # random fart mellan 18 och 27
            fireballrect.x = random.randint(10, 290) # spawna fireballen på random x mellan 10 och 250, improvement gör det i en lista så man kan tex visa med en röd prick vart nästa fireball hamnar innan den förra har landat
            resolution.blit(fireballbild, fireballrect) #visa fireballen

        if skottRect.colliderect(zombie1rect): # om zombien blir skjuten

            zombiefart = random.randint(10, 18) # ge zombien en ny fart
            zombie1rect.x = 560 # spawna tillbaks i början
            resolution.blit(zombie1, zombie1rect)
            global skottlive # ta bort skottet, sätts på igen om space bar trycks
            skottlive = False
            skottRect.x = walkR_rect.x - 5
            kills += 1 # addera till score

            global time1
            time1 = pygame.time.get_ticks()  # tiden ändras fram tills sista collission då loopen e slut
    elif 6 < kills < 20:
        timer1 = start_time1 - time1 #  en timer
        if timer1 < 4000: # om inte gått 4 sek visa bilden från round2 och zombie/fireball är med så att det inte ska ske collision under tiden
            zombie1rect.x = 600
            fireballrect.y = 0
            round2(0, 0)
        if timer1 > 4000: # om de gått 4 sekunder börja spelet igen
            global fireballfart2
            fireballrect.y += fireballfart2
            if fireballrect.y >= 440:
                fireballrect.y = -30
                fireballfart2 = random.randint(42, 62)
                fireballrect.x = random.randint(12, 290)
                resolution.blit(fireballbild, fireballrect)



            if skottRect.colliderect(zombie1rect):
                zombiefart = random.randint(16, 24)
                zombie1rect.x = 550
                resolution.blit(zombie1, zombie1rect)
                skottlive = False
                skottRect.x = walkR_rect.x - 5
                kills += 1
                global time2
                time2 = pygame.time.get_ticks() # samma princip som förra time1

    if kills > 19:
        timer2 = start_time1 - time2
        if timer2 < 3520: # visa you won bilden 3.4 sekunder sen ständav map2 och sätt på map1
            zombie1rect.x = 605
            fireballrect.y = 10
            you_won()
        if timer2 > 3400:
            global map2live
            map2live = False
            global map1live
            map1live = True
            global map1klar
            map1klar = True
            #ändra map1 till ny funktion med map och nya gubbar osånt heeejj


    if walkR_rect.colliderect(fireballrect): # dessa 2 är när man dör
        map2live = False
        you_lost()
    if walkR_rect.colliderect(zombie1rect):
        map2live = False
        you_lost()




prat1 = pygame.image.load("prat1.png")
prat1_x = 110
prat1_y = 200
prat2 = pygame.image.load("prat2.png")
prat2_x = 110
prat2_y = 200
map1klar = False # heeeehheheeehheheheehehe grrr
lastimer1gong = True
inte_vunnit = True
map1live = True
map2live = False
skottlive = False
live = True
prat2live = False
prat3live = False
mellanmaps_live = False
readonce = True
hej = 1
look = 1
skott1 = 1
while live:
    mouse_x , mouse_y = pygame.mouse.get_pos() # få musens position
    pygame.time.wait(50) # pausa lite för mindre lagg
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                live = False
        if event.type == pygame.QUIT:
            live = False # sätt att stänga av spelet
    if map1live:
        map1()
          #  spelare_x = 30
           # spelare_y = 400
        # i loopen så att man ej kan röra på sig innan man tryckt C i början
        resolution.blit(prat1, (prat1_x, prat1_y))
        if prat1_y == 200: # första prat
            enter_fight = False
        if input[pygame.K_c]: # dåligt sätt att ta bort första prat bubblan och ist visa den andra
            prat1_y = -200
            prat2live = True
            enter_fight = True # gör så man kan röra sig igen
        if prat2live: # funkar utan denhär raden men la till så att under tiden man collidar med gubben i dungeon ska texten försvinna
            resolution.blit(prat2, (prat2_x, prat2_y))
        if prat3live:
            pass # för sen
        input = pygame.key.get_pressed()
        if enter_fight:
            if input[pygame.K_a]:
                spelare_x -= fartmap1
            if input[pygame.K_d]:
                spelare_x += fartmap1
            if input[pygame.K_w]:
                spelare_y -= fartmap1
            if input[pygame.K_s]:
                spelare_y += fartmap1
        spelare = pygame.Rect(spelare_x, spelare_y, spelare_bredd, spelare_hojd)
        spelare_rect = pygame.draw.rect(resolution, (250, 250, 250), spelare)
        if spelare_x >= bredd - 20:
            spelare_x = bredd - 20
        if spelare_x <= 0:
            spelare_x = 0
        if spelare_y >= hojd - 20:
            spelare_y = hojd - 20
        if spelare_y <= 0:
            spelare_y = 0 # dessa ^ så man ej kan gå ut ur map1

            # här fixa så man ej kan gå på vattnet


        if map1klar: # när du vunnit blir den true och visar en hamburgare som reward som också använder mus position för att visa info texten (i funktionen)
            reward_bild()
        if inte_vunnit: # så länge man inte vunnit kan man collide med gubben i dungeon, annars går det ej.
            if obj_rect.colliderect(spelare_rect):
                enter_fight = False # kan ej röra dig utan du måste trycka e eller q
                prat2live = False # ta bort första pratbubblan
                resolution.blit(enter_fight_press, (0, 0))
                resolution.blit(innan_fight_pratbubbla, (350, 200))

                if input[pygame.K_e]:
                    map1live = False
                    map2live = True
                    reset_map2() # om e trycks starta map2 och refresha den med hjälp av funktion
                if input[pygame.K_q]: # du kan röra dig igen
                    enter_fight = True
                    spelare_x = 525
                    spelare_y = 286

            elif not prat1_y == 200: # pratbubblan kommer tillbaks om du trycker q. men bara första gången inte efter du redan kört en gång.
                prat2live = True
        elif not inte_vunnit: # bara test
            gun = pygame.image.load("gun.png")
            resolution.blit(gun, (480, 242))
    if map2live:
        map2()
        input = pygame.key.get_pressed()

        if input[pygame.K_a]:
            walkR_rect.x -= fartmap2
            look = 0

        if input[pygame.K_d]:
            walkR_rect.x += fartmap2
            look = 1

        walkL_rect = walkR_rect # gubben som visar att du rör dig åt vänster ska vara samma som den åt höger

        if look == 0: #när du trycker a rörs gubben left och moveleft bilden visas
            resolution.blit(walk_left, walkL_rect)
        if look == 1: # samma princip
            resolution.blit(walk_right, walkR_rect)


        if walkR_rect.x >= 295:
            walkR_rect.x = 295
        if walkR_rect.x <= 0:
            walkR_rect.x = 1
        if walkL_rect.x <= 0:
            walkL_rect = 0
        if walkL_rect.x >= 295:
            walkL_rect.x = 295 # så  du ej kan gå utanför

        if input[pygame.K_SPACE]: # om du skjuter kollar gubben åt höger
            look = 1
            skottlive = True
        if skottlive:
            skottRect.x += 33 # skottets hastighet
            resolution.blit(skottbild, skottRect)
        if skottRect.x >= bredd: # skottet försvinner om den åker utanför mapen men detta är förutom under round 2 bilden omöjligt eftersom den alltid kommer collide med zombie
            skottRect.x = walkR_rect.x
            skottlive = False

    if mellanmaps_live: # om du förlorar :
        input = pygame.key.get_pressed()
        if input[pygame.K_c]: # om du trycker c tas du tillbaks till map1 spawn
            map1live = True
            prat2_y = -200
            spelare_x = 30
            spelare_y = 400
            prat3live = True # lägg ny prat på denhär som gubben vid spawn säger
            #map2 stängs redan av efter collisionen då den måste stängas av direkt ( annars fortsätter spelet ändå)


    pygame.display.flip()  #visar ändringarna som gjorts på skärmen
    clock.tick(60) # FPS
pygame.quit() # om loopen avslutas stängs allt av
sys.exit()
