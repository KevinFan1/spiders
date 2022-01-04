import time

from pymouse.mac import PyMouse

m = PyMouse()
m.click(500, 500, 1)
m.click(500, 500, 1)
time.sleep(10.053)
m.click(500, 500, 1)
