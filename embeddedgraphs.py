import random as rnd
from itertools import combinations

class EmbedGraph:
#creates a graph with vertices positioned randomly in space
    def __init__(self, edges, positions = {}, space_dim=3 ):
        self.edges=edges[:]
        vertices = [e[0] for e in edges] + [e[1] for e in edges]
        vertices=list(set(vertices[:]))
        self.verts = vertices
        if not positions:
            positions = []
            for v in vertices:
                pos = [3*(rnd.random()-.5) for a in range(space_dim)]
                positions.append( [v, pos] )
            positions=dict(positions)
        self.positions = positions
        combs=[a for a in combinations(vertices,2)]
        rev_edges=[e[::-1] for e in edges]
        self.rev_edges = rev_edges
        nonedges = [a for a in combs if not( a in edges or a in rev_edges)]
        rev_nonedges = [e[::-1] for e in nonedges]
        self.nonedges=nonedges
        self.revnonedges=rev_nonedges

    def move(self, new_positions):
        #Updates the positions dictionary of the embedded graph
        self.positions.update(new_positions)

    def push(self, shift):
        #Update the positions by adding
        pos=self.positions
        vs = shift.keys()
        pos.update( {v: listsum(pos[v], shift[v])  for v in vs} )
        self.move(pos)



class SimplicialComplex(EmbedGraph):
    def __init__(self, simplices=[], edges=[], update_edges=True):
        self.simplices=simplices
        oneskeleton=edges
        if update_edges:
            for s in simplices:
                oneskeleton+=[a for a in combinations(s,2) if (a not in oneskeleton)]
        EmbedGraph.__init__(self, edges=oneskeleton)
        dual_edges=[]
        for ss in combinations(simplices,2):
            overlap= set(ss[0]).intersection(set(ss[1]))
            if len(overlap)==2:
                dual_edges.append( ss )
        self.dual_edges=dual_edges


def simplicify(graph):
    simps=[]
    for tri in combinations(graph.verts,3):
        if all([ (ed in graph.edges) or (ed in graph.rev_edges) for ed in combinations(tri,2)]):
            simps.append( tri )
    return SimplicialComplex(simplices=simps, edges=graph.edges)



def distsq( v1, v2):
    return sum( [ (a-b)**2 for a,b in zip(v1,v2) ] )

def listsum(l1,l2):
    return [ float(a + b) for a,b in zip(l1,l2)]

def listdiff(l1,l2):
    return [ float(a - b) for a,b in zip(l1,l2)]

def listscale(a,v):
    return [ float(a * b) for b in v]

def crossproduct(v,w):
    return [ v[(foo+1)%3] * w[(foo+2)%3] - v[(foo-1)%3] * w[(foo-2)%3] for foo in range(3)]

def normalize(v):
    return listscale(  ( sum([foo**2 for foo in v]) )**-.5  , v)

def neg_coulomb_gradient( g, step=.01, alpha=1.0, edge_length=1.0, power=2.0):
    #negative gradient for potential: coloumb between nonadjacent, (d^2-1)^2 between adjacent
    #parameter alpha gives coloumb strength
    pos = g.positions
    p=pos.values()
    grad = { v: len(pos[v]) * [0.0] for v in g.verts}
    for v,w in combinations(g.verts,2):
        xv = pos[v]
        xw = pos[w]
        if (v,w) in g.edges or (v,w) in g.rev_edges:
            q =  edge_length - distsq(xv,xw)
        elif power == 2.0:
            q =  alpha / ( distsq(xv,xw) )
        else:
            q = alpha / sum([(a-b)**2 for a,b in zip(xv,xw)])**(power/2)
        dxv = listdiff( xv, xw)
        dxv = listscale(step* q, dxv)
        dxw = listscale( -1, dxv)
        dxv = listsum(dxv, grad[v])
        dxw = listsum(dxw, grad[w])
        grad.update({v:dxv})
        grad.update({w:dxw})
    return grad

def icosahedron():
    icosedges=[[0, 1], [0, 5], [0, 7], [0, 8], [0, 11], [1, 2], [1, 5], [1, 6], [1, 8], [2, 3], [2, 6], [2, 8], [2, 9], [3, 4], [3, 6], [3, 9], [3, 10], [4, 5], [4, 6], [4, 10], [4, 11], [5, 6], [5, 11], [7, 8], [7, 9], [7, 10], [7, 11], [8, 9], [9, 10], [10, 11]]
    icosedges= [tuple(e) for e in icosedges]
    return EmbedGraph(icosedges[:])

def graphglue(graph0,vertex0,graph1,vertex1):
    pass

def zaxistovmat(v):
    if v==[0,0,1]:
        return [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
    if v==[0,0,-1]:
        return [-1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
    else:
        v1=normalize(crossproduct(v,[0,0,1]))
        v2=crossproduct(v,v1)
        return [v1[0], v2[0], v[0], 0, v1[1], v2[1], v[1], 0,  v1[2], v2[2], v[2], 0, 0, 0, 0, 1 ]

def zcameraspot(gs,factor=35):
    minxpos=-1
    maxxpos=1
    minypos=-1
    maxypos=1
    
    for g in gs:
        for v in g.verts:
            p=g.positions[v]
            minxpos=min([minxpos, p[0]])
            maxxpos=max([maxxpos, p[0]])
            minypos=min([minypos, p[1]])
            maxypos=max([maxypos, p[1]])
    d=max([maxxpos-minxpos,maxypos-minypos])
    return max([1,factor*d])

def simp_normal(g, simp):
    va = listdiff( g.positions[simp[0]] , g.positions[simp[1]] )
    vb = listdiff( g.positions[simp[0]] , g.positions[simp[2]] )
    return crossproduct(va,vb)