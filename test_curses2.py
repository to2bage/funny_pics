import curses
from curses.textpad import Textbox, rectangle

def main(stdscr):
    stdscr.addstr(0, 0, "Enter IM message :(hit Ctrl-G to send)")

    editwin = curses.newwin(5, 30, 2, 1)
    rectangle(stdscr, 1, 0, 1 + 5 + 1, 1 + 30 + 1)
    stdscr.refresh()

    box = Textbox(editwin)

    box.edit()

    message = box.gather()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    main(stdscr)