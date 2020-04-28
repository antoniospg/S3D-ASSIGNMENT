#math imports
from random import random
from math import radians, degrees, atan2, sqrt, copysign, acos, cos

#python import
import copy

#blender imports
import mathutils
from mathutils import Quaternion, Vector
import bpy

class Turtle(object):
    #perform the turtle movements
    #attributes of Turtle class
    dir = Vector([0.0, 0.0, 1.0])
    pos = Vector([0.0, 0.0, 0.0])
    right = Vector([-1.0, 0.0, 0.0])
    width = 0.0
    
    def __init__(self, dir, pos, right, width):
        self.dir = dir
        self.pos = pos
        self.right = right
        self.width = width
        
        self.dir.normalize()
        self.right.normalize()
      
    def yaw(self, ang):
        #positive angle moves to the right
        axis  = self.dir.cross(self.right)
        axis.normalize()
        
        rot = Quaternion(axis, radians(ang))
        
        self.dir.rotate(rot)
        self.dir.normalize()
        self.right.rotate(rot)
        self.right.normalize()
           
    def pitch(self, ang):
        #positive angle rises turtle's nose
        self.dir.rotate(Quaternion(self.right, radians(ang)))
        self.dir.normalize()
        
    def roll(self, ang):
        #positive angle turn right
        self.right.rotate(Quaternion(self.dir, radians(ang)))
        self.right.normalize()
        
    def move(self, step):
        #move the turtle forward
        self.pos += self.dir * step

    def setWidth(self, width):
        self.width = width
        
    def resetVertical(self):
        self.dir = Vector([0.0, 0.0, 1.0])
        slef.right = Vector([-1.0, 0.0, 0.0])
 
class Branch(object):
    #attributes
    polyline = None
    start = Vector([0,0,0])
    turtle = None
    curve = None
    #handle lenght
    tang_l = 0.00
    
    def __init__(self, curve, turtle, tropism, trop_const):
        #set tropism
        axis = turtle.dir.cross(tropism)
        rot = Quaternion(axis, trop_const*axis.length)
        turtle.dir.rotate(rot)
        turtle.dir.normalize()
        
        self.polyline = curve.splines.new('BEZIER')
        self.curve = curve
        self.turtle = copy.deepcopy(turtle)
        self.start = self.turtle.pos
        self.polyline.bezier_points[0].co = self.start
        
        self.polyline.bezier_points[0].radius = self.turtle.width
        
        self.polyline.bezier_points[0].handle_left = self.turtle.pos
        self.polyline.bezier_points[0].handle_right = self.turtle.pos
        
        self.tang_l = 1
        
