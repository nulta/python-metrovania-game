from pygame import Vector2, Rect
from typing import TYPE_CHECKING, Sequence
import game_globals
import debug
from constants import TILE_SIZE

if TYPE_CHECKING:
    from entity import Entity

class PhysicsComponent:
    def __init__(self, owner: "Entity"):
        self._owner = owner
        self._velocity = Vector2(0, 0)   # pixels per second
        self._gravity = Vector2(0, 900)  # pixels per second

        # TODO: 타일맵 어떻게 불러와야 함???
        _ = None
        self._static_tilemap = [
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, 2, 2, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, 2, 2, _, _, _, _, _, _, _, _],
                [6, _, _, _, 6, 6, _, 2, 2, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 2, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 6, 2, 2, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ]
        self._static_tilemap = list(map(lambda row: list(map(bool, row)), self._static_tilemap))
        self._tile_size = TILE_SIZE
        # TODO: 맵과 엔티티의 충돌 판정 처리?
        # TODO: 엔티티와 엔티티의 충돌 판정 처리?

    @property
    def owner(self):
        return self._owner

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, val: "Vector2"):
        self._velocity = Vector2(int(val.x), int(val.y))


    def update(self):
        # print("===== NEW FRAME =====")
        self._update_gravity()
        self.owner.position += self.velocity * game_globals.delta_time
        self._update_collision()
    
    def _update_collision(self):
        # 지금은 일단 맵과의 충돌만 처리하고 있다.

        vel = self.velocity

        collided = False
        rep_x = 0.0
        rep_y = 0.0
        # 최대 10번 반복한다
        # for _ in range(10):
        #     collided = False
        #     for rect in self._get_collide_rects():
        #         repulse_vec = self._get_repulse_vector(vel, rect)
        #         if repulse_vec:
        #             print(repulse_vec)
        #             self.owner.position += repulse_vec
        #             vel = Vector2(0, 0)
        #             collided = True

        #     # 아무하고도 충돌하지 않았다면, 루프에서 빠져나간다
        #     if not collided:
        #         break
        
        # if collided:
        #     # 방금 루프는, 10회 제한이 없었다면 무한 루프로 빠졌을 수도 있다
        #     # 별로 좋지 않은 경우이다. 경고를 해 주자.
        #     print(f"PhysicsComponent of {repr(self.owner)}: Failed to solve the collisions"
        #           + "in 10 times. Possible physics error?")

        orig_pos = self.owner.position

        for rect in self._get_collide_rects():
            repulse_vec = self._get_repulse_vector(vel, rect)
            if repulse_vec.x:
                rep_x = repulse_vec.x
            if repulse_vec.y:
                rep_y = repulse_vec.y
        
        if rep_x and rep_y:

            if rep_x > rep_y:
                # X만 움직여도 되지 않을까?
                has_collision = False
                vel2 = Vector2(vel.x, 0)
                self.owner.position = orig_pos + Vector2(0, rep_y)
                for rect in self._get_collide_rects():
                    # TODO: optimize. 여기선 충돌하는지 여부만 판정해도 되는데 불필요하게 연산을 하고 있다.
                    repulse_vec = self._get_repulse_vector(vel2, rect)
                    if repulse_vec:
                        has_collision = True
                        continue

                # Y만 움직여도 되지 않을까?
                if has_collision:
                    has_collision = False
                    vel2 = Vector2(0, vel.y)
                    self.owner.position = orig_pos + Vector2(rep_x, 0)
                    for rect in self._get_collide_rects():
                        # TODO: optimize. 여기선 충돌하는지 여부만 판정해도 되는데 불필요하게 연산을 하고 있다.
                        repulse_vec = self._get_repulse_vector(vel2, rect)
                        if repulse_vec:
                            has_collision = True
                            continue
                
                if has_collision:
                    # 앗, 무조건 둘 다 움직여야 하는구나.
                    vel = Vector2(0, 0)
                    self.owner.position.x = orig_pos.x + rep_x
                    self.owner.position.y = orig_pos.y + rep_y
                else:
                    vel = vel2
            else:
                # Y만 움직여도 되지 않을까?
                has_collision = False
                vel2 = Vector2(0, vel.y)
                self.owner.position = orig_pos + Vector2(rep_x, 0)
                for rect in self._get_collide_rects():
                    # TODO: optimize. 여기선 충돌하는지 여부만 판정해도 되는데 불필요하게 연산을 하고 있다.
                    repulse_vec = self._get_repulse_vector(vel2, rect)
                    if repulse_vec:
                        has_collision = True
                        continue

                # X만 움직여도 되지 않을까?
                if has_collision:
                    has_collision = False
                    vel2 = Vector2(vel.x, 0)
                    self.owner.position = orig_pos + Vector2(0, rep_y)
                    for rect in self._get_collide_rects():
                        # TODO: optimize. 여기선 충돌하는지 여부만 판정해도 되는데 불필요하게 연산을 하고 있다.
                        repulse_vec = self._get_repulse_vector(vel2, rect)
                        if repulse_vec:
                            has_collision = True
                            continue
                
                if has_collision:
                    # 앗, 무조건 둘 다 움직여야 하는구나.
                    vel = Vector2(0, 0)
                    self.owner.position.x = orig_pos.x + rep_x
                    self.owner.position.y = orig_pos.y + rep_y
                else:
                    vel = vel2
        else:
            if rep_x:
                vel = Vector2(0, vel.y)
                self.owner.position.x += rep_x
            elif rep_y:
                vel = Vector2(vel.x, 0)
                self.owner.position.y += rep_y
                

            
        
        # Velocity를 업데이트해준다.
        self.velocity = vel
        # self.velocity = Vector2(0,0)

    def _get_repulse_vector(self, vel: "Vector2", target_rect: "Rect"):
        # vel이 영벡터라면 영벡터를 반환한다
        if not vel: return Vector2(0, 0)

        # 현재 시점의 히트박스 Rect
        rect_0: "Rect | None" = self.owner.get("hitbox")

        # 히트박스가 없으면 충돌 판정이 없으므로 영벡터를 반환한다
        if not rect_0: return Vector2(0, 0)

        # 이동 이후의 히트박스 Rect
        rect_1 = rect_0.move(vel * game_globals.delta_time)

        # target_rect와 충돌하지 않는다면, 반발할 필요가 없으므로 영벡터를 반환한다
        if not rect_1.colliderect(target_rect): return Vector2(0, 0)

        # 정규화된(길이가 1인) vel 벡터
        vel_norm = vel.normalize()

        # "반발 벡터"
        repulse_vec = Vector2(0, 0)

        # rect의 변과 target의 변 사이 X좌표의 차
        diff_x = None
        # 반발 벡터의 길이. 기본값은 무한대.
        repulse_x_len = float("inf")
        if vel.x < 0:
            # vel 벡터가 왼쪽으로 가고 있다
            # rect의 왼쪽 변과 target의 오른쪽 변에 대해서 X좌표의 차를 계산
            diff_x = target_rect.right - rect_1.left
        elif vel.x > 0:
            # vel 벡터가 오른쪽으로 가고 있다
            # rect의 오른쪽 변과 target의 왼쪽 변에 대해서 X좌표의 차를 계산
            diff_x = target_rect.left - rect_1.right
        
        if diff_x is not None:
            # repulse_x 벡터와 그 길이를 계산해낸다
            # repulse_x = vel_norm * (diff_x / vel_norm.x)
            repulse_x = Vector2(diff_x, vel_norm.y * diff_x / vel_norm.x)
            repulse_x_len = repulse_x.length()

        # rect의 변과 target의 변 사이 Y좌표의 차
        diff_y = None
        # 반발 벡터의 길이. 기본값은 무한대.
        repulse_y_len = float("inf")
        if vel.y > 0:
            # vel 벡터가 아래쪽으로 가고 있다
            # rect의 아래쪽 변과 target의 위쪽 변에 대해서 Y좌표의 차를 계산
            diff_y = target_rect.top - rect_1.bottom
        elif vel.y < 0:
            # vel 벡터가 위쪽으로 가고 있다
            # rect의 위쪽 변과 target의 아래쪽 변에 대해서 Y좌표의 차를 계산
            diff_y = target_rect.bottom - rect_1.top
        
        if diff_y is not None:
            # repulse_y 벡터와 그 길이를 계산해낸다
            # repulse_y = vel_norm * (diff_y / vel_norm.y)
            repulse_y = Vector2(vel_norm.x * diff_y / vel_norm.y, diff_y)
            repulse_y_len = repulse_y.length()
        
        # repulse_y와 repulse_x 중 더 크기가 작은 벡터를 찾는다
        if repulse_y_len > repulse_x_len:
            # X축 방향으로 밀어낸다
            repulse_vec = Vector2(diff_x or 0, 0)
        elif repulse_x_len > repulse_y_len:
            # Y축 방향으로 밀어낸다
            repulse_vec = Vector2(0, diff_y or 0)
        
        repulse_vec = Vector2(int(repulse_vec.x), int(repulse_vec.y))
        
        # debug.rect(rect_1, color=(0, 0, 255))
        # debug.line(rect_1.center, rect_1.center + repulse_vec, color=(255, 0, 0))
        
        return repulse_vec

    def _update_gravity(self):
        self.velocity += self._gravity * game_globals.delta_time

    def _get_collide_rects(self):
        rects = []
        # Static Tilemap에서 rect들을 구워낸다
        # TODO: owner 근처에 있는 rect들만 뽑아내도록 하기
        tile_size = self._tile_size
        for y, row in enumerate(self._static_tilemap):
            for x, tile_exists in enumerate(row):
                if tile_exists:
                    rects.append(Rect(x * tile_size, y * tile_size, tile_size, tile_size))

        for rect in rects:
            debug.rect(rect)

        return rects
