def reduce(in_value: int, maxval: int = 255):
    """Limits a val to a range of 0 to 255"""
    return max(0, min(in_value, maxval))


def rgb_to_hex(rgb: tuple):
    """Converts an rgb tuple to hex"""
    return "#{0:02x}{1:02x}{2:02x}".format(
        reduce(rgb[0]), reduce(rgb[1]), reduce(rgb[2])
    )


def rgba_to_hex(rgba: tuple):
    """Converts an rgba tuple to rgba hex"""
    return "#{0:02x}{1:02x}{2:02x}{3:02x}".format(
        reduce(rgba[0]), reduce(rgba[1]), reduce(rgba[2]), reduce(rgba[3])
    )


def hex_to_rgb(hex: str):
    """Converts hex to rgb tuple"""
    return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]


def hex_to_rgba(hex: str):
    """Tries to convert rgba hex to rgba, on failure converts rgb hex to rgb and sets a full opacity"""
    try:
        return [int(hex[i : i + 2], 16) for i in range(1, 8, 2)]
    except ValueError as e:
        rgba = hex_to_rgb(hex)
        rgba.append(255)
        return rgba


def get_gradient(steps: int):
    """Generates a gradient with a given number of steps"""
    return [
        rgb_to_hex(v) for v in reversed(linear_gradient("#FFFFFF", "#000000", steps))
    ]


def rgb_to_scalar(rgb: tuple):
    """Converts an rgb itterable to scalar list"""
    return [int(x / 255.0) for x in rgb]


def scalar_to_rgb(rgb: tuple):
    """Converts rgb scalar to rgb list"""
    return [int(x * 255.0) for x in rgb]


def linear_gradient(
    start_hex: str = "#000000", finish_hex: str = "#FFFFFF", n: int = 10
):
    """Generates a linear gradient between two colors, accepts html hex or rgb formats"""
    s = hex_to_rgb(start_hex) if isinstance(start_hex, str) else start_hex
    f = hex_to_rgb(finish_hex) if isinstance(finish_hex, str) else finish_hex
    rgb = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        rgb.append([int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) for j in range(3)])
    return rgb


def get_rainbow(steps: int):
    """Generates a rainbow with a given number of steps. Steps must be divisible by 4)"""
    assert steps % 4 == 0, "Steps should be divisible by 4"
    rainbow = []
    step = int(steps / 4)
    rainbow.extend(linear_gradient("#FF0000", "#FFFF00", step))
    rainbow.extend(linear_gradient("#7FFF00", "#00FF7F", step))
    rainbow.extend(linear_gradient("#00FFF", "#0000FF", step))
    rainbow.extend(linear_gradient("#7F00FF", "#FF007f", step))
    return [rgb_to_hex(v) for v in reversed(rainbow)]


COLOR_FUNCTIONS = [
    reduce,
    rgb_to_hex,
    rgba_to_hex,
    hex_to_rgb,
    hex_to_rgba,
    get_gradient,
    rgb_to_scalar,
    scalar_to_rgb,
    linear_gradient,
    get_rainbow,
]