class Tree(object):
    #stack to put the branches
    stack = []
    curve = None
    obj = None
    #main Branch object
    stem = None
    #tropism vector and constant
    tropism = Vector([0,0,0])
    trop_const = 0.001
      
    def __init__(self, turtle, tropism, mean_step):
        self.tropism = tropism
        self.trop_const = mean_step/1000
        
        #create and bevel the curve
        self.curve = bpy.data.curves.new(name = "Tree",type='CURVE')
        self.curve.dimensions = '3D'
        self.curve.fill_mode = 'FULL'
        self.curve.bevel_depth = 0.045     
    
        #link the object to the scene
        self.obj = bpy.data.objects.new("Tree"+"Obj", self.curve)
        bpy.context.scene.collection.objects.link(self.obj)
        
        #create first branch and push into the stack
        self.stack.append(Branch(self.curve, turtle, self.tropism, self.trop_const))
        
        #set the handles to the turtles point
        self.stack[0].polyline.bezier_points[0].handle_left = self.stack[0].turtle.pos
        self.stack[0].polyline.bezier_points[0].handle_right = self.stack[0].turtle.pos
        
        self.stem = self.stack[0]
        
    def move(self, step):
        #update tangent lenght
        self.stem.tang_l = step/10
        #move turtle
        self.stem.turtle.move(step)
        
        #add new point
        self.stem.polyline.bezier_points.add(1)
        self.stem.polyline.bezier_points[-1].co = self.stem.turtle.pos
        
        #handles direction tangent to the curve
        self.stem.polyline.bezier_points[-1].handle_left = self.stem.turtle.pos - self.stem.turtle.dir*self.stem.tang_l
        self.stem.polyline.bezier_points[-1].handle_right = self.stem.turtle.pos + self.stem.turtle.dir*self.stem.tang_l
        
        #set the curve radius to be the turtle's width
        self.stem.polyline.bezier_points[-1].radius = self.stem.turtle.width
        
    def pitch(self, ang):
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_right= self.stem.turtle.pos + self.stem.turtle.dir*self.stem.tang_l
        
        #pitch the turtle
        self.stem.turtle.pitch(ang)
        
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_left = self.stem.turtle.pos - self.stem.turtle.dir*self.stem.tang_l
        
    def roll(self, ang):
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_right= self.stem.turtle.pos + self.stem.turtle.dir*self.stem.tang_l
        
        #roll the turtle
        self.stem.turtle.roll(ang)
        
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_left = self.stem.turtle.pos - self.stem.turtle.dir*self.stem.tang_l
        
    def yaw(self, ang):
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_right= self.stem.turtle.pos + self.stem.turtle.dir*self.stem.tang_l
        
        #yaw the turtle
        self.stem.turtle.yaw(ang)
        
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_left = self.stem.turtle.pos - self.stem.turtle.dir*self.stem.tang_l
        
    def fork(self):
        #create new branch and push into the stack
        self.stack.append(Branch(self.curve, self.stem.turtle, self.tropism, self.trop_const))
        #subscribe stem attribute with a new branch starting from the last vertex
        self.stem = self.stack[-1]
        
    def closeBranch(self):
        #pop out of the stack (set radius to 0 if no one is parent of this branch)
        self.stack.pop()
        #set the radius to 0
        self.stem.turtle.width = 0
        self.stem.polyline.bezier_points[-1].radius = self.stem.turtle.width
        
        #subscribe stem attribute with the previous branch
        if(len(self.stack) != 0): self.stem = self.stack[-1]
        
    def closeZBranch(self):
        #pop out of the stack
        self.stack.pop()
        #subscribe stem attribute with the previous branch
        if(len(self.stack) != 0): self.stem = self.stack[-1]
        
    def setW(self, width):
        #set the curve radius at turtle location
        self.stem.polyline.bezier_points[-1].radius = width
        self.stem.turtle.setWidth(width)
        
    def resetOrientation(self):
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_right= self.stem.turtle.pos + self.stem.turtle.dir*self.stem.tang_l
        
        #reset orientation of turtle
        self.stem.turtle.resetVertical()
        
        #set handle to be tangent to the segment
        self.stem.polyline.bezier_points[-1].handle_left = self.stem.turtle.pos - self.stem.turtle.dir*self.stem.tang_l
        
    def multiplyW(self, value):
        #multiply the turtle width by value
        self.stem.turtle.width *= value
        self.stem.polyline.bezier_points[-1].radius = self.stem.turtle.width
        
               
"""
TURTLE SYMBOLS

!(w) Set turtle width to w.
*(w) Multiply turtle width by w.
F(l) or f(l) Move turtle forward by l .
+(a) Turn turtle left by a.
-(a) Turn turtle right by a.
&(a) Pitch turtle down by a.
^(a) Pitch turtle up by a.
/(a) Roll turtle right by a.
n(a) Roll turtle left by a.
[ Start branch.
] End branch seting radius to 0.
$ Reset turtle to vertical
% Set Branch radius to 0
} End branch without seting radius to 0.

"""
 """ RATIOS ARE ALSO DEFINED IN THE PARSER """

"""  EXAMPLES OF SEQUENCES  """

