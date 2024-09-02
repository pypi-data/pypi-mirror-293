

import numpy as np
import matplotlib.pyplot as plt

# z = -np.linspace(9,15,100)
# x = np.linspace(-26,26,1000)
#
# x,z = np.meshgrid(x,z)
#
# Z = -np.exp(-0.05*z) +4*(z+10)**2
# X = x**2
#
#
# plt.contour(x,z,(X+Z),[0])
# plt.xlim([-1.5,1.5])
# plt.ylim([-11.5,-8.5])

import numpy as np
from matplotlib import pyplot as plt
from math import pi

u = 10.5     #x-position of the center
v = 0.0    #y-position of the center
a = 1.5     #radius on the x-axis
b = 1.    #radius on the y-axis

t = np.linspace(0, pi, 50)

with open('europa_torus.txt', 'w+') as f:
    for ti in t:
        f.write('   {:.7e},  {:.7e}\n'.format(u+a*np.cos(ti), v+b*np.sin(ti)))

plt.plot(u+a*np.cos(t), v+b*np.sin(t))
plt.grid(color='lightgray',linestyle='--')
plt.show()
