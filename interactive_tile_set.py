import os
from get_keys import getkey

class InteractiveTileSet:
  def __init__(self, x, y):
    self.x_max = x
    self.y_max = y
    self.x_cur = 0
    self.y_cur = 0

  def __display_board(self, board_iter):
    os.system('clear')
    x = 0
    y = 0
    buffer = ""
    for tile in board_iter:
      end = " "
      value = tile
      if self.y_cur == y and self.x_cur == x:
        value = "\033[92m@\033[00m"
      x += 1
      if x == self.x_max:
        x = 0
        y += 1
        end = "\n"
      buffer += "{}{}".format(value, end)
    print(buffer)

  def __display_status(self, status, cmd_options):
    print(status)
    print("")
    for cmd in cmd_options:
      print("{}: {}".format(cmd, cmd_options[cmd]))

  def loop(self, board_iter_method, board_status_method, cmd_options):
    cmds = list(cmd_options.keys())
    try:
        while True:
            self.__display_board(board_iter_method())
            self.__display_status(board_status_method(), cmd_options)
            k = getkey()
            if len(list(filter(lambda x: x == k,cmds))):
              return {"cmd": k, "x": self.x_cur, "y": self.y_cur}
            elif k == 'up' and self.y_cur > 0:
              self.y_cur -= 1
            elif k == 'down' and self.y_cur < self.y_max -1:
              self.y_cur += 1
            elif k == 'left' and self.x_cur > 0:
              self.x_cur -= 1
            elif k == 'right' and self.x_cur < self.x_max -1:
              self.x_cur += 1
            else:
                pass
    except (KeyboardInterrupt, SystemExit):
        os.system('stty sane')
        print('stopping.')
        return None




if __name__ == "__main__":
  pass
