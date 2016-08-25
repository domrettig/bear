from client import Client
from secret imoprt HOST

def main():
  try:
    # client = Client(host=HOST)
    client = Client()
    client.print_help()
    client.send_message()
  except KeyboardInterrupt:
    pass