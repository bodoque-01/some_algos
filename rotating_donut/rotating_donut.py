import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 2 * np.pi, 200)
p = np.linspace(0, 2 * np.pi, 200)

theta, phi = np.meshgrid(t, p)
print(theta)
R, r = 2, 1


# Ah well, logic for this is the following:
# Get that we basically draw a big circle, the one that a "smaller" perpendicular circle will rotate in, orbit it.
# To draw the big circle in XY, simple: just (R * cos(theta), R*sin(theta), 0) (or add some height if needed for the specific implementation).
# Now, for the smaller circle, it must orbit "inside" the big one, so the center is just (R * cos(theta), R*sin(theta), 0).
# The final Z now, because the circle is orthogonal to the big circle that lies in XY, it'll play the part of the circle's vertical radius, thus Z = r*sin(phi).
# The small circle has two directions it can go:
# Up/Down, pure Z/vertical motion, Z = r*sin(phi)
# Toward/Away from origin, r*cos(theta).
# Here's the critical part: "toward/away from origin" is NOT the same as "in the X/Y direction"
# What direction IS "radially outward"? At angle θ on the big circle, "outward" means the direction (cos(theta), sin(theta), 0). 
# Thus, to get the X and Y components of the small circle's "toward/away from origin" motion, we multiply r*cos(phi) by cos(theta) for X and sin(theta) for Y. Because if we are inside the small circle, moving "outward" means moving along the direction defined by the big circle's angle θ.

X = R * np.cos(theta) + (np.cos(theta) * r * np.cos(phi))
Y = R * np.sin(theta) + (r * np.cos(phi) * np.sin(theta))
Z = r * np.sin(phi)



fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()