""" SYMPODIAL TREE """
def genSympodialSeq(itr, step):
    #generate sequence that will move the turtle
    #commands are in the form of a tuples list tuple("symbol",[value1, value2,...])
    #list of commands in the form of [("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[])] 
    #ex: ("^",[45])
    
    lsys = []
    
    #AXIOM
    lsys.extend([("A",[step, 1*step])])
    res = []
    base_w = 1*step
    
    #CONSTANTS
    #contraction ratio 1
    r1 = 0.9
    #contraction ratio 2
    r2 = 0.7
    #branching angle 1
    a1 = 10
    #branching angle 2
    a2 = 50
    #width decrease rate
    wr = 0.657
    
    #REWRITING
    #repat itr times, changing the values
    for num in range(itr):
        for x in lsys:
            #REWRITE RULES:
            if(x[0] == "A"):
                w = x[1][1]
                l = x[1][0]
                
                res += [("!", [w]), ("F", [l]), ("[", []), ("&", [a1]), ("B", [l*r1, w*wr]), ("}", []), ("/", [180]),
                        ("[", []), ("&", [a2-30]), ("B", [l*r2, w*wr]), ("}", [])]
                        
            elif(x[0] == "B"):
                w = x[1][1]
                l = x[1][0]
                
                res += [("!", [w]), ("F", [l]), ("[", []), ("+", [a1]), ("B", [l*r1, w*wr]), ("}", []),
                        ("[", []), ("-", [a2]), ("B", [l*r2, w*wr]), ("}", [])]
            
            else:
                res += [(x[0],x[1])]
            ##      
        lsys = copy.deepcopy(res)
        res = []
    #end of principal branch
    lsys += [("}",[])]
    
    return lsys

""" WILLOW """
def genWillowSeq(itr, step):
    #generate sequence that will move the turtle
    #commands are in the form of a tuples list tuple("symbol",[value1, value2,...])
    #list of commands in the form of [("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[])] 
    #ex: ("^",[45])
    
    lsys = []
    
    #AXIOM
    lsys.extend([("T",[]), ("A",[])])
    res = []
    base_w = 3*step
    
    #REWRITING
    #repat itr times, changing the values
    for num in range(itr):
        for x in lsys:
            #REWRITE RULES:
            if(x[0] == "T"):
                res += [("!", [base_w]), ("F", [step*1.5]), ("T",[])]
            
            elif(x[0] == "A"):
                res += [("&", [90]), ("X", []), ("B", []), ("B", []), ("B", []), ("B", []), ("B", []), ("B", [])]
                
            elif(x[0] == "B"):
                res += [("-", [10]), ("X", []), ("-", [10]), ("X", []), ("-", [10]), ("X", [])]
                
            elif(x[0] == "X"):
                res += [("Z", []), ("-", [10]), ("Z", []), ("-", [10]), ("Z", []), ("-", [10]), ("Z", [])]
                
            elif(x[0] == "Z"):
                res += [("!", [base_w*0.2]), ("%", [])]
                
            elif(x[0] == "%"):
                i = random()
                if(i > 0.5): res += [("[", []), ("&", [15]), ("F", [step]), ("%", []), ("}", [])]
                else: res += [("[", []), ("&", [25]), ("F", [step]), ("%", []), ("!", [base_w*0.1]), ("[", []), ("-", [10]), ("F", [step]), ("%", []),
                                ("}", []), ("[", []), ("+", [10]), ("F", [step]), ("%", []), ("}",[]) , ("}",[])]
            
            else:
                res += [(x[0],x[1])]
            ##      
        lsys = copy.deepcopy(res)
        res = []
    #end of principal branch
    lsys += [("}",[])]
    
    return lsys

