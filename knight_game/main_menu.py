import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800, 550))
pygame.display.set_caption("Menu")

BG = pygame.image.load("img/menu_background.png")

def get_font(size):
    return pygame.font.Font('ancient/Ancient.ttf', size)

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = get_font
        self.running = True

        # Define os botões aqui para que possam ser acessados por outros métodos
        self.PLAY_BUTTON = Button(image=pygame.image.load("img/play.png"), pos=(400, 200), 
                                  text_input="PLAY", font=self.font(75), base_color="#d7fcd4", hovering_color="White")
        self.OPTIONS_BUTTON = Button(image=pygame.image.load("img/options.png"), pos=(400, 300), 
                                     text_input="OPTIONS", font=self.font(75), base_color="#d7fcd4", hovering_color="White")
        self.QUIT_BUTTON = Button(image=pygame.image.load("img/quit.png"), pos=(400, 400), 
                                  text_input="QUIT", font=self.font(75), base_color="#d7fcd4", hovering_color="White")

    def draw(self):
        self.screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = self.font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 50))
        self.screen.blit(MENU_TEXT, MENU_RECT)

        # Desenha os botões
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.PLAY_BUTTON.checkForInput(pos):
                    return 'start'
                if self.OPTIONS_BUTTON.checkForInput(pos):
                    return 'options'
                if self.QUIT_BUTTON.checkForInput(pos):
                    return 'quit'
        return 'menu'

    def run(self):
        while self.running:
            self.draw()
            action = self.handle_events()
            if action == 'start':
                return 'game'
            elif action == 'options':
                return 'options'
            elif action == 'quit':
                pygame.quit()
                sys.exit()

# Para rodar o menu principal
if __name__ == "__main__":
    menu = MainMenu(SCREEN)
    menu.run()
