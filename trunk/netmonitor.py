#!/usr/bin/env python

# netmonitor.py, by Yusuke Shinyama, *public domain*

import Tkinter, re

class Monitor:
  
  status = "/proc/net/dev"
  
  def __init__(self, dev="eth0", geometry="2x2+0+0", background="black",
               color_in="green", color_out="red", color_in_out="yellow", delay=100):
    self.background = background
    self.color_in = color_in
    self.color_out = color_out
    self.color_in_out = color_in_out
    self.delay = delay
    self.pat = re.compile(r"^\s*"+dev+r":\s*(\d+)\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*(\d+)")
    self.w = Tkinter.Tk()
    self.w.wm_overrideredirect(1)
    self.w.wm_geometry(geometry)
    self.w.configure(bg=self.background, bd=0)
    self.w.after(self.delay, self.watch)
    self.nin = 0
    self.nout = 0
    Tkinter.mainloop()
    # not reached

  def watch(self):
    f = open(self.status);
    f.readline(); f.readline()
    while 1:
      s = f.readline()
      if not s: break
      m = self.pat.match(f.readline())
      if m:
        (i, o) = (long(m.group(1)), long(m.group(2)))
        break
    f.close()
    c = self.background
    if self.nin+512 < i and self.nout < o:
      c = self.color_in_out
    elif self.nin+512 < i:
      c = self.color_in
    elif self.nout < o:
      c = self.color_out
    (self.nin, self.nout) = (i, o)
    self.w.configure(bg=c)
    self.w.update_idletasks()
    self.w.after(self.delay, self.watch)
    return

if __name__ == "__main__":
  Monitor()
