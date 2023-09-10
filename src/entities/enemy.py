import random
import pygame
from .entity import *
from .player import *
from .weapons import *
import time
import math
from pygame import Surface
from pygame.math import Vector2
from constants import *
from .character_base import CharacterBase, MoveCommand
from typing import Callable

class Enemy(CharacterBase):
    is_enemy = True

    def __init__(self):
        super().__init__()

        self._sprite_name = ""                             # sprites/enemy/{???}_1.png\
        self._max_hp = 100                          # 최대 체력
        self._damage_taking_delay = 0.5             # 데미지를 입은 뒤의 일시적 무적 시간(초)
        # self._move_speed = PLAYER_MOVE_SPEED        # 이동 속도
        # self._jump_power = 500                      # 점프 시의 최대 수직 속력 (px/s).
        # self._max_jump_time = 0.2                   # 긴 점프의 최대 유지 시간
        # self._max_damage_knockback = 3000           # 데미지 넉백의 최대 속력 (데미지 비례)
        # self._damage_knockback_y_multiplier = 1.5   # 데미지 넉백에서 Y방향 속력에 곱해질 수
        # self._x_velocity_dec_midair = 600           # 초당 x방향 속력의 감소량 (공중에 떴을 때)
        # self._x_velocity_dec_floor = 6000           # 초당 x방향 속력의 감소량 (땅 위에서)
        # self._x_velocity_dec_moving_mul = 3.0       # 이동 키를 누르고 있을 때, 초당 x방향 속력 감소량의 배수
        self._weapon = BasicGun(True)
        self._hp = self._max_hp

        self._floor_check_distance = 30  # 앞에 바닥이 있는지 확인할 때, 확인지점의 거리(px)
        self._ai_ignore_distance = 500   # 플레이어가 이 거리보다 멀다면 보지 못한다
        self._ai_minimum_distance = 200   # 플레이어가 이 거리보다 가깝다면 뒤로 뺀다
        self._floor_allow_stair = True   # 반블럭을 탈 수 있는지 여부


    def update(self):
        self._update_command()
        super().update()

    def _update_command(self):
        """현재 시점에서 AI의 MoveCommand를 업데이트한다."""
        command = self._move_command
        command.reset()

        player_dist = self._get_distance_to_player()
        to_player_axis = self._get_axis_to_player()

        # 플레이어를 찾을 수 있는가?
        if player_dist >= self._ai_ignore_distance:
            return

        # 좀 뒤로 이동해야 하는가?
        if player_dist <= self._ai_minimum_distance:
            command.move_axis = -to_player_axis

        # 이동할 방향이 안전한가?
        if not self._is_okay_to_go(command.move_axis):
            command.move_axis = 0.0

        # 이동하지 않고 있는가?
        if command.move_axis == 0:
            # 플레이어 쪽을 바라보고 총을 쏜다.
            if self.direction.x != to_player_axis:
                command.move_axis = to_player_axis * 0.05
            command.shoot = True


    def _get_distance_to_player(self):
        """플레이어와의 거리를 받아온다. 플레이어가 없다면 무한대를 반환한다."""
        from entity_manager import EntityManager
        player = EntityManager.get_player()

        if not player:
            return float("inf")
        else:
            return self.position.distance_to(player.position)

    def _get_axis_to_player(self):
        """플레이어 쪽으로 향하는 axis를 받아온다. 플레이어가 없거나 위치가 일치한다면 0을 반환한다."""
        from entity_manager import EntityManager
        player = EntityManager.get_player()

        if not player:
            return 0.0
        else:
            diff = player.position.x - self.position.x
            if diff == 0:
                return 0.0
            else:
                return math.copysign(1.0, diff)

    def _is_okay_to_go(self, axis: "float"):
        """이 앞 axis쪽 방향에 벽과 낭떠러지가 없는지 체크한다."""
        collides = self.physics.does_point_collide
        base_distance = self._floor_check_distance
        rechecks = 1

        if base_distance > 60:
            rechecks = base_distance // 60

        for divstep in range(1, rechecks+1):
            distance = base_distance // divstep
            to_wall = self.hitbox.midtop + Vector2(axis * distance, 0)
            to_floor_1 = self.hitbox.midbottom + Vector2(axis * distance, 1)
            to_floor_2 = self.hitbox.midbottom + Vector2(axis * distance, 31)
            is_okay = True
            if self._floor_allow_stair:
                is_okay = not collides(to_wall) and (collides(to_floor_1) or collides(to_floor_2))
            else:
                is_okay = not collides(to_wall) and collides(to_floor_1)
            if not is_okay:
                return False

        return True
    
    def _is_falling(self):
        return self.physics.velocity.y > 5


