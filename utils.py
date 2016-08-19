import sys,struct,fcntl,termios,readline
from colors import colors

CLEAR_LINE = '\x1b[2K'
MOVE_UP = '\x1b[1A'
MOVE_TO_START = '\x1b[0G'

def bprint(msg):
  sys.stdout.write(CLEAR_LINE)
  sys.stdout.write(MOVE_TO_START)
  print(str(msg))
  sys.stdout.write('bear>> ' + readline.get_line_buffer())
  sys.stdout.flush() # otherwise text won't show until key is pressed

def msg_print(username, msg):
  message = colors.OKBLUE + username + ': ' + colors.ENDC + msg
  bprint(message)