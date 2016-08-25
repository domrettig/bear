from client import Client
from secret import HOST

def main():
  try:
    client = Client(host=HOST)
    client.print_help()
    client.send_message()
  except KeyboardInterrupt:
    pass