# 이 파일에는 각종 도움이 되는 함수를 모아놓는다.
# 주로, math 패키지에는 없는 유용한 수학 함수가 많다.

def clamp(x: float, mini: float, maxi: float) -> float:
    """실수 x가 닫힌구간 [mini, maxi] 내에 속하게 만든다.
    
    `최댓값 = (mini와 maxi 중 더 작은 값)`, `최솟값 = (mini와 maxi 중 더 큰 값)`일 때,
    `최댓값 < x`이면 `최댓값`을, `x < 최솟값`이면 `최솟값`을, 아니라면 `x`를 반환한다.
    이 함수에서 mini와 maxi의 순서는 상관이 없다."""
    if mini > maxi:
        mini, maxi = maxi, mini
    return max(mini, min(maxi, x))


def lerp(t: float, start: float, end: float) -> float:
    """선형 보간.

    좌표 (0, start)와 (1, end) 사이를 잇는 직선 y=f(t)에서, t에 대한 y값을 반환한다.

    이 함수의 정의역과 치역은 실수 전체이다. t가 구간 [0, 1]을 벗어날 수 있기 때문이다.

    @example `lerp(0.0, 0, 100) == 0`
    @example `lerp(0.5, 0, 100) == 50`
    @example `lerp(1.0, 0, 100) == 100`
    @example `lerp(2.0, 0, 100) == 200`
    """
    return (1 - t) * start + t * end

def lerpc(t: float, start: float, end: float) -> float:
    """범위를 가지는 선형 보간. 선형 보간과 같지만 `0 <= t <= 1`가 되도록 강제한다.

    이 함수의 치역은 닫힌구간 [start, end] 이다.

    @example `lerp(0.5, 0, 100) == 50`
    @example `lerp(2.0, 0, 100) == lerp(0, 100, 1.0) == 100`
    """
    return lerp(clamp(t, 0, 1), start, end)

def inv_lerp(y: float, start: float, end: float) -> float:
    """선형 보간의 역함수.

    좌표 (0, start)와 (1, end) 사이를 잇는 직선 y=f(t)에서, y 좌표가 주어졌을 때의 t값을 반환한다.

    이 함수의 정의역과 치역은 실수 전체이다. t가 구간 [0, 1]을 벗어날 수 있기 때문이다.

    @example `inv_lerp(0, 0, 100) == 0.0`
    @example `inv_lerp(50, 0, 100) == 0.5`
    @example `inv_lerp(100, 0, 100) == 1.0`
    @example `inv_lerp(200, 0, 100) == 2.0`
    """
    return (y - start) / (end - start)

def remap(t: float, range_from: "tuple[float, float]", range_to: "tuple[float, float]") -> float:
    """구간 `range_from`에 대한 실수 t를, 구간 `range_to`에 재할당한다.

    `range_from`이 `(0, 10)`이고 `range_to`가 `(-100, 100)`이라고 해 보자.
    이 때 `t`가 `5`라면, 이 `t`는 `range_from`의 50% 지점에 속한다.
    그렇다면 이 함수는 `range_to`의 50% 지점에 속하는 값인 `0`을 반환하게 된다.

    이 함수의 정의역과 치역은 실수 전체이다. t가 `range_from`의 바깥에 있을 수 있기 때문이다.
    """
    return lerp(inv_lerp(t, range_from[0], range_from[1]), range_to[0], range_to[1])

def remapc(t: float, range_from: "tuple[float, float]", range_to: "tuple[float, float]") -> float:
    """범위를 가지는 remap.

    remap()과 같지만, t가 `range_from`의 범위 내에 있도록 강제한다.
    
    이 함수의 치역은 구간 `range_to`이다.
    """
    return remap(clamp(t, *range_from), range_from, range_to)


def easein(t: float) -> float:
    """기본 Ease-in 함수. easeInQuint이다.

    무언가가 (t=0 부근) 느리게 출발해서 (t=1 부근) 빠르게 도착하는 연출을 할 때 쓰인다.

    이 함수의 치역은 닫힌구간 [0,1] 이다.
    """
    t = clamp(t, 0, 1)
    return t ** 5

def easeout(t: float) -> float:
    """기본 Ease-out 함수. easeOutQuint이다.

    무언가가 (t=0 부근) 빠르게 출발해서 (t=1 부근) 서서히 느려지는 연출을 할 때 쓰인다.

    이 함수의 치역은 닫힌구간 [0,1] 이다.
    """
    t = clamp(t, 0, 1)
    return 1 - (1-t) ** 5

