import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plotSetup(xmin = -6.0, xmax = 6.0, ymin = -2.0, ymax = 4.0):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    return ax

def formatEqn(coefs, b):
    leadingLabel = {-1: '-{} x_{}', 0: '', 1: '{} x_{}'}
    followingLabel = {-1: ' - {} x_{}', 0: '', 1: ' + {} x_{}'}
    nterms = len(coefs)
    i = 0
    # skip initial terms with coefficient zero
    while ((i < nterms) and (np.sign(coefs[i]) == 0)):
        i += 1
    # degenerate equation 
    if (i == nterms):
        return '0 = {}'.format(b)
    # first term is formatted slightly differently
    if (np.abs(coefs[i]) == 1):
        label = leadingLabel[np.sign(coefs[i])].format('',i+1)
    else:
        label = leadingLabel[np.sign(coefs[i])].format(np.abs(coefs[i]),i+1)
    # and the rest of the terms if any exist
    for j in range(i+1,len(coefs)):
        if (np.abs(coefs[j]) == 1):
            label = label + followingLabel[np.sign(coefs[j])].format('',j+1)
        else:
            label = label + followingLabel[np.sign(coefs[j])].format(np.abs(coefs[j]),j+1)
    label = label + ' = {}'.format(b)
    return label

def plotLinEqn (a1, a2, b):
    # a1 x + a2 y = b
    [xmin, xmax] = plt.xlim()
    x1 = xmin
    y1 = (b - (x1 * a1))/float(a2)
    x2 = xmax
    y2 = (b - (x2 * a1))/float(a2)
    plt.plot([x1, x2],[y1, y2], label='${}$'.format(formatEqn([a1, a2],b)))

def centerAxes (ax):
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def plotSetup3d(xmin = -3.0, xmax = 3.0, ymin = -3.0, ymax = 3.0, zmin = -3.0, zmax = 3.0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.axes.set_xlim([xmin, xmax])
    ax.axes.set_ylim([ymin, ymax])
    ax.axes.set_zlim([zmin, zmax])
    ax.axes.set_xlabel('$x_1$')
    ax.axes.set_ylabel('$x_2$')
    ax.axes.set_zlabel('$x_3$')
    return ax

def plotLinEqn3d(ax, l1, color='Green'):
    # a1 x + a2 y + a3 z = b
    pts = intersectionPlaneCube(ax, l1)
    ptlist = np.array([np.array(i) for i in pts])
    x = ptlist[:,0]
    y = ptlist[:,1]
    z = ptlist[:,2]
    if (len(x) > 2):
        try:
            triang = mp.tri.Triangulation(x, y)
        except:
            # this happens where there are triangles parallel to the z axis
            # so some points in the x,y plane are repeated (which is illegal for a triangulation)
            # this is a hack but it works!
            try:
                triang = mp.tri.Triangulation(x, z)
                triang.y = y
            except:
                triang = mp.tri.Triangulation(z, y)
                triang.x = x
        ax.plot_trisurf(triang, z, color=color, alpha=0.3, linewidth=0, shade=False)

def intersectionPlaneCube(ax, l1):
    # returns the vertices of the polygon defined by the intersection of a plane
    # and the rectangular prism defined by the limits of the axes
    bounds = np.array([ax.axes.get_xlim(), ax.axes.get_ylim(), ax.axes.get_zlim()])
    coefs = l1[0:3]
    b = l1[3]
    points = []
    for x in [0, 1]:
        for y in [0, 1]:
            for z in [0, 1]:
                corner = [x, y, z]
                # 24 corner-pairs 
                for i in range(3):
                    # but only consider each edge once (12 unique edges)
                    if corner[i] == 0:
                        # we are looking for the intesection of the line defined by
                        # the two constant values with the plane
                        isect = (b - np.sum([coefs[k] * bounds[k][corner[k]] for k in range(3) if k != i]))/float(coefs[i])
                        if ((isect >= bounds[i][0]) & (isect <= bounds[i][1])):
                            pt = [bounds[k][corner[k]] for k in range(3)]
                            pt[i] = isect
                            points.append(tuple(pt))
    return set(points)

def plotIntersection3d(ax, eq1, eq2, color='Blue'):
    bounds = np.array([ax.axes.get_xlim(), ax.axes.get_ylim(), ax.axes.get_zlim()])
    tmp = np.array([np.array(eq1), np.array(eq2)])
    A = tmp[:,:-1]
    b = tmp[:,-1]
    ptlist = []
    for i in range(3):
        vars = [k for k in range(3) if k != i]
        A2 = A[:][:,vars]
        for j in range(2):
            b2 = b - bounds[i,j] * A[:,i]
            try:
                pt = np.linalg.inv(A2).dot(b2)
            except:
                continue
            if (pt[0] >= bounds[vars[0]][0]) & (pt[0] <= bounds[vars[0]][1]) & (pt[1] >= bounds[vars[1]][0]) & (pt[1] <= bounds[vars[1]][1]):
                point = [0,0,0]
                point[vars[0]] = pt[0]
                point[vars[1]] = pt[1]
                point[i] = bounds[i,j]
                ptlist.append(point)
    ptlist = np.array(ptlist).T
    ax.plot(ptlist[0,:], ptlist[1,:], zs = ptlist[2,:], color=color)

