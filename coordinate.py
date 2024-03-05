import numpy as np
import matplotlib.pyplot as plt
from pytransform3d.plot_utils import make_3d_axis
import pytransform3d.transformations as pt

R=np.eye(3)
P=[-0.017,-0.157,-0.880] 
A2B=pt.transform_from(R,P)
print("Transformation Matrix:")
print(A2B)

points=[-0.076,0.099,0.920,1]
transformed=pt.transform(A2B,points)
print("Transformed values =" +str(transformed))