class BasicEnemy(Enemy):

    def __init__(self):
        super().__init__()
        self._sprite_name = "enemy/monster"
        self._weapon = PoorGun(True)


class BossPattern():
    """보스의 패턴."""
    def __init__(self,
                 update_command: "Callable[[Boss, MoveCommand], None]",
                 timeout: "float",
                 next: "int",
                 start: "Callable[[Boss], None]" = (lambda x:None),
                 surface: "None | Callable[[Boss, type[super]], Surface]" = None):
        self.next = next
        self.on_start = start
        self.on_update_command = update_command
        self.on_surface = surface
        self.time = timeout


class Boss(Enemy):
    """특수패턴을 가지는 적."""
    is_boss = True
    patterns: "list[BossPattern]" = []

    def __init__(self):
        super().__init__()
        self._pattern_idx = 9999
        self._pattern_timer = 0
        self._wait_timer = 1  # 기본적으로, 시작 후 1초간 대기한다.

        self.hurt_player_on_touch = True  # 플레이어와 닿으면 플레이어에게 데미지가 들어가는가?
        self.set_pattern(0)
    

    def update(self):
        from entity_manager import EntityManager
        super().update()

        if self.hurt_player_on_touch:
            player = EntityManager.get_player()
            if player and player.hitbox.colliderect(self.hitbox):
                player.take_damage(50, self.position)

    def _update_command(self):
        dt = game_globals.delta_time
        command = self._move_command
        command.reset()
        
        # Wait 상태인가? 그렇다면 아무것도 하지 않는다
        if self._wait_timer > 0:
            self._wait_timer = max(self._wait_timer - dt, 0)
            return
        
        # 패턴 타이머 처리
        self._pattern_timer -= dt
        if self._pattern_timer <= 0:
            self.next_pattern()

        # 현재 BossPattern에게 책임을 떠넘긴다
        self.current_pattern.on_update_command(self, command)

    def _on_die(self):
        from entity_manager import EntityManager
        super()._on_die()
        scene = EntityManager.game_scene
        if scene:
            scene.victory()

    def surface(self) -> "Surface":
        if self.current_pattern.on_surface:
            ret = self.current_pattern.on_surface(self, super)
        else:
            ret = super().surface()
        return ret


    @property
    def current_pattern(self):
        return self.patterns[self._pattern_idx]

    def next_pattern(self):
        self.set_pattern(self.current_pattern.next)

    def set_pattern(self, pattern_idx: "int"):
        assert pattern_idx < len(self.patterns)
        print(self.__class__.__name__, f"Switch Boss Pattern {self._pattern_idx} -> {pattern_idx}")

        old_pattern_index = self._pattern_idx
        if old_pattern_index != pattern_idx:
            self._pattern_idx = pattern_idx
            self._pattern_timer = self.current_pattern.time
            self.current_pattern.on_start(self)
    
    def wait_for(self, wait_time: "float"):
        self._wait_timer = wait_time


