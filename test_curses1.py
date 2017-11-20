import curses
import time

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

# 打开新的窗口
begin_x = 20
begin_y = 7
height = 5
width = 40
win = curses.newwin(height, width, begin_y, begin_x)
li = [curses.A_BLINK, curses.A_BOLD, curses.A_DIM, curses.A_REVERSE, curses.A_STANDOUT, curses.A_UNDERLINE]
for index, item in enumerate(li):
    stdscr.addstr(0, 0, "Current mode: Typing mode", item)
    stdscr.refresh()
    time.sleep(1)
    win.refresh()
# stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_BLINK)
stdscr.refresh()
win.refresh()
