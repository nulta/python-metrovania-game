import random
import pygame
import game_globals
from entities import *
from input_manager import *
from entity_manager import EntityManager

class Game():
    """메인 게임 클래스. 메인 루프를 관리한다."""

    def __init__(self):
        # 초기화
        pygame.init()
        pygame.display.set_caption(GAME_WINDOW_NAME)
        self.screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, 30)  # 임시용
        self.initialize_game()

        # 메인 루프
        while not game_globals.exit:
            self.update_clock()
            self.update_events()
            self.update_input()
            self.update_entities()
            self.process_draw()

        # 종료 연출
        self.exit_fadeout()
    
    def initialize_game(self):
        """게임 상태를 초기화한다."""
        player = Player(GENDER_FEMALE)
        player.position = Vector2(20, 200)
        EntityManager.push_entity(player)

    def update_clock(self):
        """FPS를 유지하고 globals.delta_time을 업데이트한다."""
        game_globals.delta_time = self.clock.tick(GAME_MAX_FPS) / 1000
        game_globals.frame_count += 1
        game_globals.game_time += game_globals.delta_time
        game_globals.frames_per_second = self.clock.get_fps()

    def update_input(self):
        """InputManager를 업데이트한다."""
        InputManager.update()

    def update_events(self):
        """event를 받아서 처리한다."""
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                game_globals.exit = True

    def update_entities(self):
        """모든 Entity들을 업데이트한다."""
        EntityManager.update()

    def process_draw(self):
        """게임 화면을 그린다."""
        # 배경을 그린다.
        self.screen.fill((0, 180, 255))

        # 엔티티를 그린다.
        EntityManager.draw(self.screen)

        # DEBUG: FPS 카운터를 그린다.
        surface = self._font.render(f"FPS: {int(game_globals.frames_per_second)}", True, (255,255,255))
        self.screen.blit(surface, (0, 0))

        # 화면에 띄운다.
        pygame.display.flip()

    def exit_fadeout(self):
        """게임 화면을 페이드아웃한다."""
        fader = pygame.Surface(GAME_WINDOW_SIZE)
        fader.fill((0, 0, 0))
        fader.set_alpha(int(255 / GAME_MAX_FPS * 9))

        t = 0
        while t < 0.3:
            pygame.event.pump()
            t += self.clock.tick(GAME_MAX_FPS) / 1000
            self.screen.blit(fader, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    Game()
