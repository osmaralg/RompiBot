from Tkinter import *

root = Tk()

def task():
    print("hello")
    root.after(200, task)  # reschedule event in 2 seconds

root.after(200, task)
root.mainloop()



def after(self, ms, func=None, *args):
    """Call function once after given time.

    MS specifies the time in milliseconds. FUNC gives the
    function which shall be called. Additional parameters
    are given as parameters to the function call.  Return
    identifier to cancel scheduling with after_cancel."""