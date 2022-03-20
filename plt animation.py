import random
import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
#% matplotlib qt

l1= [10, 30, 20,5,6]
l2 = [30, 5, 44, 22, 48]

fig, axes = plt.subplots(nrows = 1, ncols = 1, figsize = (15,5)) 
plt.style.use("ggplot")

x1,y1,y2,y3 = [], [], [], []
xval = count(0,3)
def animate(i):
    x1.append(next(xval))
    y1.append((l1[i]))
    axes.set_title("o")
    axes.plot(x1,y1, color="red")
    
anim = FuncAnimation(fig, animate, interval=30)

f = 'C:/Users/Anika Nath/MIT/1st UROP/ani.gif'
writergif = animation.PillowWriter(fps=30) 
anim.save (f, writer=writergif)