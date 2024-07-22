# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Raw Touch Values Scaled to Display Dimensions
# To be used after Calibration Simpletest

import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from circuitpython_st7796s import ST7796S
from circuitpython_xpt2046 import Touch

# Support both 8.x.x and 9.x.x. Change when 8.x.x is discontinued as a stable release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

displayio.release_displays()
# 3.5" ST7796S Display
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
DISPLAY_ROTATION = 180

# Touch calibration
TOUCH_X_MIN = 93
TOUCH_X_MAX = 1996
TOUCH_Y_MIN = 93
TOUCH_Y_MAX = 1996

tft_cs = board.D9
tft_dc = board.D10
tft_rst = board.D17
ts_cs = board.D6

spi = board.SPI()
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7796S(
    display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rotation=DISPLAY_ROTATION, portrait=False
)

# Instantiate the touchpad
touch = Touch(
    spi=spi,
    cs=ts_cs,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=DISPLAY_ROTATION,
    x_min=TOUCH_X_MIN,
    x_max=TOUCH_X_MAX,
    y_min=TOUCH_Y_MIN,
    y_max=TOUCH_Y_MAX,
)

# Quick Colors for Labels
TEXT_BLACK = 0x000000
TEXT_BLUE = 0x0000FF
TEXT_CYAN = 0x00FFFF
TEXT_GRAY = 0x8B8B8B
TEXT_GREEN = 0x00FF00
TEXT_LIGHTBLUE = 0x90C7FF
TEXT_MAGENTA = 0xFF00FF
TEXT_ORANGE = 0xFFA500
TEXT_PURPLE = 0x800080
TEXT_RED = 0xFF0000
TEXT_WHITE = 0xFFFFFF
TEXT_YELLOW = 0xFFFF00

def make_my_label(font, anchor_point, anchored_position, scale, color):
    func_label = label.Label(font)
    func_label.anchor_point = anchor_point
    func_label.anchored_position = anchored_position
    func_label.scale = scale
    func_label.color = color
    return func_label

instructions_label = make_my_label(
    terminalio.FONT, (0.5, 0.5), (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 4), 2, TEXT_WHITE
)
x_min_label = make_my_label(
    terminalio.FONT, (0.0, 0.0), (10, DISPLAY_HEIGHT/2), 2, TEXT_WHITE
)
x_max_label = make_my_label(
    terminalio.FONT, (1.0, 0.0), (DISPLAY_WIDTH - 10, DISPLAY_HEIGHT/2), 2, TEXT_WHITE
)
y_min_label = make_my_label(
    terminalio.FONT, (0.5, 0.0), (DISPLAY_WIDTH / 2, 10), 2, TEXT_WHITE
)
y_max_label = make_my_label(
    terminalio.FONT, (0.5, 1.0), (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - 10), 2, TEXT_WHITE
)

main_group = displayio.Group()
main_group.append(x_min_label)
main_group.append(x_max_label)
main_group.append(y_min_label)
main_group.append(y_max_label)
main_group.append(instructions_label)
display.root_group = main_group

                
print("Go Ahead - Touch the Screen - Make My Day!")

def map_touch_to_display(raw_x, raw_y, x_min=TOUCH_X_MIN, x_max=TOUCH_X_MAX, y_min=TOUCH_Y_MIN, y_max=TOUCH_Y_MAX):
    mapped_x = DISPLAY_WIDTH * (raw_x - x_min) // (x_max - x_min)
    mapped_y = DISPLAY_HEIGHT * (raw_y - y_min) // (y_max - y_min)
    return mapped_x, mapped_y

x = y = 0
x_min = y_min = x_max = y_max = min(DISPLAY_WIDTH, DISPLAY_HEIGHT) // 2
x_min_label.text = f"X-Min:{x_min}"
x_max_label.text = f"X-Max:{x_max}"
y_min_label.text = f"Y-Min:{y_min}"
y_max_label.text = f"Y-Max:{y_max}"
instructions_label.text = f"draw swirlies on corners"

while True:
    touch_point = touch.raw_touch()
    if touch_point is not None:
        raw_x, raw_y = touch_point
        mapped_x, mapped_y = map_touch_to_display(raw_x, raw_y)
        x_min = min(x_min, mapped_x)
        x_max = max(x_max, mapped_x)
        y_min = min(y_min, mapped_y)
        y_max = max(y_max, mapped_y)
        print(f"(({x_min}, {x_max}), ({y_min}, {y_max}))")
        x_min_label.text = f"X-Min:{x_min}"
        x_max_label.text = f"X-Max:{x_max}"
        y_min_label.text = f"Y-Min:{y_min}"
        y_max_label.text = f"Y-Max:{y_max}"
        time.sleep(0.05)