def easeinout(t: float) -> float:
    """기본 Ease-in-out 함수. easeInOutQuint이다.

    무언가가 (t=0 부근) 느리게 출발해서 (t=0.5 부근) 서서히 빨라지다가
    (t=1 부근) 다시 서서히 느려지는 연출을 할 때 쓰인다.

    이 함수의 치역은 닫힌구간 [0,1] 이다.
    """
    t = clamp(t, 0, 1)
    if t < 0.5: return (16 * t ** 5)
    else: return (1 - (-2*t+2) ** 5 / 2)


def on_keyframes(t: float, frames: "dict[float, float]", easein=False, easeout=False) -> float:
    """주어진 키프레임에서 실수 t에 대응하는 값을 반환한다.

    `키프레임`은 실수 전체에서 연속인 그래프이다.
    주어진 점들을 이어서 만드는데, 작동 방식은 다음과 같다.

    1. `frames` 딕셔너리를 보고, `키프레임` 그래프에 점을 찍는다.
    2. `키프레임` 그래프의 점들을 서로 잇는다.
    3. `키프레임` 그래프의 왼쪽 끝과 오른쪽 끝에는 기울기가 0인 반직선을 잇는다.
    4. 만들어진 `키프레임` 그래프를 `y=f(x)`라 할 때, 실수 `f(t)`를 반환한다.

    `키프레임` 그래프의 점들을 잇는 규칙은 다음과 같다:
    - 기본적으로, 두 점 사이를 직선으로 잇는다.
    - 만약 `easein`이 True면, 두 점 사이를 easein()으로 잇는다.
    - 만약 `easeout`이 True면, 두 점 사이를 easeout()으로 잇는다.
    - 만약 둘 다 True면, 두 점 사이를 easeinout()으로 잇는다.

    @param frames: `키프레임`의 점들을 `{x좌표1: y좌표1, x좌표2: y좌표2}` 식으로 나타낸 딕셔너리.
    @param easein: `키프레임`의 점들을 Ease-in 방식으로 이을 지 여부.
    @param easeout: `키프레임`의 점들을 Ease-out 방식으로 이을 지 여부.
    """
    if t in frames: return frames[t]

    small_k = None
    large_k = None
    for k in sorted(frames):
        if k < t:
            small_k = k
            continue
        else:
            large_k = k
            break
    
    if small_k is None:
        return large_k in frames and frames[large_k] or 0.0
    if large_k is None:
        return small_k in frames and frames[small_k] or 0.0

    t = remap(t, (small_k, large_k), (0, 1))
    small_v = frames[small_k]
    large_v = frames[large_k]

    if easein and easeout:
        t = easeinout(t)
    elif easein:
        t = globals()["easein"](t)
    elif easeout:
        t = globals()["easeout"](t)
    return lerp(t, small_v, large_v)


if True:
    from typing import Generic, Callable, TypeVar, Any
    global classproperty
    _T = TypeVar("_T")

    class classproperty(Generic[_T]):
        def __init__(self, f: "Callable[[Any], _T]"):
            self.f = f

        def __get__(self, obj, cls) -> "_T":
            return self.f(cls)


def approach_linear(current: "float", target: "float", vel: "float"):
    """target 값과 current 값의 차를 vel만큼 줄인 값을 반환한다.
    
    @example `approach_linear(105, 0, 50) == 55`
    @example `approach_linear(55, 0, 50) == 5`
    @example `approach_linear(5, 0, 50) == 0`
    """
    assert vel >= 0
    if current > target:
        return max(current - vel, target)
    elif current < target:
        return min(current + vel, target)
    else:
        return target


assert approach_linear(100, 50, 1000) == 50
assert approach_linear(100, 50, 10) == 90
assert approach_linear(-100, 50, 10) == -90
assert approach_linear(-100, 50, 1000) == 50


def approach_easeout(current: "float", target: "float", vel: "float", epsilon = 0.1):
    """approach_linear와 비슷하지만 가까워질수록 vel이 줄어든다."""
    dist = abs(current - target)
    if dist < epsilon:
        return target

    if dist < vel * 2:
        vel *= remap(dist, (0, vel * 2), (0, 1))**2
    
    return approach_linear(current, target, vel)
