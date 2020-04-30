################################
#
#   RRT Pseudo CodeQgoal //region that identifies success
#    Counter = 0 //keeps track of iterations
#    lim = n //number of iterations algorithm should run for
#    G(V,E) //Graph containing edges and vertices, initialized as empty
#    While counter < lim:
#        Xnew  = RandomPosition()
#        if IsInObstacle(Xnew) == True:
#            continue
#        Xnearest = Nearest(G(V,E),Xnew) //find nearest vertex
#        Link = Chain(Xnew,Xnearest)
#        G.append(Link)
#        if Xnew in Qgoal:
#            Return G
#    Return G
#
#########################################

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
import math

class Point:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

def dist(p1, p2):
     return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

def LineIntersectCircle(p,lsp,lep):
# p is the circle parameter, lsp and lep is the two end of the line
  x0,y0,r0 = p
  x1,y1 = lsp.x,lsp.y
  x2,y2 = lep.x,lep.y
  if x1 == x2:
    if abs(r0) >= abs(x1 - x0):
        p1 = x1, y0 - math.sqrt(r0**2 - (x1-x0)**2)
        p2 = x1, y0 + math.sqrt(r0**2 - (x1-x0)**2)
        inp = [p1,p2]
        # select the points lie on the line segment
        inp = [p for p in inp if p[1]>=min(y1,y2) and p[1]<=max(y1,y2)]
    else:
        inp = []
  else:
    k = (y1 - y2)/(x1 - x2)
    b0 = y1 - k*x1
    a = k**2 + 1
    b = 2*k*(b0 - y0) - 2*x0
    c = (b0 - y0)**2 + x0**2 - r0**2
    delta = b**2 - 4*a*c
    if delta >= 0:
        p1x = (-b - math.sqrt(delta))/(2*a)
        p2x = (-b + math.sqrt(delta))/(2*a)
        p1y = k*x1 + b0
        p2y = k*x2 + b0
        inp = [[p1x,p1y],[p2x,p2y]]
        # select the points lie on the line segment
        inp = [p for p in inp if p[0]>=min(x1,x2) and p[0]<=max(x1,x2)]
    else:
        inp = []
  return inp


def get_ordered_list(points, x, y):
   points.sort(key = lambda p: math.sqrt((p.x - x)**2 + (p.y - y)**2))
   return points

#Creating a graph
G = nx.Graph()
iteration_max = 100
counter = 0

XDIM = 20
YDIM = 20
Epsilon = 1

qinit = Point
qinit.x = 10
qinit.y = 10

print('init point')
print(qinit.x,qinit.y)

G.add_node(0, pos= (qinit.x, qinit.y) )


qgoal = Point(5,5, 0)


while counter < iteration_max:
    if counter == 0:
        qstart = qinit
        qcircle = [qstart.x,qstart.y,1]


    #Random Point
    qrand = Point(random.randint(0, 20),random.randint(0, 20), -1)
    print(qrand.x,qrand.y)
    
    points = []
    distances = []
    #loop over G to compute distance to find nearest Vertex
    print('these are the nodes')
    for n, data in G.nodes(data=True):

        print(n, data['pos'])
        p = Point(data['pos'][0],data['pos'][1], n)
        points.append(p)
        distances.append(dist(points[n],qrand))
       
    
    print(distances)

    #Gets ordered list
    points = get_ordered_list(points,qrand.x, qrand.y)


    distance = dist(points[0],qrand)

    if distance > 1:
        ### This function crashes sometimes for some reason, need debug..
        qnew = LineIntersectCircle(qcircle,qstart,qrand)  
        flat_list = Point(qnew[0][0], qnew[0][1], -1)
    else: 
        flat_list = qrand
        print('This id will be less than a meter away !')
        print(points[0].id)


    counter += 1
    #adding new edge and nodes
    G.add_node(counter, pos=(flat_list.x,flat_list.y))
    G.add_edge(counter,points[0].id)


    if (flat_list.x == qgoal.x and flat_list.y == qgoal.y):
        print('arrived at goal !!!!')
        break
 
    else:    
        qstart = flat_list
        qcircle = [qstart.x,qstart.y,1]
        

print('hello !')
print(G)
nx.draw(G, pos=nx.spring_layout(G),with_labels=True)    
plt.draw()
plt.savefig("hello.png" ) # save as png












