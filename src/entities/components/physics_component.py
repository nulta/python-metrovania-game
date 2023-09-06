from pygame import Vector2, Rect
from typing import TYPE_CHECKING, Sequence
import game_globals
import debug
from constants import TILE_SIZE, DEBUG_DRAW_HITBOX
from math import isnan, copysign

if TYPE_CHECKING:
    from entity import Entity

class PhysicsComponent:
    def __init__(self, owner: "Entity"):
        self._owner = owner
        self._velocity = Vector2(0, 0)   # pixels per second
        self._gravity = Vector2(0, 1200)  # pixels per second

        self._collision_map = [[]]
        self._tile_size = TILE_SIZE

        if self.owner._level:
            self._collision_map = self.owner._level.get_collision_map()
        else:
            print("PhysicsComponent: Failed to get collision map - self.owner._level is None!")

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
        self._velocity = Vector2(round(val.x), round(val.y))


    def update(self):
        self._update_gravity()
        self._update_position()
        self._check_stuck()

        if DEBUG_DRAW_HITBOX:
            for rect in self._get_collide_rects():
                rect = rect.move(-game_globals.camera_offset)
                debug.draw_rect(rect, color=(0, 255, 128))

    def does_point_collide(self, point: "Vector2"):
        """주어진 좌표점이 맵과 겹치는지 여부를 알아낸다.
        
        주의: 이 엔티티의 근처에 있는 (반경 3타일 가량) 경우에만 제대로 판단할 수 있다.
        엔티티와 멀리 떨어져 있는 좌표점에 대해서 판단할 경우에는 항상 False를 반환한다.
        """
        assert self.owner.position.distance_to(point) <= (TILE_SIZE * 3)
        if DEBUG_DRAW_HITBOX:
            debug.draw_point(point, color=(255,0,0))
        return any(map(lambda rect: rect.collidepoint(point), self._get_collide_rects()))

    def _update_position(self):
        if not self.velocity:
            return

        old_pos = self.owner.position
        new_pos = old_pos + (self.velocity * game_globals.delta_time)
        new_pos.x = round(new_pos.x)
        new_pos.y = round(new_pos.y)
        
        old_hitbox: "Rect | None" = self.owner.get("hitbox")
        if not old_hitbox:
            return
        new_hitbox = old_hitbox.move(new_pos - old_pos)

        possible_colliding_rects = self._get_collide_rects()
        lose_x_vel = False  # X방향 속도를 잃어야 하는가? (즉, X방향으로 벽에 박았는가?)
        lose_y_vel = False  # Y방향 속도를 잃어야 하는가? (즉, Y방향으로 벽에 박았는가?)
        loops = 0
        while True:
            collided = False

            # Discrete 방식으로 충돌하는지 판정
            real_colliding_rects: "list[Rect]" = []
            for rect in possible_colliding_rects:
                if not new_hitbox.colliderect(rect):
                    continue
                real_colliding_rects.append(rect)
            
            # 충돌하는 것으로 판정된 Rect들을 거리에 따라 정렬
            real_colliding_rects.sort(key=lambda rect: Vector2(rect.center).distance_squared_to(new_hitbox.center))

            for rect in real_colliding_rects:
                # 현재 상태에서 충돌하는지 판별
                # new_pos는 변경되었을 수도 있다.
                delta_pos = new_pos - old_pos
                new_hitbox = old_hitbox.move(delta_pos)
                if not new_hitbox.colliderect(rect):
                    continue
                if not delta_pos:
                    continue

                # 충돌한다면, 충돌 해결
                collided = True
                infinite = float("inf")  # 무한대

                # X 방향으로 옮겨서 충돌을 해결할 때, 옮겨야 할 픽셀 수
                diff_x = infinite
                if 0 < delta_pos.x:    # X-->
                    diff_x = round(new_hitbox.right - rect.left)
                elif delta_pos.x < 0:  # <--X
                    diff_x = round(rect.right - new_hitbox.left)

                assert diff_x >= 0

                # Y 방향으로 옮겨서 충돌을 해결할 때, 옮겨야 할 픽셀 수
                diff_y = infinite
                if 0 < delta_pos.y:    # Y going down
                    diff_y = round(new_hitbox.bottom - rect.top)
                elif delta_pos.y < 0:  # Y going up
                    diff_y = round(rect.bottom - new_hitbox.top)
                
                assert diff_y >= 0
                assert min(diff_x, diff_y) != infinite

                # 벡터의 내적
                dot_x = abs(delta_pos.dot((diff_x, 0)))
                dot_y = abs(delta_pos.dot((0, diff_y)))

                if isnan(dot_x): dot_x = infinite
                if isnan(dot_y): dot_y = infinite

                assert not (dot_x == infinite and dot_y == infinite)

                # 더 적게 밀어도 되는 쪽으로 민다.
                if dot_x < dot_y:
                    # X쪽으로 반작용을 가한다.
                    assert delta_pos.x
                    lose_x_vel = True
                    diff_x = min(abs(diff_x), abs(delta_pos.x))  # 작용력보다 수직 항력이 크면 안 된다
                    new_pos.x -= copysign(diff_x, delta_pos.x)
                else:
                    # Y쪽으로 반작용을 가한다.
                    lose_y_vel = True
                    diff_y = min(abs(diff_y), abs(delta_pos.y))  # 작용력보다 수직 항력이 더 크면 안 된다
                    new_pos.y -= copysign(diff_y, delta_pos.y)
            
            if not collided:
                break

            loops += 1
            if loops >= 5:
                print("PhysicsComponent: Failed to resolve collisions in 5 times! possible phys error?")
                break
            
        self.owner.position = new_pos
        if lose_x_vel:
            self.velocity.x = 0
        if lose_y_vel:
            self.velocity.y = 0
    
    def _check_stuck(self):
        """속도가 0이고 벽에 끼었을 경우, 바깥으로 나간다."""
        if self.velocity:
            return

        for rect in self._get_collide_rects():
            hitbox: "Rect | None" = self.owner.get("hitbox")
            if not hitbox:
                return
            if rect.colliderect(hitbox):
                # 끼었다!
                self.owner.position += Vector2(0, -60)

    def _check_trigger(self):
        """나와 겹치는 트리거가 있는지 확인하고, 있다면 발동시킨다."""
        pass

    def _update_gravity(self):
        self.velocity += self._gravity * game_globals.delta_time

    def _get_collide_rects(self):
        rects: "list[Rect]" = []

        # Static Tilemap에서 근처에 있는 rect들을 뽑아온다
        for y, row in enumerate(self._collision_map):
            for x, rect in enumerate(row):
                if rect and self._is_nearby_tile(x, y):
                    rects.append(rect)

        return rects

    def _is_nearby_tile(self, tile_x, tile_y):
        my_pos = self.owner.position
        tile_size = self._tile_size
        distance_max_sqr = (tile_size * 3) ** 2
        tile_pos = (tile_x * tile_size + (tile_size / 2), tile_y * tile_size + (tile_size / 2))
        distance_sqr = my_pos.distance_squared_to(tile_pos)
        if distance_sqr <= distance_max_sqr:
            return True
        else:
            return False