import pygame
import random
from main_menu import MainMenu

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel_height = 150
screen_width = 800
screen_height = 400 + bottom_panel_height

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Main game')

#Initialize MainMenu
main_menu = MainMenu(screen)

#game variables
state = 'menu'
level = 1 #controla o nivel atual do jogo 
total_stages = 3
curret_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0


medieval_font = pygame.font.Font('ancient/Ancient.ttf',20)

#define colours
red = (139,0,0)
green = (0,255,0)
yellow = (255,255,0)

#background image/ formating the img
background_img = pygame.image.load('textures/background-forest.webp').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Reduzir o tamanho da imagem para criar um efeito pixelado
small_img = pygame.transform.scale(background_img, (400, 200))

# Ampliar a imagem de volta para o tamanho da tela
pixelated_img = pygame.transform.scale(small_img, (screen_width, screen_height))

#create function draw text
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img, (x, y))

# Função para desenhar o fundo pixelado
def draw_bg():
    screen.blit(pixelated_img, (0, -100))


#panel img/ sword cursor
panel_img = pygame.image.load('textures/panel.png').convert_alpha()

#potion
potion_img = pygame.image.load('img/potions/health_potion.png').convert_alpha()

#victory and defeat
victory_img = pygame.image.load('img/victory1.png').convert_alpha()
defeat_img = pygame.image.load('img/defeat1.png').convert_alpha()

victory_img = pygame.transform.scale(victory_img, (200, 100))


#restart
restart_img = pygame.image.load('img/restart.png').convert_alpha()


#cursor icon
sword_img = pygame.image.load('img/sword.cur').convert_alpha()



bottom_panel_color = (0,0,0)


#function for drawing panel
def draw_panel():
   #draw panel rectangle
   screen.blit(panel_img, (0,screen_height - bottom_panel_height))
   #show knight stats
   draw_text(f'{knight.name} HP: {knight.hp}', medieval_font,red,100,screen_height - bottom_panel_height + 10)
   for count, i in enumerate(bandit_list):
       #show name and health 
       draw_text(f'{i.name} HP: {i.hp}', medieval_font,red,550, (screen_height - bottom_panel_height + 10)+ count * 60)

