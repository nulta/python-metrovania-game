import random
import pygame
from entities import *
import globals

class Game():
    """메인 게임 클래스. 메인 루프를 관리한다."""

    def __init__(self):
        # 초기화
        pygame.init()
        pygame.display.set_caption(GAME_WINDOW_NAME)
        self.screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        
        # 메인 루프
        while not globals.exit:
            self.update_clock()
            self.update_events()
            self.process_draw()
            pygame.display.flip()

        # 종료 연출
        self.exit_fadeout()

    def update_clock(self):
        """FPS를 유지하고 globals.delta_time을 업데이트한다."""
        globals.delta_time = self.clock.tick(GAME_MAX_FPS) / 1000
        globals.frame_count += 1
        globals.game_time += globals.delta_time

    def update_events(self):
        """event를 받아서 처리한다."""
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                globals.exit = True
    
    def process_draw(self):
        """게임 화면을 그린다."""
        # 임시용.
        self.screen.fill((0, 180, 255))

    def exit_fadeout(self):
        """게임 화면을 페이드아웃한다."""
        fader = pygame.Surface(GAME_WINDOW_SIZE)
        fader.fill((0, 0, 0))
        fader.set_alpha(255 / GAME_MAX_FPS * 9)

        t = 0
        while t < 0.3:
            pygame.event.pump()
            t += self.clock.tick(GAME_MAX_FPS) / 1000
            self.screen.blit(fader, (0, 0))
            pygame.display.update()


if __name__ == "__main__":
    Game()
