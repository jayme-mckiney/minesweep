import random
from enum import Enum
import os

MaskState = Enum('MaskState', ['CLEAR', 'FLAG', 'FOG'])
GameState = Enum('GameState', ['ACTIVE', 'WIN', 'BOOM'])
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
    self.__zero()
    self.__seed()
    self.__number_board()

  def display(self):
    print("")
    if self.game_state == GameState.BOOM:
      print(' BOOM!')
    elif self.game_state == GameState.WIN:
      print(' CLEAR!')
    for y in range(self.y):
      for x in range(self.x):
        if self.board_mask[x][y] == MaskState.FOG:
          print("#", end=" ")
        elif self.board_mask[x][y] == MaskState.FLAG:
          print("!", end=" ")
        else:
          print(self.board[x][y], end=" ")
      print('\n')
    print('')

  def __game_over(self):
    self.game_state = GameState.BOOM
    self.board_mask = [[MaskState.CLEAR for y in range(self.y)] for x in range(self.x)]

  def __zero(self):
    self.board = [[0 for y in range(self.y)] for x in range(self.x)]
    self.board_mask = [[MaskState.FOG for y in range(self.y)] for x in range(self.x)]

  def __seed(self):
    for x in range(self.num_mines):
      loc = (random.randrange(self.x), random.randrange(self.y))
      while self.board[loc[0]][loc[1]] != 0:
        loc = (random.randrange(self.x), random.randrange(self.y))
      self.board[loc[0]][loc[1]] = 'X'

  def __number_board(self):
    for y in range(self.y):
      for x in range(self.x):
        if self.board[x][y] != 'X':
          self.board[x][y] = self.__count_neighbors(x,y)

  def __count_neighbors(self, x, y):
    bomb_count = 0
    if x > 0 and self.board[x-1][y] == 'X': # west
      bomb_count += 1
    if x < self.x -1 and self.board[x+1][y] == 'X': # east
      bomb_count += 1
    if y > 0 and self.board[x][y-1] == 'X': # north
      bomb_count += 1
    if y < self.y -1 and self.board[x][y+1] == 'X': # south
      bomb_count += 1
    if x > 0 and y > 0 and self.board[x-1][y-1] == 'X': # north west
      bomb_count += 1
    if x < self.x -1 and y > 0 and self.board[x+1][y-1] == 'X': # north east
      bomb_count += 1
    if x > 0 and y < self.y -1 and self.board[x-1][y+1] == 'X': # south west
      bomb_count += 1
    if x < self.x -1 and y < self.y -1 and self.board[x+1][y+1] == 'X': # south east
      bomb_count += 1
    return bomb_count

  def __colapse_adjacent_mask(self, x, y):
    self.board_mask[x][y] = MaskState.CLEAR
    if self.board[x][y] != 0:
      return
    if x > 0 and self.board_mask[x-1][y] == MaskState.FOG: # west
      self.__colapse_adjacent_mask(x-1,y)
    if x < self.x -1 and self.board_mask[x+1][y] == MaskState.FOG: # east
      self.__colapse_adjacent_mask(x+1,y)
    if y > 0 and self.board_mask[x][y-1] == MaskState.FOG: # west
      self.__colapse_adjacent_mask(x,y-1)
    if y < self.y -1 and self.board_mask[x][y+1] == MaskState.FOG: # south
      self.__colapse_adjacent_mask(x,y+1)
    if x > 0 and y > 0 and self.board_mask[x-1][y-1] == MaskState.FOG: # north west
      self.__colapse_adjacent_mask(x-1, y-1)
    if x < self.x -1 and y > 0 and self.board_mask[x+1][y-1] == MaskState.FOG: # north east
      self.__colapse_adjacent_mask(x+1, y-1)
    if x > 0 and y < self.y -1 and self.board_mask[x-1][y+1] == MaskState.FOG: # south west
      self.__colapse_adjacent_mask(x-1, y+1)
    if x < self.x -1 and y < self.y -1 and self.board_mask[x+1][y+1] == MaskState.FOG: # south east
      self.__colapse_adjacent_mask(x+1, y+1)

  def __win_check(self):
    if self.game_state == GameState.BOOM: 
      return False
    if sum([y.value for x in self.board_mask for y in x]) == self.x * self.y + self.num_mines:
      self.game_state = GameState.WIN
      return True

  def solve(self):
    for x in self.board_mask:
      for y in x:
        if y == MaskState.FOG:
          y = MaskState.CLEAR

  def check(self, x, y):
    if self.board[x][y] == 'X':
      self.__game_over()
    elif self.board[x][y] == 0:
      self.__colapse_adjacent_mask(x,y)
    else: 
      self.board_mask[x][y] = MaskState.CLEAR
    if self.flagged == self.num_mines:
      self.__win_check()

  def mark(self, x, y):
    if self.board_mask[x][y] == MaskState.FLAG:
      self.board_mask[x][y] = MaskState.FOG
      self.flagged -= 1
    elif self.board_mask[x][y] == MaskState.FOG:
      self.board_mask[x][y] = MaskState.FLAG
      self.flagged += 1
    if self.flagged == self.num_mines:
      self.__win_check()

  def iterate_tile_states(self):
    for y in range(self.y):
      for x in range(self.x):
        value = self.board[x][y]
        if self.board_mask[x][y] == MaskState.FOG:
          value = "#"
        elif self.board_mask[x][y] == MaskState.FLAG:
          value = "!"
        yield value


