from pygame.locals import *
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

# ACTION 상수
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3
ACTION_JUMP = 4
ACTION_SHOOT = 5

# AXIS 상수
AXIS_HORIZONTAL = 0
AXIS_VERTICAL = 1

class InputManager():
    """사용자의 입력을 받고 그 상태를 알려준다."""
    
    # 키에 대응하는 액션의 이름.
    _key_table = {
        K_UP: ACTION_UP,
        K_DOWN: ACTION_DOWN,
        K_LEFT: ACTION_LEFT,
        K_RIGHT: ACTION_RIGHT,
        K_SPACE: ACTION_JUMP,
        K_z: ACTION_JUMP,
        K_x: ACTION_SHOOT,
    }

    # 모든 액션들의 집합.
    _all_actions = set(_key_table.values())

    # 마지막 프레임에서 눌려있었던 액션들의 집합.
    _last_held_actions = set()

    # 현재 프레임에서 액션들의 pressed/held/released 상태.
    # 아무것도 아닌 경우, 키가 존재하지 않는다.
    _action_status: "dict[int, int]" = {}

    # 이 클래스 내에서만 사용할 상수.
    _PRESSED = 0
    _HELD = 1
    _RELEASED = 2

    @classmethod
    def update(self):
        # 키 입력 정보를 받아온다.
        keys = pygame.key.get_pressed()
        current_held_actions = set()
        for key, action in self._key_table.items():
            if keys[key]:
                # 현재 이 키가 눌려 있다.
                current_held_actions.add(action)
        
        # 이전 프레임과 지금 프레임의 키 입력 정보를 가지고 액션의 입력 정보를 계산한다.
        for action in self._all_actions:
            on_prev_frame = action in self._last_held_actions
            on_current_frame = action in current_held_actions

            if on_prev_frame and on_current_frame:
                # 이전 프레임에서도, 지금 프레임에서도 눌려 있다.
                self._action_status[action] = self._HELD
            elif not on_prev_frame and on_current_frame:
                # 지금 프레임에서만 눌려 있다.
                self._action_status[action] = self._PRESSED
            elif on_prev_frame and not on_current_frame:
                # 이전 프레임에서만 눌려 있었다.
                self._action_status[action] = self._RELEASED
            else:
                # 이전 프레임에서도, 지금 프레임에서도 눌려있지 않다.
                if action in self._action_status:
                    del self._action_status[action]
        
        # 클래스 내부 상태를 업데이트한다.
        self._last_held_actions = current_held_actions
    
    @classmethod
    def held(self, action: int):
        """어떤 버튼이 '지금 눌려있는지'를 판정한다."""
        print(self._action_status)
        status = self._action_status.get(action, None)
        return (status == self._PRESSED) or (status == self._HELD)
    
    @classmethod
    def pressed(self, action: int):
        """어떤 버튼이 '방금 눌러졌는지'를 판정한다."""
        status = self._action_status.get(action, None)
        return status == self._PRESSED
    
    @classmethod
    def released(self, action: int):
        """어떤 버튼이 '방금 떼어졌는지'를 판정한다."""
        status = self._action_status.get(action, None)
        return status == self._RELEASED
    
    @classmethod
    def axis(self, axis: int) -> float:
        """어떤 이동축의 값을 받아온다.
        
        이동축의 값은 -1 이상 +1 이하의 실수이며, 키보드 또는 조이스틱으로 조작한다.
        """
        # 이 두개 말고 다른 축을 추가할 일이 있을까?
        value = 0.0
        if axis == AXIS_HORIZONTAL:
            if self.held(ACTION_LEFT): value -= 1.0
            if self.held(ACTION_RIGHT): value += 1.0
        elif axis == AXIS_VERTICAL:
            if self.held(ACTION_DOWN): value -= 1.0
            if self.held(ACTION_UP): value += 1.0

        return min(max(value, -1.0), 1.0)
