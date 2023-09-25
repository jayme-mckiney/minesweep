
class MatrixBoard:
  def __init__(self, x, y, initial_val):
    self.x = x
    self.y = y
    self.board = None
    self.set_all(initial_val)

  def set_all(self, val):
    self.board = [[val for y in range(self.x)] for x in range(self.y)]

  def set(self, x, y, val):
    if self.x > x and self.y > y:
      self.board[x][y] = val

  def get(self, x, y):
    if self.x > x and self.y > y:
      return self.board[x][y]

  def iter(self):
    for y in range(self.y):
      for x in range(self.x):
        yield self.board[x][y]
        
  def index_iter(self):
    for y in range(self.y):
      for x in range(self.x):
        yield (x,y)

  def get_upper_left_coords(self, x, y):
    if x > 0 and y > 0:
      return (x-1, y-1)
    else:
      return None

  def get_upper_coords(self, x, y):
    if y > 0:
      return (x, y-1)
    else:
      return None

  def get_upper_right_coords(self, x, y):
    if x < self.x -1 and y > 0:
      return (x+1, y-1)
    else:
      return None

  def get_right_coords(self, x, y):
    if x > 0:
      return (x-1, y)
    else:
      return None

  def get_lower_right_coords(self, x, y):
    if x < self.x -1 and y < self.y -1:
      return (x+1, y+1)
    else:
      return None

  def get_lower_coords(self, x, y):
    if y < self.y -1:
      return (x, y+1)
    else:
      return None

  def get_lower_left_coords(self, x, y):
    if x > 0 and y < self.y -1:
      return (x-1, y+1)
    else:
      return None

  def get_left_coords(self, x, y):
    if x > 0:
      return (x-1,y)
    else:
      return None

  def get_upper_left(self, x, y):
    if x > 0 and y > 0:
      return self.board[x-1][y-1]
    else:
      return None

  def get_upper(self, x, y):
    if y > 0:
      return self.board[x][y-1]
    else:
      return None

  def get_upper_right(self, x, y):
    if x < self.x -1 and y > 0:
      return self.board[x+1][y-1]
    else:
      return None

  def get_right(self, x, y):
    if x > 0:
      return self.board[x-1][y]
    else:
      return None

  def get_lower_right(self, x, y):
    if x < self.x -1 and y < self.y -1:
      return self.board[x+1][y+1]
    else:
      return None

  def get_lower(self, x, y):
    if y < self.y -1:
      return self.board[x][y+1]
    else:
      return None

  def get_lower_left(self, x, y):
    if x > 0 and y < self.y -1:
      return self.board[x-1][y+1]
    else:
      return None

  def get_left(self, x, y):
    if x > 0:
      return self.board[x-1][y]
    else:
      return None
