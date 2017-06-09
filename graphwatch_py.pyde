# Animation Example
from embeddedgraphs import *
import copy

time = 0   # use time to move objects from one frame to the next
framecount=0
home=os.path.expanduser("~")
#torus
'''
bigM=8
lilm=5
simp=[[(a,b), ((a)%bigM,(b+1)%lilm), ((a+1)%bigM,(b+1)%lilm)] for a in range(bigM) for b in range(lilm)]
simp+=[[(a,b), ((a+1)%bigM,(b)%lilm), ((a+1)%bigM,(b+1)%lilm)] for a in range(bigM) for b in range(lilm)]
edges=[[(a,b),((a+1)%bigM,(b))] for a in range(bigM) for b in range(lilm)]
edges+=[[(a,b),(a,(b+1)%lilm)] for a in range(bigM) for b in range(lilm)]
#edges+=[[(a,b),((a+1)%bigM,(b+1)%lilm)] for a in range(bigM) for b in range(lilm)]
'''

'''
#Mobius
m=25
mn=5
edges=[ [ (foo,k), (foo,k+1)] for foo in range(m+1) for k in range(mn)]# for foo in range(m) for k in range(mn)]
edges+=[ [ (foo,k), (foo+1,k)] for foo in range(m) for k in range(mn+1)]# for foo in range(m) for k in range(mn)]
edges+=[[(foo,k),(foo+1,k+1)] for foo in range(m) for k in range(mn)]
edges+=[[(0,k),(m,mn-k)] for k in range(mn+1)]
edges+=[[(0,k),(m,mn-k-1)] for k in range(mn)]
#edges+=[[(0,k),(m,mn-k+1)] for k in range(mn-1)]
'''
oggs=[simplicify(icosahedron()) for foo in range(3)]
oggcol=[(255,0,0),(200,55,0),(150,155,0)]
far=1.3
oggspot=[(far*sin(PI*2.0*foo/3), far*cos(PI*2.0*foo/3),0) for foo in range(3)]

def setup():
    size (800, 800, P3D)
    perspective (60 * PI / 180, 1, 0.1, 1000)  # 60 degree field of view
    
def draw():
    global time
    global framecount
    framecount += 1
    time += 0.01
    camera (0, 0, 5, 0, 0, 0, 0,  1, 0) # zcameraspot([ogg],factor=1.3)# position the virtual camera
    background (28,28,28)
    #background (25, 255, 255)
    # create a directional light source
    ambientLight(50, 50, 50);
    lightSpecular(255, 255, 255)
    directionalLight (100, 100, 100, -0.3, 0.5, -1)
    noStroke()
    specular (180, 180, 180)
    shininess (20.0)
    pushMatrix()
    #scale(30,30,1)
    for foo in range(3):
        ogg=oggs[foo]
        pushMatrix()
        #rotateX(time)
        spot=oggspot[foo]
        translate(*spot)
        mo=neg_coulomb_gradient(ogg, .01, 0.5, edge_length=.5)
        ogg.push(mo)
        drawgraph(ogg,simplex_color=oggcol[foo])
        popMatrix()
    popMatrix()
    if framecount%3==0:
        saveFrame(home+"/Desktop/anima/frame-#####.png")
    
def drawgraph(g, simplex_color=(255,0,0), draw_simplices=True, draw_edges=False, edge_color=(0,255,0), edge_vol=.0006, draw_vertices=False, vertex_color=(0,0,255), vertex_size=0.08):
    if draw_simplices:
        fill(*simplex_color)
        for s in g.simplices:
            beginShape()
            for v in s:
                vertex(*g.positions[v])
            endShape()
    if draw_edges:
        fill(*edge_color)
        for e in g.edges:
            p1=g.positions[e[0]]
            p2=g.positions[e[1]]
            drawedge(p1,p2, V=edge_vol)
    if draw_vertices:
        fill(*vertex_color)
        for v in g.verts:
            pushMatrix()
            translate (*(g.positions[v]))
            sphereDetail(40)
            sphere(vertex_size)
            popMatrix()

        
def drawedge(p1, p2, V=PI*.0002):
    dir=[p1[foo]-p2[foo] for foo in range(len(p1))]
    h=sqrt(sum([foo**2 for foo in dir]))
    udir=[foo/h for foo in dir]
    r=sqrt(V/h)
    #r=min([.1,r])
    pushMatrix()
    translate(*p2)
    applyMatrix(*zaxistovmat(udir))
    scale(r,r,h)
    cylinder()
    popMatrix()
    

# cylinder with radius = 1, z range in [0,1]
def cylinder(sides = 64):
    # first endcap
    '''    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 0)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    '''    # sides
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, 0)
        normal (x2, y2, 0)
        vertex (x2, y2, 0)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2