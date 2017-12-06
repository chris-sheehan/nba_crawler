
# from funcs import *

class Team(object):
  def __init__(school_name, school_abbrev):
    self.school_name = school_name
    self.school_abbrev = school_abbrev
    load_roster()
    load_games()
    pass

  def load_roster(self):
    # Load a list of player objects
    pass

  def load_games(self):
    # Load a list of game objects
    pass