class FireEnemy(Boss):

    def pattern_move_left(self: "Boss", command: "MoveCommand"):
        if self._is_okay_to_go(-1):
            command.move_axis = -1
        elif not self._is_falling():
            self.next_pattern()
            return

    def pattern_move_right(self: "Boss", command: "MoveCommand"):
        if self._is_okay_to_go(1):
            command.move_axis = 1
        elif not self._is_falling():
            self.next_pattern()
            return

    def pattern_shoot(self: "Boss", command: "MoveCommand"):
        to_player_axis = self._get_axis_to_player()
        self.direction = Vector2(to_player_axis, 0)
        command.shoot = True

    def pattern_firedash(self: "Boss", command: "MoveCommand"):
        if not self._is_okay_to_go(self.direction.x):
            self._flip = not self._flip
        command.move_axis = self.direction.x

    def pattern_firedash_surface(self: "Boss", super: "type[super]"):
        from entity_manager import EntityManager
        time = EntityManager.game_scene and EntityManager.game_scene.scene_time or 0

        original = super().surface()
        canvas = Surface(original.get_size())

        flame = ResourceLoader.load_image_2x("item/firebullet.png")
        flame.set_alpha(int(math.sin(time * 2) * 127 + 32))
        canvas.blit(flame, (0,0))
        canvas.blit(original, (0,0))

        return canvas


    patterns = [
        # 0
        BossPattern(
            pattern_move_left,
            timeout=10,
            next=1,
        ),

        # 1
        BossPattern(
            pattern_shoot,
            timeout=10,
            next=2,
        ),

        # 2
        BossPattern(
            pattern_move_right,
            timeout=10,
            next=3,
        ),

        # 3
        BossPattern(
            pattern_shoot,
            timeout=10,
            next=0,
        ),

        # 여기서부터 특수패턴
        # 4
        BossPattern(
            pattern_firedash,
            timeout=10,
            next=4,
        ),
    ]


    def __init__(self):
        super().__init__()

        self._sprite_name = "enemy/fire"
        self._max_hp = 750
        self._damage_taking_delay = 1.0
        self._move_speed = 500
        # self._jump_power = 500
        # self._max_jump_time = 0.2
        # self._max_damage_knockback = 3000
        # self._damage_knockback_y_multiplier = 1.5
        # self._x_velocity_dec_midair = 600
        self._x_velocity_dec_floor = 1000
        self._x_velocity_dec_moving_mul = 1.0
        self._weapon = FireBossGun(True)
        self._hp = self._max_hp

        self._floor_check_distance = 120  # 앞에 바닥이 있는지 확인할 때, 확인지점의 거리(px)

    def update(self):
        super().update()
        if self.hp <= 250:
            self.set_pattern(4)

class WindEnemy(Boss):

    def pattern_move_left(self: "Boss", command: "MoveCommand"):
        if self._is_okay_to_go(-1):
            command.move_axis = -1
        elif not self._is_falling():
            self.next_pattern()
            return

    def pattern_move_right(self: "Boss", command: "MoveCommand"):
        if self._is_okay_to_go(1):
            command.move_axis = 1
        elif not self._is_falling():
            self.next_pattern()
            return

    def pattern_shoot(self: "Boss", command: "MoveCommand"):
        to_player_axis = self._get_axis_to_player()
        self.direction = Vector2(to_player_axis, 0)
        command.shoot = True

    def pattern_firedash(self: "Boss", command: "MoveCommand"):
        if not self._is_okay_to_go(self.direction.x):
            self._flip = not self._flip
        command.move_axis = self.direction.x


    patterns = [
        # 0
        BossPattern(
            pattern_move_left,
            timeout=10,
            next=1,
        ),

        # 1
        BossPattern(
            pattern_shoot,
            timeout=10,
            next=2,
        ),

        # 2
        BossPattern(
            pattern_move_right,
            timeout=10,
            next=3,
        ),

        # 3
        BossPattern(
            pattern_shoot,
            timeout=10,
            next=0,
        ),

        # 여기서부터 특수패턴
        # 4
        BossPattern(
            pattern_firedash,
            timeout=10,
            next=4,
        ),
    ]


    def __init__(self):
        super().__init__()

        self._sprite_name = "enemy/fire"
        self._max_hp = 750
        self._damage_taking_delay = 1.0
        self._move_speed = 500
        # self._jump_power = 500
        # self._max_jump_time = 0.2
        # self._max_damage_knockback = 3000
        # self._damage_knockback_y_multiplier = 1.5
        # self._x_velocity_dec_midair = 600
        self._x_velocity_dec_floor = 1000
        self._x_velocity_dec_moving_mul = 1.0
        self._weapon = FireBossGun(True)
        self._hp = self._max_hp

        self._floor_check_distance = 120  # 앞에 바닥이 있는지 확인할 때, 확인지점의 거리(px)

    def update(self):
        super().update()
        if self.hp <= 250:
            self.set_pattern(4)
