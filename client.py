import tkinter as tk
import zmq
import pystreaming as ps

# send self.hold to server using push/pull zmq sockets

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400,  height=400)

        self.label = tk.Label(self, text="last key pressed:  ", width=100)
        self.label.pack(fill="both", padx=100, pady=100)

        self.label.bind("<w>", self.on_wasd)
        self.label.bind("<KeyRelease-w>", self.on_wasd_release)
        self.label.bind("<a>", self.on_wasd)
        self.label.bind("<KeyRelease-a>", self.on_wasd_release)
        self.label.bind("<s>", self.on_wasd)
        self.label.bind("<KeyRelease-s>", self.on_wasd_release)
        self.label.bind("<d>", self.on_wasd)
        self.label.bind("<KeyRelease-d>", self.on_wasd_release)
        self.label.bind("<space>", self.on_wasd)
        self.label.bind("<KeyRelease-space>", self.on_wasd_release)
        # up arrow
        self.label.bind("<Up>", self.on_wasd)
        self.label.bind("<KeyRelease-Up>", self.on_wasd_release)
        # down arrow
        self.label.bind("<Down>", self.on_wasd)
        self.label.bind("<KeyRelease-Down>", self.on_wasd_release)
        # left arrow
        self.label.bind("<Left>", self.on_wasd)
        self.label.bind("<KeyRelease-Left>", self.on_wasd_release)
        # right arrow
        self.label.bind("<Right>", self.on_wasd)
        self.label.bind("<KeyRelease-Right>", self.on_wasd_release)

        # give keyboard focus to the label by default, and whenever
        # the user clicks on it
        self.label.focus_set()
        self.label.bind("<1>", lambda event: self.label.focus_set())


        # my shit
        self.hold = {
          "w": False,
          "a": False,
          "s": False,
          "d": False,
          "Up": False,
          "Down": False,
          "Left": False,
          "Right": False,
          "space": False
        }


        self.receiver = ps.Receiver("tcp://192.168.4.3:5556")

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect("tcp://192.168.4.3:5555")

    def on_wasd(self, event):
        self.hold[event.keysym] = True
        self.label.configure(text=f"hold: {self.hold} last key pressed: {event.keysym}")
        self.socket.send_pyobj(self.hold, flags=zmq.NOBLOCK)

    def on_wasd_release(self, event):
        self.hold[event.keysym] = False
        self.label.configure(text=f"hold: {self.hold} last key released: {event.keysym}")
        self.socket.send_pyobj(self.hold, flags=zmq.NOBLOCK)


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()