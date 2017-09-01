import Tkinter as tk

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Avanzar", 
                                command=self.create_window)
        self.button2 = tk.Button(self, text="Create new window2", 
                                command=self.create_window)
        self.button3 = tk.Button(self, text="Create new window3", 
                                command=self.create_window)
        self.button4 = tk.Button(self, text="Create new window4", 
                                command=self.create_window)
        self.button.pack(side="top")
        self.button2.pack(side="left")
        self.button3.pack(side="left")
        self.button4.pack(side="bottom")

    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
   # def modify_velocity(self,clientID,handle1,handle2,handle3,handle4,vel1)
       
# self.simxSetJointVelocity(clientID,handle1,vel1,self.sim_opmode_blocking)
 #       self.simxSetJointVelocity(clientID,handle2,vel1,self.sim_opmode_blocking)
  #      self.simxSetJointVelocity(clientID,handle3,vel1,self.sim_opmode_blocking)
   #     self.simxSetJointVelocity(clientID,handle4,vel1,self.sim_opmode_blocking)

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
