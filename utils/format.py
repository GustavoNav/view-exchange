def format_number(value):
    value = float(value)

    sign = 1
    if value < 0:
        value = value * -1
        sign = -1

    if value >= 1e9:
        return f'{ sign*value / 1e9:.2f}B'
    elif value >= 1e6:
        return f'{sign*value / 1e6:.2f}M'
    elif value >= 1e3:
        return f'{sign*value / 1e3:.2f}K'
    else:
        return f'{sign*value:.2f}'