# 이 파일에는 상수를 모아놓는다.
# 상수는 프로그램이 실행되는 동안 "변하지 않는" 변수이다.
# 상수의 이름은 전부 대문자로 작성한다.

# 설정 값
GAME_WINDOW_NAME = "게임 이름"
RESOURCE_PATH = "./resources"
TILE_SIZE = 30 * 2

GAME_WINDOW_SIZE = (840, 600)  # 30*2의 배수
# GAME_MAX_FPS = 144
GAME_MAX_FPS = 60
GAME_MAX_DELTA_TIME = 1/20


# GENDER 값
GENDER_MALE   = 0
GENDER_FEMALE = 1

#속도, 질량
PLAYER_MOVE_SPEED = 300


# ACTION 상수 (InputManager)
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3
ACTION_JUMP = 4
ACTION_SHOOT = 5
ACTION_CHANGE = 6  # 무기 바꾸기
ACTION_CONFIRM = 7 # 확인 키 (메뉴 화면에서)
ACTION_CANCEL = 8  # 취소 키 (메뉴 화면에서)

# AXIS 상수
AXIS_HORIZONTAL = 0
AXIS_VERTICAL = 1


# pygame.freetype.STYLE_* 상수
from pygame.freetype import (
    STYLE_DEFAULT as FONT_STYLE_DEFAULT,
    STYLE_NORMAL as FONT_STYLE_NORMAL,
    STYLE_STRONG as FONT_STYLE_STRONG,
    STYLE_OBLIQUE as FONT_STYLE_OBLIQUE,
    STYLE_UNDERLINE as FONT_STYLE_UNDERLINE,
    STYLE_WIDE as FONT_STYLE_WIDE,
)
