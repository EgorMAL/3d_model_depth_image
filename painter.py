"""Function to draw model"""
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d
from box import Box

def draw_box(box:Box, ax):
    """Function to draw model"""
    x = box.start_point[0]
    y = box.start_point[1]
    z = box.start_point[2]
    dx = box.d[0]
    dy = box.d[1]
    dz = box.d[2]

    p = Rectangle((x, y),dx,dy,fc="red",ec='black') # низ
    p2 = Rectangle((x, y),dx,dy,fc="red",ec='black') # вверх

    # one side
    p3 = Rectangle((y,z),dy,dz,fc="red",ec='black') #
    p4 = Rectangle((y,z),dy,dz,fc="red",ec='black') #

    # another side
    p5 = Rectangle((x,z),dx,dz,fc="red",ec='black') #
    p6 = Rectangle((x,z),dx,dz,fc="red",ec='black') #

    ax.add_patch(p)
    ax.add_patch(p2)
    ax.add_patch(p3)
    ax.add_patch(p4)
    ax.add_patch(p5)
    ax.add_patch(p6)

    art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
    art3d.pathpatch_2d_to_3d(p2, z=z+dz, zdir="z")
    art3d.pathpatch_2d_to_3d(p3, z=x, zdir="x")
    art3d.pathpatch_2d_to_3d(p4, z=x+dx, zdir="x")
    art3d.pathpatch_2d_to_3d(p5, z=y, zdir="y")
    art3d.pathpatch_2d_to_3d(p6, z=y+dy, zdir="y")
