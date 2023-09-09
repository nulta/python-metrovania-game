import pygame
from .entity import *
from .player import *
from .weapons import *
from pygame import Surface
from pygame.math import Vector2
from constants import *

class MoveCommand():
    """CharacterBase가 매 틱 처리할 이동 명령."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.move_axis = 0.0  # 이동축. -1: 왼쪽, 0:정지, 1: 오른쪽.
        self.jump = False   # 점프
        self.shoot = False  # 총 발사

class CharacterBase(Entity):
    """Player와 Enemy의 기반 클래스."""

    def __init__(self):
        super().__init__()
        self.physics = PhysicsComponent(self)

        self._sprite_name = ""                      # 그릴 스프라이트의 기본 이름
        self._max_hp = 100                          # 최대 체력
        self._damage_taking_delay = 1.0             # 데미지를 입은 뒤의 일시적 무적 시간(초)
        self._move_speed = PLAYER_MOVE_SPEED        # 이동 속도
        self._jump_power = 500                      # 점프 시의 최대 수직 속력 (px/s).
        self._max_jump_time = 0.2                   # 긴 점프의 최대 유지 시간
        self._max_damage_knockback = 3000           # 데미지 넉백의 최대 속력 (데미지 비례)
        self._damage_knockback_y_multiplier = 1.5   # 데미지 넉백에서 Y방향 속력에 곱해질 수
        self._x_velocity_dec_midair = 600           # 초당 x방향 속력의 감소량 (공중에 떴을 때)
        self._x_velocity_dec_floor = 6000           # 초당 x방향 속력의 감소량 (땅 위에서)
        self._x_velocity_dec_moving_mul = 3.0       # 이동 키를 누르고 있을 때, 초당 x방향 속력 감소량의 배수
        self._weapon: "Weapon | None" = None

        self._hp = self._max_hp
        self._pivot = Vector2(30, 56)
        self._walking_timer = 0.0
        self._flip = False
        self._jump_timer = 0
        self._jumping = False
        self._invincible_timer = 0  # 무적 타이머. 0보다 큰 값이면 무적 상태임을 뜻한다.
        self._shoot_timer = 0       # 무기 발사 타이머. 발사 키를 "꾹 누르고 있을 때의" 연사 처리용.
        self._move_command = MoveCommand()


    @property
    def hitbox(self):
        offset = pygame.Vector2(-20, -56)
        size = pygame.Vector2(40, 56)
        return pygame.Rect(self.position + offset, size)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, round(value))
        self._hp = util.clamp(value, 0, 200)
        if self.dead:
            self._on_die()

    @property
    def direction(self):
        return Vector2(1 if self._flip else -1, 0)
    
    @property
    def dead(self):
        return self.hp <= 0


    def update_movement(self):
        """캐릭터 이동 및 입력을 처리한다."""
        dt = game_globals.delta_time
        command = self._move_command

        # 좌우 이동 처리용 변수
        axis = command.move_axis
        vel_x = self.physics.velocity.x

        # X 속도의 변화량
        x_dec = self._x_velocity_dec_midair * dt
        if self.is_on_floor():
            x_dec = self._x_velocity_dec_floor * dt
        if axis:
            x_dec *= self._x_velocity_dec_moving_mul

        # 목표 X 속도
        desired_vel_x = self._move_speed * axis
        self.physics.velocity.x = util.approach_easeout(vel_x, desired_vel_x, x_dec)

        # 애니메이션 및 상태 처리
        if axis:
            self._walking_timer += dt
            if axis > 0:
                self._flip = True
            else:
                self._flip = False
        else:
            self._walking_timer = 0

        # 점프 처리
        if command.jump:
            self.jump(True)
        else:
            self._jumping = False
        
        # 무기 처리
        if self._weapon:
            direction = self.direction
            self._weapon.position = Vector2(self.hitbox.center) + direction * 20
            self._weapon.direction = direction

            if command.shoot:
                self._shoot_timer -= dt
                if self._shoot_timer < 0:
                    self._shoot_timer = self._weapon.shoot_cooldown + 0.01
                    self._weapon.shoot()
            else:
                self._shoot_timer = 0


    def jump(self, long_jump = False):
        """위로 점프한다. 도약했다면 True를 반환한다."""
        dt = game_globals.delta_time

        if self.is_on_floor() and not self._jumping:
            # Audio.play("jump_1")
            self._jumping = True
            self._jump_timer = 0
            self.physics.velocity.y = min(self.physics.velocity.y, -self._jump_power)
            return True
        elif long_jump and self._jumping:
            self._jump_timer += dt
            if self._jump_timer < self._max_jump_time:
                self.physics.velocity.y = min(self.physics.velocity.y, -self._jump_power)

        return False


    def update(self):
        super().update()
        dt = game_globals.delta_time

        # 이동 처리
        self.update_movement()

        # 물리 처리
        self.physics.update()
        
        # 무적 상태 처리
        self._invincible_timer = max(0, self._invincible_timer - dt)

    def surface(self):
        if not self._sprite_name:
            surface = Surface((60, 60))
            surface.fill((255, 0, 255))
            return surface

        from scene_manager import SceneManager
        scene_time = SceneManager.scene_time

        image_offset_y = 0
        image_flipped = self._flip

        # 가져와야 할 이미지의 이름을 조립한다
        chip_idx = int((self._walking_timer // 0.25 + 1) % 4)
        if chip_idx == 3: chip_idx = 1
        if self._walking_timer and chip_idx == 1: image_offset_y = 2

        image_path = f"{self._sprite_name}_{chip_idx}.png"

        surface = ResourceLoader.load_image_2x(image_path).copy()
        surface = pygame.transform.flip(surface, image_flipped, False)
        surface.scroll(0, image_offset_y)

        # 무적상태일 경우 깜빡임
        if self._invincible_timer:
            is_in_blink = scene_time * 10 % 2 > 1
            if is_in_blink:
                # 반투명 상태로 만든다.
                surface.set_alpha(128)

        return surface


    def take_damage(self, damage: "int", origin: "Vector2 | None" = None) -> bool:
        """지정된 양만큼의 데미지를 입는다. 데미지를 입었다면 True를 반환한다."""

        # 무적 상태일 때는 데미지를 받지 않는다.
        if self._invincible_timer:
            return False

        # 데미지를 입은 뒤에는 일시적으로 무적이 된다.
        self._invincible_timer = self._damage_taking_delay
        self.hp -= damage
        # Audio.play("hurt_2")

        # origin이 있다면 넉백을 받는다.
        if origin:
            knockback_direction = (self.position - origin).normalize()
            knockback_power = self._max_damage_knockback * util.clamp(damage / self._max_hp, 0, 5)
            knockback = knockback_direction * knockback_power
            knockback.y *= self._damage_knockback_y_multiplier
            self.physics.velocity += knockback
        
        return True


    def _on_die(self):
        """캐릭터의 HP가 0이 되었을 때 호출된다."""
        self.remove()

    def is_on_floor(self):
        """바닥에 발을 딛고 있는가?"""
        # 벽에 닿아있을 때의 True 판정을 방지하기 위해서, 히트박스보다 한 픽셀씩 좁게 판정한다
        check_points = [
            Vector2(self.hitbox.bottomleft)  + Vector2(+1, +1),
            Vector2(self.hitbox.midbottom)   + Vector2( 0, +1),
            Vector2(self.hitbox.bottomright) + Vector2(-1, +1),
        ]
        return any(map(self.physics.does_point_collide, check_points))
