def smoothstep(edge0, edge1, x):
    if x < edge0:
        return 0

    if x >= edge1:
        return 1

    # Scale/bias into [0..1] range
    x = (x - edge0) / (edge1 - edge0)

    return x * x * (3 - 2 * x)
