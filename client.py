import socket
import threading
import pickle
from utils.prints import *
from utils.colors import colors

try:
  from secret import KEY, IV
  from Crypto.Cipher import AES
except ImportError:
  pass

class Client(object):
  def __init__(self, host=socket.gethostname(), port=6000, encryption=False):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host,port))
    self.username = input('Username: ').strip()
    self.sock.sendall(self.username.encode())
    self.encryption = encryption

    self.listener = threading.Thread(target=self.listener,name='listener')
    # make listener thread a daemon so client can be gracefully exited
    self.listener.daemon = True
    self.listener.start()

  def listener(self):
    while True:
      m = self.sock.recv(1024)

      if not m:
        break # connection has been closed on server side

      m = pickle.loads(m)

      if m[0] == 'USERNAMES':
        # user requested a list of usernames
        # sent from server in form (USERNAMES,['USER1','USER2',....,'USERX'])
        usernames = ', '.join(m[1])
        msg_print('USERS HERE', usernames)
      else:
        # user sent a regular message
        # messages from server aren't encrypted
        if self.encryption and m[0] != 'SERVER':
          m = (m[0],self.decrypt(m[1]).decode().strip())
        msg_print(*m)

  def encrypt(self,m):
    obj = AES.new(KEY, AES.MODE_CBC, IV)
    return obj.encrypt(m)

  def decrypt(self,m):
    obj = AES.new(KEY, AES.MODE_CBC, IV)
    return obj.decrypt(m)

  def print_help(self):
    menu = colors.OKBLUE + 'HELP MENU\n' + colors.ENDC + \
          colors.OKGREEN + '!exit' + colors.ENDC + ' -- quit program\n' + \
          colors.OKGREEN + '!here' + colors.ENDC + ' -- list logged in users'
    print(CLEAR_LINE + MOVE_UP)
    print(menu)

  def parse_command(self, msg):
    if msg[0] == 'help':
      self.print_help()

    elif msg[0] == 'file':
      print(CLEAR_LINE + MOVE_UP)
      print('Filesharing coming soon.')

    elif msg[0] == 'files':
      print(CLEAR_LINE + MOVE_UP)
      print('Filesharing coming soon.')

    elif msg[0] == 'here':
      # need to ask the server for a list of users in chat room
      m = pickle.dumps((self.username,'!here'))
      self.sock.sendall(m)

    else:
      print(CLEAR_LINE + MOVE_UP)
      print('Not a recognized command. !help for list of available commands')

  def send_message(self):
    while True:
      message = input('bear>> ')
      # delete the previous input prompt/message
      print(MOVE_UP + CLEAR_LINE + MOVE_UP)

      if message == '!exit':
        self.sock.close()
        return
      # commands start with !
      elif message[0] == '!':
        self.parse_command(message[1:].split(' '))
      else:
        if self.encryption:
          message = self.encrypt(message.strip().rjust(256))

        # use pickle to preserve tuple structure
        msg = pickle.dumps((self.username,message.strip()))
        self.sock.sendall(msg)
