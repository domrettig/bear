from client import Client
from secret import HOST

def main(local=False):
  try:
    if local:
      client = Client()
    else:
      client = Client(host=HOST)
    client.print_help()
    client.send_message()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()