#figther class
class Fighter():
    def __init__(self, x,y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.block_chance = 0.2
        self.animation_list = {'idle':[],'attack':[],'block': [], 'hurt':[],'death':[]}
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()       
     # Definindo os fatores de escala para cada personagem
        scale_factors = {
            'Knight': 4,  # Tamanho original do cavaleiro
            'Bandit': 3   # Tamanho reduzido dos bandidos
            }
        scale_factor = scale_factors.get(self.name, 1)  # Usar 1 se o personagem não estiver no dicionário
        self.load_animations(scale_factor)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def load_animations(self, scale_factor):
        # load idle animation
        if self.name == 'Knight':
            sprite_sheet = pygame.image.load(f'img/{self.name}/knight_idle.png').convert_alpha()
            sheet_width = sprite_sheet.get_width()
            sheet_height = sprite_sheet.get_height()
            frame_width = sheet_width // 4  # Adjust based on the number of frames in the sprite sheet
            frame_height = sheet_height

            for i in range(4): 
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * scale_factor, frame_height * scale_factor))
                self.animation_list['idle'].append(frame)
            # load attack animations 
            for i in range(10):
                img = pygame.image.load(f'img/{self.name}/attack/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
                self.animation_list['attack'].append(img)

            #cut block animations
            sprite_sheet = pygame.image.load(f'img/{self.name}/knight_block.png').convert_alpha()
            sheet_width = sprite_sheet.get_width()
            sheet_height = sprite_sheet.get_height()
            frame_width = sheet_width // 7  # Adjust based on the number of frames in the sprite sheet
            frame_height = sheet_height
            #load block frames
            for i in range(7):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * scale_factor, frame_height * scale_factor))
                self.animation_list['block'].append(frame)

            # load hurt animations
            for i in range(3):
                img = pygame.image.load(f'img/{self.name}/hurt/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
                self.animation_list['hurt'].append(img)
            
            #cut death frames
            sprite_sheet = pygame.image.load(f'img/{self.name}/knight_death.png').convert_alpha()
            sheet_width = sprite_sheet.get_width()
            sheet_height = sprite_sheet.get_height()
            frame_width = sheet_width // 9  # Adjust based on the number of frames in the sprite sheet
            frame_height = sheet_height
            #load death frames
            for i in range(9):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (frame_width * scale_factor, frame_height * scale_factor))
                self.animation_list['death'].append(frame)
            
            
        else:
            # Load each frame individually for other characters
            img_count = 3 
            for i in range(img_count):
                img = pygame.image.load(f'img/{self.name}/idle/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
                self.animation_list['idle'].append(img)

            #load attack animations 
            img_count=8
            for i in range(img_count):
                img = pygame.image.load(f'img/{self.name}/attack/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
                self.animation_list['attack'].append(img)

            #load hurt animations
            img_count=2
            for i in range(img_count):
                img = pygame.image.load(f'img/{self.name}/hurt/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
                self.animation_list['hurt'].append(img)

            #load death animations
            img_count=9
            for i in range(img_count):
                img = pygame.image.load(f'img/{self.name}/death/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
                self.animation_list['death'].append(img)

    def update(self):
        animation_cooldown = 150
        
            #animation and update image
        self.image = self.animation_list[self.action][self.frame_index]
        previous_center = self.rect.center   # Salva o centro atual do personagem
        self.rect = self.image.get_rect(center=previous_center) # Aplica a nova imagem mantendo o centro

        #check time passed
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #loop for the animation
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 'death':
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()



    def idle(self):
        self.action = 'idle'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self,target):
        self.action = 'attack'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        if target.block(self):
            return
        #damage
        rand = random.randint(-5,5)
        damage = self.strength + rand
        critical = random.random() < 0.1 #10% chance of critical attack
        if critical:
            damage *= 2
        target.hp -= damage
        target.hurt() #calls hurt aniamtion
        #check if character is death
        if target.hp <= 1:
            target.hp = 0
            target.alive = False
            target.death()
        #create damage text    
        damage_text = DamageText(target.rect.centerx,target.rect.y, str(damage), red, critical)
        damage_text_group.add(damage_text)
        #attack animations 
        


    def block(self, attacker):
        if self.name == 'Knight':
            if random.random() < self.block_chance:
                self.action = 'block'
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()
                damage_text = DamageText(self.rect.centerx, self.rect.y, 'Blocked!',(255,255,255) )
                damage_text_group.add(damage_text)
                #logica para block
                return True 
            return False
            


    def hurt(self):
        self.action = 'hurt'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def death(self):
        self.action = 'death'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.alive = False


    def perform_heal(character, heal_amount):
        if character.alive and character.potions > 0:
            actual_heal = min(heal_amount, character.max_hp - character.hp)
            character.hp += actual_heal
            character.potions -= 1
            damage_text = DamageText(character.rect.centerx,character.rect.y, str(heal_amount), green,)
            damage_text_group.add(damage_text)
            return True
        return False

   #reset the game 
    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()



# rect position the image 
    def draw(self):
        screen.blit(self.image,self.rect)

    


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp 
        self.max_hp = max_hp


    def draw(self,hp):
        #uptade health
        self.hp = hp
        #calculate health
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen,red,(self.x,self.y,150,20))
        pygame.draw.rect(screen,green,(self.x,self.y,150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour, critical = False):
        pygame.sprite.Sprite.__init__(self)
        self.colour = yellow if critical else colour #critical hit yellow
        self.image = medieval_font.render(str(damage), True, self.colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        #erase damage
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()




class Button():
    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        action = False
        #desenha botao
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
         #get mouse position
        pos = pygame.mouse.get_pos()
            #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            #draw button

            return action


#instance of the class/ positions and health
knight = Fighter(200,260,'Knight',30,10,3)
bandit1 = Fighter(550,270,'Bandit',20,6,1)
bandit2 = Fighter(700,270,'Bandit',20,6,1)


bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)


knight_health_bar = HealthBar(100,screen_height - bottom_panel_height + 40, knight.hp, knight.max_hp )
bandit1_health_bar = HealthBar(550,screen_height - bottom_panel_height + 40, bandit1.hp, bandit1.max_hp )
bandit2_health_bar = HealthBar(550,screen_height - bottom_panel_height + 100, bandit2.hp, bandit2.max_hp )


#create button 
potion_button = Button(screen,100,screen_height - bottom_panel_height + 70, potion_img, 64,64)

#restart button 
restart_button = Button(screen,330,145 , restart_img, 120, 40)



# Maintain the game window
run = True
while run:
    if state == 'menu':
        state = main_menu.run()

    if state == 'game':
        clock.tick(fps)
        #draw background
        draw_bg()

        #draw panel
        draw_panel()
        knight_health_bar.draw(knight.hp)
        bandit1_health_bar.draw(bandit1.hp)
        bandit2_health_bar.draw(bandit2.hp)

        #draw fighters
        knight.update()
        knight.draw()

        #draw bandits
        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        #damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        #controle player actions
        #reset action variables
        attack = False
        potion = False
        target = None
        pygame.mouse.set_visible(True) #hide mouse
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                pygame.mouse.set_visible(False) #hide mouse
                screen.blit(sword_img, pos)  #show sword
                if clicked == True and bandit.alive == True:
                    attack = True
                    target = bandit_list[count]
        if potion_button.draw():
            potion = True
        draw_text(str(knight.potions), medieval_font, red, 150, screen_height - bottom_panel_height + 70)

        if game_over == 0:
            #player action
            if knight.alive:
                if curret_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                        if attack and target is not None:
                            knight.attack(target)
                            curret_fighter+=1
                            action_cooldown = 0
                        #potion
                        if potion:
                            if Fighter.perform_heal(knight, potion_effect):
                                curret_fighter += 1
                                action_cooldown = 0
                                potion = False  # Reset potion flag
            else:
                game_over = -1


            #enemies actions to attack, heal, etc
            for count, bandit in enumerate(bandit_list):
                if curret_fighter == 2 + count:
                        if bandit.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                #bandit potion 
                                if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                                    if Fighter.perform_heal(bandit, potion_effect):
                                        curret_fighter += 1
                                        action_cooldown = 0
                                        continue
                                #look for player action
                                #attack
                                bandit.attack(knight)
                                curret_fighter+=1
                                action_cooldown = 0
                        else:
                            curret_fighter +=1

            if curret_fighter > total_fighters:
                curret_fighter = 1


        #check bandits are dead
        alive_bandits = 0
        for bandit in bandit_list:
            if bandit.alive == True:
                alive_bandits += 1 
        if alive_bandits == 0:
            game_over = 1     

        #check game over 
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (289,30))
            if game_over == -1:
                screen.blit(defeat_img, (289,30))
            if restart_button.draw():
                knight.reset()
                for bandit in bandit_list:
                    bandit.reset()
                curret_fighter = 1
                game_over = 0

    
    #close the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

    #Update the events
        pygame.display.update()
pygame.quit()


