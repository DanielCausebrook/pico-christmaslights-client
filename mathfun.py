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
