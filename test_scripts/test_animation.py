
'''
This is to gain familiarity with how the matplotlib.animation library works in practice.

Items of interest learned:
- various settings declared on Axes need to be included in the update-loop, e.g. ax.set_xticks([])
- the variable `num` (sometimes called `frames`) as below in the update function is actually required, even if it's not explicitly used
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


t = np.linspace(0,10)

fig, ax = plt.subplots()
sharedProps = {"xticks": [], "yticks": []}

def update(frame, t):
    x = [np.random.randint(0,10) for _ in t]
    y = [np.random.randint(0,10) for _ in t]
    print(frame)
    ax.clear()
    ax.scatter(x, y, marker='o')
    ax.update(sharedProps)
    



ani = animation.FuncAnimation(fig, update, 20, interval=200, fargs=[t])
ani.save('test_scripts/animation_drawing.gif', writer="imagemagick", fps=5)