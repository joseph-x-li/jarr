from pystreaming import Receiver, buffer, display
import numpy as np

def main():
  with Receiver("tcp://192.168.4.3:5556") as stream:
    def videohandler():
      return stream.handler(timeout=60_000)

    for _, data in buffer(0.5, {'video': videohandler}):
        display(np.fliplr(np.flipud(data['arr'])), BGR=False)

if __name__ == "__main__":
  main()