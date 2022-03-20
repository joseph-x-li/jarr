from pystreaming import Receiver, buffer, display
with Receiver("tcp://localhost:5555") as stream:
    for _, data in buffer(0.5, {'video': stream.handler}):
        display(data['arr'])