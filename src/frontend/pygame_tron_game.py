import pygame

from src.frontend.tron_game import TronGame

class PygameTronGame(TronGame):
    def set_waiting_for_players(self, is_waiting):
        pass

    def set_on_get_players(self, on_get_players):
        pass

    def set_on_player_move(self, on_player_move):
        pass

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode([500, 500])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))

            pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

            pygame.display.flip()
        
        pygame.quit()
            
                


