#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#import sympy as sp

from math import copysign

minimal_difference = 0.003
from scipy import array as ar
m_d = minimal_difference
minimal_speed = 0.002; m_s = minimal_speed

def vector_value(v):
    return (v[0]**2+v[1]**2)**0.5

def compose_equation_line(segment): # ax+by+c=0
    global m_d
    if len(segment) == 4:
        l = segment
        if abs(l[2]-l[0])<=m_d:
            b=0; a=1; c=-l[0]
        elif abs(l[3]-l[1])<=m_d:
            a=0; b=1; c=-l[1]
        else:
            a=-(l[3]-l[1])/(l[2]-l[0])
            b=1
            c=0-a*l[2]-b*l[3]
        return [a,b,c]

    elif len(segment) == 2:
        l = segment
        if abs(l[1][0]-l[0][0])<=m_d:
            b=0; a=1; c=-l[0][0]
        elif abs(l[1][1]-l[0][1])<=m_d:
            a=0; b=1; c=-l[0][1]
        else:
            a=-(l[1][1]-l[0][1])/(l[1][0]-l[0][0])
            b=1
            c=0-a*l[1][0]-b*l[1][1]
        return [a,b,c]


def compose_normal_line(coefs,optcoords=None):
    if type(optcoords)!= type(None):
        ss = compose_normal_line(coefs)
        c=0-ss[0]*optcoords[0]-ss[1]*optcoords[1]
        return ar([ss[0],ss[1],c])

    else:
        if coefs[0]==0:
            return ar([1,0,0])
        if coefs[1]==0:
            return ar([0,1,0])
        else:
            if coefs[1]!=1:
                return compose_normal_line(ar(coefs)/coefs[1])

            a=-1/coefs[0]
            b=coefs[1]
            return ar([a,b,0])

def seq_to_line(points):
    xprev = -1; yprev=-1
    lines = list()
    for point in points:
        if xprev==-1:
            xprev=point[0]; yprev=point[1]
        else:
            line = [xprev,yprev,point[0],point[1]]
            xprev = point[0]; yprev = point[1]
            lines.append(line)
    return lines

def find_intersection(line1,line2):
    a1=line1[0];a2=line2[0];b1=line1[1];b2=line2[1]
    c1=line1[2];c2=line2[2]
    if abs(b1*b2)>m_d:
        x=(-c1/b1+c2/b2)/(a1/b1-a2/b2)
        y=(-c1-a1*x)/b1
    elif abs(b1)<m_d and abs(b2)>m_d:
        x = -c1/a1
        y = (-c2-a2*x)/b2
    elif abs(b2)<m_d and abs(b1)>m_d:
        x = -c2/a2
        y = (-c1-a1*x)/b1
    elif abs(b2)<m_d and abs(b1)<m_d:
        return []
    return[x,y]

def segments_have_intersection(seg1coords,seg2coords):
    s1 = seg1coords; s2 = seg2coords
    if (min(s1[0],s1[2])<max(s2[0],s2[2]) and max(s1[0],s1[2])>min(s2[0],s2[2])): #or (min(s2[0],s2[2])<max(s1[0],s1[2]) and max(s2[0],s2[2])>min(s1[0],s1[2])):
        if (min(s1[1],s1[3])<max(s2[1],s2[3]) and max(s1[1],s1[3])>min(s2[1],s2[3])):
            return True
    return False

def distance_point_point(point1,point2):
    return vector_value(point2-point1)

def resultant_speed(obj1,obj2):
    return [obj2.mass/obj1.mass*(-1)*obj1.vx, obj2.mass/obj1.mass * (-1)* obj1.vy]

def cos_vect(v1,v2):
    return (scal_mult(v1,v2)/vector_value(v1)/vector_value(v2))

def shortest_segment_point_segment(point,segment):
    if len(segment)>2:
        return shortest_segment_point_segment(point,divide_segment_into_points(segment))
    try:
        if len(point[0])>1:
            return shortest_segment_point_segment(segment,point)
    except:
        pass
    vect1 = segment[0] - point
    vect2 = segment[1] - point

    try:
        if cos_vect(vect1, segment[0]-segment[1]) <= 0:
            return ar([point,segment[0]])
        if cos_vect(vect2, segment[1]-segment[0]) <= 0:
            return ar([point,segment[1]])
    except:
        a = 9
    normal = compose_normal_line(compose_equation_line(segment),point)
    return ar([point,find_intersection(normal,compose_equation_line(segment))])



def scal_mult(v1,v2):
    return v1[0]*v2[0]+v2[1]*v1[1]

def distance_segment_point(segment,pointcoords):
    if len(pointcoords)>2:
        return distance_segment_point(pointcoords,segment)
    d = shortest_segment_point_segment(pointcoords,segment)
    return distance_point_point(d[0],d[1])

def projection_velocity_segment(v,segment):
    l = ar([segment[1][0]-segment[0][0],segment[1][1]-segment[0][1]])
    cos = cos_vect(v,l)
    return cos*vector_value(v)/vector_value(l)*l

    '''l = [segment[1][0]-segment[0][0],segment[1][1]-segment[0][1]]
    cos = vector_value(v)*vector_value(l)/(l[0]*v[1]+l[1]*v[0])
    endless_line = compose_equation_line(segment)
    a=endless_line[0]; b = endless_line[1]
    return ar([vector_value(v)*cos*b,vector_value(v)*a])'''


def distance_segment_segment(seg1coords,seg2coords):
    dpp = distance_point_point
    s1 = seg1coords; s2 = seg2coords
    if segments_have_intersection(s1,s2):
        return 0
    else:
        return min(dpp([s1[0],s[1]],[s2[0],s2[1]]), dpp([s1[0],s[1]],[s2[2],s2[3]]), dpp([s1[2],s[3]],[s2[0],s2[1]]), dpp([s1[2],s[3]],[s2[2],s2[3]]))

