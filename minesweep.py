import random
from enum import Enum
import os
from board import MatrixBoard

MaskState = Enum('MaskState', ['CLEAR', 'FLAG', 'FOG'])
GameState = Enum('GameState', ['ACTIVE', 'WIN', 'BOOM'])
ColorCode = Enum('ColorCode', ['WHITE', 'GREEN', 'YELLOW', 'ORANGE'])
class MineBoard:
  def __init__(self, x = 4, y = 4, mines=3):
    self.x = x
    self.y = y
    self.num_mines = mines
    self.flagged = 0
    self.board = None
    self.board_mask = None
    self.game_state = GameState.ACTIVE
    self.game_over = False
    self.win_state = False
    self.reset()

  def reset(self):
    self.game_state = GameState.ACTIVE
    self.flagged = 0
    self.__zero()
    self.__seed()
    self.__number_board()

  def __game_over(self):
    self.game_state = GameState.BOOM
    for c in self.board_mask.index_iter():
      if self.board_mask.get(*c) == MaskState.FOG:
        self.board_mask.set(*c, MaskState.CLEAR)

  def __zero(self):
    self.board = MatrixBoard(self.x, self.y, 0)
    self.board_mask = MatrixBoard(self.x, self.y, MaskState.FOG)

  def __seed(self):
    for x in range(self.num_mines):
      loc = (random.randrange(self.x), random.randrange(self.y))
      while self.board.get(*loc) != 0:
        loc = (random.randrange(self.x), random.randrange(self.y))
      self.board.set(*loc, 'X')

  def __number_board(self):
    for y in range(self.y):
      for x in range(self.x):
        if self.board.get(x, y) != 'X':
          self.board.set(x, y, self.__count_neighbors(x,y))

  def __count_neighbors(self, x, y):
    bomb_count = 0
    if self.board.get_upper_left(x,y) == 'X':
      bomb_count += 1
    if self.board.get_upper(x,y) == 'X':
      bomb_count += 1
    if self.board.get_upper_right(x,y) == 'X':
      bomb_count += 1
    if self.board.get_right(x,y) == 'X':
      bomb_count += 1
    if self.board.get_lower_right(x,y) == 'X':
      bomb_count += 1
    if self.board.get_lower(x,y) == 'X':
      bomb_count += 1
    if self.board.get_lower_left(x,y) == 'X':
      bomb_count += 1
    if self.board.get_left(x,y) == 'X':
      bomb_count += 1
    return bomb_count

  def __colapse_adjacent_mask(self, x, y):
    self.board_mask.set(x, y, MaskState.CLEAR)
    if self.board.get(x,y) != 0:
      return
    if self.board_mask.get_upper_left(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_upper_left_coords(x,y))
    if self.board_mask.get_upper(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_upper_coords(x,y))
    if self.board_mask.get_upper_right(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_upper_right_coords(x,y))
    if self.board_mask.get_right(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_upper_right_coords(x,y))
    if self.board_mask.get_lower_right(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_lower_right_coords(x,y))
    if self.board_mask.get_lower(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_lower_coords(x,y))
    if self.board_mask.get_lower_left(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_lower_left_coords(x,y))
    if self.board_mask.get_left(x,y) == MaskState.FOG:
      self.__colapse_adjacent_mask(*self.board_mask.get_left_coords(x,y))

  def __win_check(self):
    if self.game_state == GameState.BOOM: 
      return False
    if sum([x.value for x in self.board_mask.iter()]) == self.x * self.y + self.num_mines:
      self.game_state = GameState.WIN
      return True

  def solve(self):
    for c in self.board_mask.index_iter():
      if self.board_mask.get(*c) == MaskState.FOG:
        self.board_mask.set(*c, MaskState.CLEAR)
        if self.board.get(*c) == 'X':
          self.game_state = GameState.BOOM
    self.__win_check()

  def status_string(self):
    state = self.game_state.name
    if self.game_state == GameState.ACTIVE:
      state += " {}/{}".format(self.flagged, self.num_mines)
    return state

  def check(self, x, y):
    if self.board_mask.get(x,y) == MaskState.FLAG:
      return
    if self.board.get(x,y) == 'X':
      self.__game_over()
    elif self.board.get(x,y) == 0:
      self.__colapse_adjacent_mask(x,y)
    else: 
      self.board_mask.set(x,y, MaskState.CLEAR)
    if self.flagged == self.num_mines:
      self.__win_check()

  def mark(self, x, y):
    if self.board_mask.get(x,y) == MaskState.FLAG:
      self.board_mask.set(x,y, MaskState.FOG)
      self.flagged -= 1
    elif self.board_mask.get(x,y) == MaskState.FOG:
      self.board_mask.set(x,y, MaskState.FLAG)
      self.flagged += 1
    if self.flagged == self.num_mines:
      self.__win_check()

  def iterate_tile_states(self):
    for c in self.board.index_iter():
        value = self.board.get(*c)
        if self.board_mask.get(*c) == MaskState.FOG:
          value = "~"
        elif self.board_mask.get(*c) == MaskState.FLAG:
          value = "!"
        yield value

def interactive_tile_loop(options):
  from interactive_tile_set import InteractiveTileSet
  board = MineBoard(options['x'], options['y'], options['bombs'])
  tile_set = InteractiveTileSet(options['x'], options['y'])
  cmd_options = {
  'esc': 'Exit',
  'q': 'Exit',
  'r': 'Reset',
  'f': 'Flag',
  's': 'Reveal all unflagged',
  'space': 'Check tile',
  'return': 'Check tile',
  'z': 'Resize custom',
  'b': 'Begginer mode',
  'm': 'Medium mode',
  'e': 'Expert mode'
  }
  while True:
    output = tile_set.loop(board.iterate_tile_states, board.status_string, cmd_options)
    if output == None or output['cmd'] == 'esc' or output['cmd'] == 'q':
      return
    elif output['cmd'] == 'r':
      board.reset()
    elif output['cmd'] == 'z':
      term_size = os.get_terminal_size()
      os.system('clear')
      print("Enter new x dimension less than {}".format(int(term_size.columns /2)))
      x = int(input())
      print("Enter new y dimension less than {}".format(int(term_size.lines / 2)))
      y = int(input())
      print("Enter new bomb count less than {}".format(int(x*y*.7)))
      bomb_count = int(input())
      board = MineBoard(x, y, bomb_count)
      tile_set = InteractiveTileSet(x, y)
    elif output['cmd'] == 'space' or output['cmd'] == 'return':
      board.check(output['x'], output['y'])
    elif output['cmd'] == 'f':
      board.mark(output['x'], output['y'])
    elif output['cmd'] == 's':
      board.solve()
    elif output['cmd'] == 'b':
      board = MineBoard(9, 9, 10)
      tile_set = InteractiveTileSet(9, 9)
    elif output['cmd'] == 'm':
      board = MineBoard(16, 16, 40)
      tile_set = InteractiveTileSet(16, 16)
    elif output['cmd'] == 'e':
      board = MineBoard(30, 16, 99)
      tile_set = InteractiveTileSet(30, 16)



if __name__ == '__main__':
  import sys
  options = {"x": 9, "y": 9, 'bombs': 10, "display": None}
  for arg in sys.argv[1:]:
    if arg[0:2] == "-x":
      options['x'] = int(arg[3:])
    elif arg[0:2] == "-y":
      options['y'] = int(arg[3:])
    elif arg[0:2] == '-b':
      options['bombs'] = int(arg[3:])

  interactive_tile_loop(options)

