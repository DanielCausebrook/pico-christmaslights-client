from typing import Tuple


def smoothstep(edge0, edge1, x):
    if x < edge0:
        return 0

    if x >= edge1:
        return 1

    # Scale/bias into [0..1] range
    x = (x - edge0) / (edge1 - edge0)

    return x * x * (3 - 2 * x)


def rgb_to_bytes(rgb):
    (r, g, b) = rgb
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_component_to_linear(x :float) -> float:
    if x >= 0.0031308:
        return 1.055 * x ** (1.0 / 2.4) - 0.055
    else:
        return 12.92 * x


def rgb_component_from_linear(x: float) -> float:
    if x >= 0.04045:
        return ((x + 0.055)/(1 + 0.055)) ** 2.4
    else:
        return x / 12.92


def hsv_interp(color1: Tuple[float, float, float], color2: Tuple[float, float, float], amount) -> Tuple[float, float, float]:
    h1 = color1[0]
    h2 = color2[0]
    h_diff = (h2 - h1) % 1
    if h_diff > 0.5:
        h_diff -= 1
    h = (h1 + h_diff * amount) % 1

    s1 = color1[1]
    s2 = color2[1]
    s_diff = s2 - s1
    s = s1 + s_diff * amount

    v1 = color1[2]
    v2 = color2[2]
    v_diff = v2 - v2
    v = v1 + v_diff * amount

    return h, s, v

def rgb_interp(color1: Tuple[float, float, float], color2: Tuple[float, float, float], amount) -> Tuple[float, float, float]:
    r1 = rgb_component_to_linear(color1[0])
    r2 = rgb_component_to_linear(color2[0])
    r = r1 * (1-amount) + r2 * amount
    g1 = rgb_component_to_linear(color1[1])
    g2 = rgb_component_to_linear(color2[1])
    g = g1 * (1-amount) + g2 * amount
    b1 = rgb_component_to_linear(color1[2])
    b2 = rgb_component_to_linear(color2[2])
    b = b1 * (1-amount) + b2 * amount

    return rgb_component_from_linear(r), rgb_component_from_linear(g), rgb_component_from_linear(b)
