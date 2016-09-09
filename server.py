import socket
import threading
import pickle
import logging
from queue import Queue

class Server(object):
  def __init__(self, host=socket.gethostname(), port=6000):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.bind((host,port))
    self.s.listen(10)
    self.connections = {}

    # 100 message backlog
    self.queue = Queue(maxsize=100)

    # logging
    self.logger = logging.getLogger(__name__)
    logging.basicConfig(filename='bear_server.log',format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S%p')

  def accept_connections(self):
    while True:
      client, client_addr = self.s.accept()
      username = client.recv(1024).decode()
      # let other users know that someone joined
      self.queue.put(('SERVER',username+' joined'))

      self.connections[username] = client
      self.logger.info('Connection accepted from user %s, IP %s on port %s',username,client_addr[0],client_addr[1])

      # start thread for client
      thread = threading.Thread(target=self.client_handler,args=(client,username))
      # daemon so program will exit if main thread is killed
      thread.daemon = True
      thread.start()

  def client_handler(self, client, username):
    while True:
      try:
        username, message = pickle.loads(client.recv(1024))
      except EOFError: # client has disconnected
        break

      if not message: # client has disconnected
        break

      elif message == '!here':
        # user requested list of current users, dont put in queue because this only gets sent to particular user
        self.logger.info('%s requested list of usernames',username)
        usernames = [k for k,v in self.connections.items()]
        msg = ('USERNAMES',usernames)
        client.sendall(pickle.dumps(msg))

      else:
        # user sent a normal message to be broadcast
        self.logger.info('%s sent a message',username)
        self.queue.put((username, message))

    client.close()
    del self.connections[username]
    self.logger.info('%s closed connection',username)
    # let other users know someone left
    self.queue.put(('SERVER',username+' left'))

  def send_messages(self):
    while True:
      if not self.queue.empty():
        m = self.queue.get()
        msg = pickle.dumps(m)
        for client in self.connections.values():
          client.sendall(msg)
        self.logger.info('%s said %s',m[0],m[1])

  def start(self):
    accept = threading.Thread(target=self.accept_connections)
    send = threading.Thread(target=self.send_messages)
    accept.start()
    send.start()

if __name__ == '__main__':
  try:
    server = Server()
    server.start()
  except Exception as e:
    server.logger.exception(e)