""" SEAWEED """
def genSeaweedSeq(itr, step):
    #generate sequence that will move the turtle
    #commands are in the form of a tuples list tuple("symbol",[value1, value2,...])
    #list of commands in the form of [("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[])] 
    #ex: ("^",[45])
    
    lsys = []
    
    #AXIOM
    lsys.extend([("F",[step])])
    res = []
    base_w = 0.5*step
    ang = 22
    
    #REWRITING
    #repat itr times, changing the values
    for num in range(itr):
        for x in lsys:
            #REWRITE RULES:
            if(x[0] == "F"):
                res += [("F", [step]), ("F", [step]), ("+", [ang]), ("[", []), ("^", [ang]), ("F", [step]), ("&", [ang]),
                        ("F", [step]), ("&", [ang]), ("F", [step]), ("]", []), ("-", [ang]), ("[", []), ("&", [ang]),
                        ("F", [step]), ("^", [ang]), ("F", [step]), ("^", [ang]), ("F", [step]), ("]", []), ("n", [step]),
                        ("[", []), ("&", [ang]), ("f", [step]), ("&", [ang]), ("f", [step]), ("^", [ang]), ("f", [step])]
            
            else:
                res += [(x[0],x[1])]
            ##      
        lsys = copy.deepcopy(res)
        res = []
    #end of principal branch
    lsys += [("]",[])]
    
    return lsys

""" BUSH """
def genBushSeq(itr, step):
    #generate sequence that will move the turtle
    #commands are in the form of a tuples list tuple("symbol",[value1, value2,...])
    #list of commands in the form of [("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[])] 
    #ex: ("^",[45])
    
    lsys = []
    
    #AXIOM
    lsys.extend([("A",[])])
    res = []
    base_w = 0.8*step
    ang = 22.5
    
    #REWRITING
    #repat itr times, changing the values
    for num in range(itr):
        for x in lsys:
            
            #REWRITE RULES:
            if(x[0] == "A"):
                res += [("[", []), ("&", [ang]), ("F", [step]), ("*", [0.8]), ("A", []),("F", [step]), ("]", []), ("/", [ang]),
                        ("/", [ang]), ("/", [ang]), ("/", [ang]), ("/", [ang]), ("[", []), ("&", [ang]), ("F", [step]),
                         ("*", [0.8]), ("A", [ang]), ("F", [step]), ("]", []), ("/", [ang]), ("/", [ang]), ("/", [ang]), ("/", [ang]), ("/", [ang]),
                         ("[", []), ("&", [ang]), ("F", [step]), ("*", [0.8]), ("A", []),("F", [step]), ("]", [])]
                         
            elif(x[0] == "F"):
                res += [("S", []), ("/", [ang]), ("/", [ang]), ("/", [ang]), ("/", [ang]), ("/", [ang]), ("F", [step])]
                
            elif(x[0] == "S"):
                res += [ ("F", [step]) , ("L", [])]
            
            elif(x[0] == "L"):
                res += [("[", []), ("^", [ang]), ("^", [ang]), ("[", []), ("-", [ang]), ("f", [step]), ("-", [ang]), ("f", [step]),
                        ("]", []),("]", [])]
                print(1)
            
            else:
                res += [(x[0],x[1])]
            ##      
        lsys = copy.deepcopy(res)
        res = []
    #end of principal branch
    lsys += [("}",[])]
    
    return lsys

""" A NICE TREE """
def genNiceTreeSeq(itr, step):
    #generate sequence that will move the turtle
    #commands are in the form of a tuples list tuple("symbol",[value1, value2,...])
    #list of commands in the form of [("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[]), ("",[])] 
    #ex: ("^",[45])
    
    ##CONSTANTS
    #divergence angle 1
    d1 = 94.74  
    #divergence angle 1   
    d2 = 132.63
    #branching angle
    a = 30.95
    #enlongating ratio
    lr = 1.229
    #widhth decrease ratio
    vr = 1.832
        
    lsys = []
    
    #AXIOM
    lsys.extend([("*",[1]),("F",[step]), ("/",[45]), ("A",[])])
    res = []
    base_w = 20*step
    
    #REWRITING
    #repat itr times, changing the values
    for num in range(itr):
        for x in lsys:
            
            #REWRITE RULES:
            if(x[0] == "A"):
                res += [("*", [1/vr]), ("F", [step/2]), ("[", []), ("&", [a]), ("F", [step/2]), ("A", []), ("}", []),
                        ("/", [d1]), ("[", []), ("&", [a]), ("F", [step/2]), ("A", []), ("}", []),
                        ("/", [d2]), ("[", []), ("&", [a]), ("F", [step/2]), ("A", []), ("}", [])]
                        
            elif(x[0] == "F"):
                l = x[1][0]
                
                res += [("F", [l*lr])]
                
            elif(x[0] == "*"):
                w = x[1][0]
                print(w)
                res += [("*", [1/(vr)])]
            
            else:
                res += [(x[0],x[1])]
            ##      
        lsys = copy.deepcopy(res)
        res = []
    #end of principal branch
    lsys += [("}",[])]
    
    return lsys
    
