import cv2
import math

def convertToNonLinearRBG(r, g, b):
    return r/255, g/255, b/255;


def inverseGamma(color):
    if(color<0.03928):
        return color/12.92;
    else:
        return math.pow(((color+0.055)/1.055),2.4);

def convertToLinearRBG(r, g, b):
    return inverseGamma(r), inverseGamma(g), inverseGamma(b);

def convertToXYZ(r, g, b):
    x = 0.412453*r + 0.35758*g + 0.180423*b
    y = 0.212671*r + 0.71516*g + 0.072169*b
    z = 0.019334*r + 0.119193*g + 0.950227*b
    return x, y, z;

def convertToLuv(x, y, z):
    # Considering D65 is used for white with y_w = 1 we have:(x_w, y_w, z_w) = (0.95,1.0,1.09) 
    u_w = 0.1977
    v_w = 0.4682
    t = y/1  #here y_w = 1
    if(t>0.008856):
        L = 116*(math.pow(t,(1/3))) - 16
    else:
        L = t*903.3
    if x == 0 and y == 0 and z == 0:
        return L, 13*L*-1*u_w, 13*L*-1*v_w
    d = x + 15*y + 3*z
    u1 = (4*x)/d
    v1 = (9*y)/d
    u = 13*L*(u1-u_w)
    v = 13*L*(v1-v_w)
    return L, u, v;
    
def convertxyYtoXYZ(x, y, Y):
    if(y==0):
        return 0, Y, 0;
    return (x*Y)/y, Y, ((1-x-y)*Y)/y;

def scale_L(L, a, b):
    return ((L-a)/(b-a))*(100.0);   # Considering the range for scaling (0,100)

def scale_Y(Y, a, b):
    return ((Y-a)/(b-a))*(1.0);

def convertLuvToXYZ(L, u, v):
    u_w = 0.1977
    v_w = 0.4682
    if(L==0):
        return 0, 0, 0;
    u1 = (u + 13*u_w*L)/(13*L)
    v1 = (v + 13*v_w*L)/(13*L)
    if(L>7.9996):
        Y = math.pow((L+16)/116,3)*1
    else:
        Y = L/903.3
    if(v1 == 0):
        X = 0
        Z = 0
    else:
        X = (Y*2.25*u1)/v1
        Z = (Y*(3 - 0.75*u1 - 5*v1))/v1
    return X, Y, Z;


def convertXYZtoRGB(X, Y, Z):
    r = 3.240479*X - 1.53715*Y - 0.498535*Z
    g = 1.875991*Y - 0.969256*X + 0.041556*Z
    b = 0.55648*X - 0.204043*Y + 1.057311*Z
    if(r > 1):
        r = 1
    if(r < 0):
        r = 0
    if(g > 1):
        g = 1
    if(g < 0):
        g = 0
    if(b > 1):
        b = 1
    if(b < 0):
        b = 0 
    return r, g, b;

def gamma(color):
    if(color < 0.00304):
        return 12.92*color;
    else:
        return (1.055*math.pow(color, (1/2.4))) - 0.055;

def convertRBGtoNonlinear(r, g, b):
    return gamma(r), gamma(g), gamma(b);

def convertToColor(r, g, b):
    return r*255, g*255, b*255;
    
def convertXYZtoxyY(x, y, z):
    if x == 0 and y == 0 and z == 0:
        return 0 , 0, 0;
    return (x/(x+y+z)), (y/(x+y+z)), y;


def hist_equ(newdict):
    floor_values = {}
    sum = 0
    sum_values = {}
    for key, value in newdict.items():
        sum = sum + newdict[key] 
        sum_values[key] = sum
        #print(sum)
    for key, value in sum_values.items():
        if key - 1 in sum_values.keys():
            k = ((sum_values[key-1] + sum_values[key])*101)/(2*sum)
            k = math.floor(k)
            floor_values[key] = k
        else:
            k = (sum_values[key]*101)/(2*sum)
            k = math.floor(k)
            floor_values[key] = k
            
    return floor_values