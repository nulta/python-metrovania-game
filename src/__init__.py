import random
import pygame
import pygame.freetype
import game_globals
import debug
from fonts import Fonts
from entities import *
from constants import *
from input_manager import InputManager
from scene_manager import SceneManager
from scenes import TitleScene

class Game():
    """메인 게임 클래스. 메인 루프를 관리한다."""

    def __init__(self):
        # 초기화
        pygame.init()
        pygame.freetype.init()
        pygame.display.set_caption(GAME_WINDOW_NAME)
        self.screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.initialize_game()

        # 메인 루프
        while not game_globals.exit:
            self.update_clock()
            self.update_events()
            self.update_input()
            self.update_scene()
            self.process_draw()

        # 종료 연출
        if isinstance(SceneManager.current_scene ,TitleScene):
            self.exit_fadeout()

    def initialize_game(self):
        """게임 상태를 초기화한다."""
        SceneManager.push_scene(TitleScene())

    def update_clock(self):
        """FPS를 유지하고 globals.delta_time을 업데이트한다."""
        game_globals.delta_time = self.clock.tick(GAME_MAX_FPS) / 1000
        game_globals.delta_time = min(game_globals.delta_time, GAME_MAX_DELTA_TIME)
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

    def update_scene(self):
        """Scene을 업데이트한다."""
        result = SceneManager.update()

        # Scene이 텅 비었다면, 게임을 종료한다.
        if not result:
            print("No scene to update! exitting...")
            game_globals.exit = True

    def process_draw(self):
        """게임 화면을 그린다."""
        # 배경을 그린다.
        self.screen.fill((0, 180, 255))

        # Scene을 그린다.
        SceneManager.draw(self.screen)

        if DEBUG_MODE:
            # FPS 카운터를 그린다.
            Fonts.get("debug").render_to(
                self.screen,
                (4, 4),
                f"FPS: {int(game_globals.frames_per_second)}",
                fgcolor=(255, 255, 255),
            )

            # debug draw를 한다
            debug.draw_debug_elements(self.screen)

        # 화면에 띄운다.
        pygame.display.flip()

    def exit_fadeout(self):
        """게임을 종료하기 전, 화면을 페이드아웃한다."""
        # 음악을 페이드 아웃한다
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(200)

        # 화면을 가릴 Surface
        fader = pygame.Surface(GAME_WINDOW_SIZE)
        fader.fill((0, 0, 0))
        fader.set_alpha(int(255 / GAME_MAX_FPS * 9))

        # 0.3초간 페이드 아웃 효과를 준다
        t = 0
        while t < 0.3:
            # 도중에 Exit 요청이 또 들어왔다면 즉시 종료한다
            if pygame.event.get(pygame.QUIT, pump=True):
                exit()
            t += self.clock.tick(GAME_MAX_FPS) / 1000
            self.screen.blit(fader, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    Game()
