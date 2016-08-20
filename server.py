import socket
import threading
import pickle
from queue import Queue

class Server(object):
  def __init__(self, host='LOCALHOST', port=6000):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.bind((host,port))
    self.s.listen(10)
    self.connections = {}
    self.queue = Queue(maxsize=100)

  def accept_connections(self):
    while True:
      client, client_addr = self.s.accept()
      username = client.recv(1024).decode()
      self.connections[username] = client
      print('Client connection accepted from {0}, {1} on port {2}'.format(username,client_addr[0],client_addr[1]))
      print(self.connections)

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
        # user requetest list of current users
        usernames = [k for k,v in self.connections.items()]
        usernames.insert(0,'USERNAMES')
        client.sendall(pickle.dumps(usernames))

      else:
        # user sent a normal message to be broadcast
        self.queue.put((username, message))

    client.close()
    del self.connections[username]
    print('Connection closed')

  def send_messages(self):
    while True:
      if not self.queue.empty():
        m = self.queue.get()
        msg = pickle.dumps(m)
        for username, client in self.connections.items():
          client.sendall(msg)

  def start(self):
    accept = threading.Thread(target=self.accept_connections)
    send = threading.Thread(target=self.send_messages)
    accept.start()
    send.start()
    ################## TODO
    # need to do a join or something here so server can be gracefully exited
    # logging
    # username login (probably need to be up on ec2/rds for that)
    # join rooms

if __name__ == '__main__':
  server = Server()
  server.start()
