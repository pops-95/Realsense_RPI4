import numpy as np
import matplotlib.pyplot as plt
from pytransform3d.plot_utils import make_3d_axis
import pytransform3d.transformations as pt

R=np.eye(3)
P=[0,-0.17,-0.7] 
A2B=pt.transform_from(R,P)
print("Transformation Matrix for 1 to camera point:")
print(A2B)

points=[0.301,0.096,0.547,1]
transformed=pt.transform(A2B,points)
print("Transformed values =" +str(transformed))


# R=np.eye(3)
# P=[0,-0.073,.115] 
# A2C=pt.transform_from(R,P)
# print("Transformation Matrix from 1 to ref point:")
# print(A2C)

# points=[transformed[0],transformed[1],transformed[2],1]
# transformed=pt.transform(A2C,points)
# print("Transformed values =" +str(transformed))


#plotting the point in 3d space

# ax= make_3d_axis(1)
# pt.plot_transform(ax,A2B)
# ax.scatter(points[0], points[1], points[2])
# plt.show()