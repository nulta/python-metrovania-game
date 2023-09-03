from pygame.locals import *
from constants import *
import pygame

# InputManager는 키보드 입력을 받아서 예쁘게 정리해주는 일을 한다.
# 이를테면, InputManager.held(KEY_LEFT) 같은 식으로 키를 받아올 수 있게.
#
# 플레이어의 입력을 인식하는 방식은 크게 세 종류로 나뉜다.
# 1. pressed - 방금 눌린 상태.
#    누른 즉시 딱 한 프레임동안만 True.
#    이를테면 스킬 발동이나 공격 키처럼. 얘네들은 눌렀을 때 한번만 발동하니까.
# 2. held - 누르고 있는 상태.
#    누르고 있을 때 True.
#    이를테면 상하좌우 이동 키처럼.
# 3. released - 방금 손을 뗀 상태.
#    눌려 있었다가 떼어진 한 프레임동안만 True.
#
# InputManager는 위의 세 입력을 분류해서 받아들인다.
# 또, (필요하다면) 조작키를 설정을 통해 바꿀 수도 있게 해 준다.
# 또, (진짜로 필요하다면) 나중에 게임패드 등을 지원하기도 더 편하게 해 준다.

class InputManager():
    """사용자의 입력을 받고 그 상태를 알려준다."""

    # 액션에 대응하는 키의 집합들.
    _action_table: "dict[int, set[int]]" = {
        ACTION_UP: {K_w, K_UP},
        ACTION_DOWN: {K_s, K_DOWN},
        ACTION_LEFT: {K_a, K_LEFT},
        ACTION_RIGHT: {K_d, K_RIGHT},
        ACTION_CHANGE_RIGHT: {K_KP_PERIOD},   
        ACTION_CHANGE_LEFT: {K_COMMA},
        ACTION_JUMP: {K_SPACE},
        ACTION_SHOOT: {K_k},
        ACTION_CONFIRM: {K_SPACE, K_RETURN},
        ACTION_CANCEL: {K_ESCAPE}       
    }

    # 마지막 프레임에서 눌려있었던 액션들의 집합.
    _last_held_actions = set()

    # 현재 프레임에서 액션들의 pressed/held/released/None 상태.
    _action_status: "dict[int, (int|None)]" = {}

    # 이 클래스 내에서만 사용할 상수.
    _PRESSED = 0
    _HELD = 1
    _RELEASED = 2

    @classmethod
    def update(cls):
        # 키 입력 정보를 받아온다.
        pressed = pygame.key.get_pressed()
        current_held_actions = set()

        for action, keys in cls._action_table.items():
            # 액션의 키가 눌려 있는지 확인한다.
            if any(pressed[k] for k in keys):
                current_held_actions.add(action)

            # 이전 프레임과 지금 프레임의 키 입력 정보를 가지고 액션의 입력 정보를 계산한다.
            then = action in cls._last_held_actions
            now = action in current_held_actions
            cls._action_status[action] = cls._get_action_status(then, now)

        # 클래스 내부 상태를 업데이트한다.
        cls._last_held_actions = current_held_actions
    
    @classmethod
    def _get_action_status(cls, then, now):
        if then and now:
            return cls._HELD
        elif not then and now:
            return cls._PRESSED
        elif then and not now:
            return cls._RELEASED
        else:
            return None


    @classmethod
    def held(cls, action: int):
        """어떤 버튼이 '지금 눌려있는지'를 판정한다."""
        status = cls._action_status.get(action, None)
        return (status == cls._PRESSED) or (status == cls._HELD)

    @classmethod
    def pressed(cls, action: int):
        """어떤 버튼이 '방금 눌러졌는지'를 판정한다."""
        status = cls._action_status.get(action, None)
        return status == cls._PRESSED

    @classmethod
    def released(cls, action: int):
        """어떤 버튼이 '방금 떼어졌는지'를 판정한다."""
        status = cls._action_status.get(action, None)
        return status == cls._RELEASED

    @classmethod
    def axis(cls, axis: int) -> float:
        """어떤 이동축의 값을 받아온다.

        이동축의 값은 -1 이상 +1 이하의 실수이며, 키보드 또는 조이스틱으로 조작한다.
        """
        # 이 두개 말고 다른 축을 추가할 일이 있을까?---:없을듯함다
        value = 0.0
        if axis == AXIS_HORIZONTAL:
            if cls.held(ACTION_LEFT): value -= 1.0
            if cls.held(ACTION_RIGHT): value += 1.0
        elif axis == AXIS_VERTICAL:
            if cls.held(ACTION_DOWN): value -= 1.0
            if cls.held(ACTION_UP): value += 1.0

        return min(max(value, -1.0), 1.0)