def simple_game_loop(options):
  board = MineBoard(options['x'], options['y'], options['bombs'])
  cmd = None
  while True:
    board.display()
    print('Pick a coordinate')
    cmd = input()
    if cmd == 'q':
      break
    elif cmd == 'r':
      board.reset()
    elif cmd[0] == 'f':
      coord = list(map(int, cmd[1:].split(',')))
      board.mark(*coord)
    else:
      coord = list(map(int, cmd.split(',')))
      board.check(*coord)


def interactive_tile_loop(options):
  from interactive_tile_set import InteractiveTileSet
  board = MineBoard(options['x'], options['y'], options['bombs'])
  tile_set = InteractiveTileSet(options['x'], options['y'])
  while True:
    output = tile_set.loop(board.iterate_tile_states, ['esc', 'q', 'r', 'f', 's', 'space', 'return', 'z'])
    if output == None or output['cmd'] == 'esc' or output['cmd'] == 'q':
      return
    elif output['cmd'] == 'r':
      board.reset()
    elif output['cmd'] == 'z':
      term_size = os.get_terminal_size()
      os.system('clear')
      print("Enter new x dimension less than {}".format(term_size.columns))
      x = int(input())
      print("Enter new y dimension less than {}".format(term_size.lines))
      y = int(input())
      print("Enter new bomb count less than {}".format(x*y*.7))
      bomb_count = int(input())
      board = MineBoard(x, y, bomb_count)
      tile_set = InteractiveTileSet(x, y)
    elif output['cmd'] == 'space' or output['cmd'] == 'return':
      board.check(output['x'], output['y'])
    elif output['cmd'] == 'f':
      board.mark(output['x'], output['y'])
    elif output['cmd'] == 's':
      board.solve()



if __name__ == '__main__':
  import sys
  options = {"x": 10, "y": 10, 'bombs': 5, "display": None}
  for arg in sys.argv[1:]:
    if arg[0:2] == "-x":
      options['x'] = int(arg[3:])
    elif arg[0:2] == "-y":
      options['y'] = int(arg[3:])
    elif arg[0:2] == '-b':
      options['bombs'] = int(arg[3:])
    elif arg[0:2] == "-d":
      options["display"] = arg[3:]
  if options['display'] == 'scroll':
    simple_game_loop(options)
  else:
    interactive_tile_loop(options)