""" SEQUENCE INTERPRETER """
def parser(tree, i, info):
    
    """ RATIOS ARE ALSO DEFINED IN THE FUNCTION """
    if(i == 0):
        seq = genSympodialSeq(info[0], info[1])
        tree.stem.turtle.width = info[1]*1
    elif(i == 1):
        seq = genWillowSeq(info[0], info[1])
        tree.stem.turtle.width = info[1]*3
    elif(i == 2): 
        seq = genSeaweedSeq(info[0], info[1])
        tree.stem.turtle.width = info[1]*0.5
    elif(i == 3): 
        seq = genBushSeq(info[0], info[1])
        tree.stem.turtle.width = info[1]*0.8
    elif(i == 4): 
        seq = genNiceTreeSeq(info[0], info[1])
        tree.stem.turtle.width = info[1]*20
    
    #transform sequence in steps
    for x in seq:
        ##interpreter rules
        
        if(x[0] == "!"): tree.setW(x[1][0])
        
        elif(x[0] == "F"): tree.move(x[1][0])
        
        elif(x[0] == "f"): tree.move(x[1][0])
        
        elif(x[0] == "+"): tree.yaw((-1)*x[1][0])
        
        elif(x[0] == "-"): tree.yaw(x[1][0])
        
        elif(x[0] == "&"): tree.pitch((-1)*x[1][0])
        
        elif(x[0] == "^"): tree.pitch(x[1][0])
        
        elif(x[0] == "/"): tree.roll(x[1][0])
        
        elif(x[0] == "n"): tree.roll((-1)*x[1][0])
        
        elif(x[0] == "["): tree.fork()
        
        elif(x[0] == "]"): tree.closeBranch()
        
        elif(x[0] == "$"): tree.resetOrientation()
        
        elif(x[0] == "*"): tree.multiplyW(x[1][0])
        
        elif(x[0] == "%"): tree.setW(0)
        
        elif(x[0] == "}"): tree.closeZBranch()
          
def run():
    """ DEFINE TYPE OF TREE """
    """
    i = 0: SYMPODIAL TREE
        1: WILLOW
        2: SEAWEED
        3: BUSH
        4: NICE TREE
    """
    i = 4
    
    """ DEFINE INITIAL ATTRIBUTES OF THE TURTLE """  
    direction = mathutils.Vector([0.0, 0.0, 1.0])
    position = mathutils.Vector([0.0, 0.0, 0.0])
    right = mathutils.Vector([-1.0, 0.0, 0.0])
    
    """ DEFINE TROPISM VECTOR """
    """ EACH CORDINATE WITH ABSOLUTE VALUE FROM 0 TO 100"""
    tropism = mathutils.Vector([0.0, 0.0, 00.0])
    
    """ DEFINE NUMBER OF ITERATIONS"""
    """
    MAX ITERATIONS OF EACH TREE:
        PINE:
        WILLOW: 8
        SEAWEED: 3
        BUSH: 5
        NICE TREE: 8   (7-best)
    """
    itr = 6
    
    """ DEFINE STEP """
    """ 10 is a good value """
    step = 20
        
    tree = Tree(Turtle(direction, position, right, 0.0), tropism, step)
    parser(tree, i, [itr, step]) 

    


run()