def line_to_segment(line):
    if line[1]>m_d:
        return [0,(-line[0]*0-line[2])/line[1],1000,(-line[0]*1000-line[2])/line[1]]
    else:
        return [-line[2]/line[0],0,-line[2]/line[0],1000]

def vector_x_direction(v):
    if v[0]<0:
        return -1
    elif v[0]>0:
        return 1
    else:
        return 0

def sign_of(x):
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0

def get_unary_vector(line,direction=1):
    l = line
    if l[0]==0:
        return ar([0,1])*direction
    if l[1]==0:
        return ar([1,0])*direction
    else:
        k = l[1]/l[0]
        x = (1/(1+1/k**2))**0.5
        return ar([x, -x/k]) * sign_of(x) * direction

def divide_segment_into_points(segment):
    if len(segment)==4:
        return ar([ar([segment[0],segment[1]]), ar( [ segment[2], segment[3] ]) ])
    else:
        return segment

def get_rebound_vector(v,segment,direction=1):
    return vector_value(v) * get_unary_vector(compose_normal_line(compose_equation_line(segment))) * direction

def edge_rebound_velocity(v,segment):
    if len(segment) > 2:
        return edge_rebound_velocity(v,divide_segment_into_points(segment))

    if segment[0][0]==segment[1][0]:
        return ar([-v[0],v[1]])
    if segment[0][1]==segment[1][1]:
        return ar([v[0],-v[1]])

    projv = projection_velocity_segment(v,segment)

    return 2*projv - v



    '''global m_d
    l = [segment[2]-segment[0],segment[3]-segment[1]]
    if abs(l[0])<m_d:
        return ar([-v[0],v[1]])
    if abs(l[1])<m_d:
        return ar([v[0],-v[1]])
    proj = projection_velocity_segment(v,segment)
    to_reflect = [v[0]-proj[0],v[1]-proj[1]]
    return ar([v[0]-to_reflect[0],v[1]-to_reflect[1]])'''

def ball_ball_rebound_velocity(ball1,ball2):
    center_line = ar([ball1.coords,ball2.coords])
    vprojection = projection_velocity_segment(ball2.v,center_line)
    m1 = ball1.mass; m2 = ball2.mass; v1 = ball1.v; v2 = vprojection#ball2.v
    return ((m1-m2)*v1 + 2*m2*v2)/(m1+m2)


def distance_between_objects(obj1,obj2):
    if obj1.type == 'ball' == obj2.type:
        return distance_point_point(obj1.coords,obj2.coords)-obj1.r-obj2.r
    elif obj1.type == 'ball' and obj2.type == 'edge':
        return distance_segment_point(obj2.coords,obj1.coords)-obj1.r
    elif obj2.type == 'skeleton' and obj1.type == 'ball':
        dist = list()
        for edge in obj2:
            dist.append(distance_segment_point(obj1.coords,edge.coords)-obj1.r)
        return min(dist)
    elif obj1.type == 'skeleton' and obj2.type == 'edge':
        distances = list()
        for edge in obj1:
            distances.append(distance_between_objects(edge,obj2))
        return min(distances)
    elif obj1.type == 'skeleton' == obj2.type:
        distances = list()
        for edge in obj1:
            distances.append(distance_between_objects(edge,obj2))
        return min(distances)
    elif obj1.type==obj2.type=="edge":
        return distance_segment_segment(obj1.coords,obj2.coords)
    else:
        return distance_between_objects(obj2,obj1)

def anomalistic(obj1,obj2,distance_between_objects_given=-1):
    if distance_between_objects_given>-1:
        return distance_between_objects_given<=-m_d
    return (distance_between_objects(obj1,obj2)<=-m_d)

def move_along_velocity(obj,distance):
    if vector_value(obj.v) > m_s:
        mult = distance/vector_value(obj.v)
        obj.move(mult*obj.v)
    else:
        obj.move(ar([0,distance]))

def get_away_direction(ball1,ball2):
    central_segment = ar( [ ball1.coords, ball2.coords ] )

    if ball1.coords[0]<ball2.coords[0]:
        direction = -1
    elif ball1.coords[0]>ball2.coords[0]:
        direction = 1
    elif ball1.coords[1]<ball2.coords[1]:
        direction = -1
    else:
        direction = 1

    return get_unary_vector(compose_equation_line(central_segment), direction)

def get_ball_edge_away_direction(ball,edge):
    ss = shortest_segment_point_segment(ball.coords,edge.coords)



def operate_anomaly(obj1,obj2,distance_between_objects_given=-1):
    if distance_between_objects_given != -1:
        dbo = distance_between_objects_given
    else:
        dbo = distance_between_objects(obj1,obj2)

    if obj1.type=='ball'==obj2.type:
        obj1_away_direction = get_away_direction(obj1,obj2)
        obj1.move(dbo*(-1)*obj1_away_direction)
        obj2.move(dbo*obj1_away_direction)
    elif obj1.type=='ball' and obj2.type=='edge':
        ss = shortest_segment_point_segment(obj2.coords, obj1.coords)
        obj1.move((ss[1]-ss[0])*dbo*0.05)
        #obj1.v *= 0.995
    else:
        operate_anomaly(obj2,obj1,distance_between_objects_given)

def obj_close(obj1,obj2,crit=10*m_d):
    pass

def invert_sincos(sincos):
    return (1-sincos**2)**0.5

def main():
    line = [200,180,160,140]
    print(compose_equation_line(line))
##    point = [180,140]
##    print(distance_line_point(line,point))
##    line = [-1/3,1,-1]
##    print(compose_normal_line(line,point))

if __name__ == '__main__':
    main()
