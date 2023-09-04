# 이 파일에는 게임 전체에서 사용될 전역 변수를 모아놓는다.
# 전역 변수는 남용하면 코드의 흐름을 흐트리고 코드를 읽기
# 어렵게 하기 때문에, 조심해서 써야 한다.

delta_time: float = 0.0
"매 프레임 업데이트된다. 이전 프레임과의 시간 차이(초 단위)."

exit: float = False
"이 값이 True가 되면 게임이 종료된다."

frame_count: int = 0
"게임이 켜진 이후로부터 지나간 프레임 수."

game_time: float = 0.0
"게임이 켜진 이후로부터 지나간 시간 (초)."

frames_per_second: float = 0.0
"현재 FPS 값. delta_time의 역수보다 정확한 값이다."

if True:
    #TODO: 제대로 된 카메라 클래스 만들기
    from pygame import Vector2
    global camera_offset
    camera_offset: "Vector2" = Vector2(0, 0)
    "카메라의 위치." 

player_gender = 1
"주인공 캐릭터의 성별값."
