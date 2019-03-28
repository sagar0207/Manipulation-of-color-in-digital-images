import cv2
import numpy as np
import sys
import colorTransformation as ct
import math

if(len(sys.argv) != 7) :
    print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

w1 = float(sys.argv[1])
h1 = float(sys.argv[2])
w2 = float(sys.argv[3])
h2 = float(sys.argv[4])
name_input = sys.argv[5]
name_output = sys.argv[6]

if(w1<0 or h1<0 or w2<=w1 or h2<=h1 or w2>1 or h2>1) :
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
if(inputImage is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

cv2.imshow("input image: " + name_input, inputImage)
RGB_image1 = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
#cv2.imshow("BGRtoRGB", RGB_image1)
rows, cols, bands = inputImage.shape # bands == 3
print(rows, cols, bands)

W1 = round(w1*(cols-1))
H1 = round(h1*(rows-1))
W2 = round(w2*(cols-1))
H2 = round(h2*(rows-1))

# The transformation should be based on the
# historgram of the pixels in the W1,W2,H1,H2 range.
# The following code goes over these pixels

finalImage = np.copy(inputImage)
tmp = np.zeros([H2-H1+1, W2-W1+1, bands], dtype=np.float)

newdict = {}
print("RGB->Luv")
for i in range(H1, H2+1) :
    for j in range(W1, W2+1) :
        r, g, b = RGB_image1[i, j]
        print("Original RGB" , i,"," ,j)        
        print(r,g,b)
        #gray = round(0.3*r + 0.6*g + 0.1*b + 0.5)
        #tmp[i, j] = [gray, gray, gray]
        r, g, b = ct.convertToNonLinearRBG(r, g, b)
        print("Nonlinear RGB")
        print(r,g,b)
        r, g, b = ct.convertToLinearRBG(r, g, b)
        print("linear RGB")
        print(r,g,b)
        x, y, z = ct.convertToXYZ(r, g, b)
        print("XYZ")
        print(x, y, z)
        
        L, u, v = ct.convertToLuv(x, y, z)
        print(L, u, v,"->" ,tmp[i-H1,j-W1])
        tmp[i-H1,j-W1] = [L, u, v]
        print("LUV")
        print(L, u, v,"->" ,tmp[i-H1,j-W1])
        
        L = math.floor(L)
        if L not in newdict.keys():
            newdict[L] = 1
        else:
            newdict[L] += 1
        
newdict = dict(sorted(newdict.items()))
print(type(newdict))
for key,value in newdict.items():
    print(key, value)
    
histvalue = {}
histvalue = ct.hist_equ(newdict)
for key,value in histvalue.items():
    print(key, value)


print("--------------------")

for i in range(H1, H2+1) :
    for j in range(W1, W2+1) :
        L, u, v = tmp[i-H1,j-W1]
        print("Before Scaling")
        print(L, u, v)
        L1 = histvalue[math.floor(L)]
        #L1 = ct.scale_L(L, minimum, maximum)
        print("After histogram equalization ", i,"," ,j)
        print(L1, u, v)
        X, Y, Z = ct.convertLuvToXYZ(L1, u, v)
        print("LUV->XYZ")
        print(X, Y, Z)
        r, g, b = ct.convertXYZtoRGB(X, Y, Z)
        print("XYZ->RGB")
        print(r, g, b)
        r1, g1, b1 = ct.convertRBGtoNonlinear(r, g, b)
        print("RBG->non linear")
        print(r, g, b)
        r, g, b = ct.convertToColor(r1, g1, b1)
        print("FinalImage")
        print(r, g, b)
        finalImage[i,j] = [int(b), int(g), int(r)]
        tmp[i-H1,j-W1] = [b, g, r]
        
cv2.imshow('tmp', tmp)
cv2.imshow('finalImage', finalImage)

# end of example of going over window

outputImage = np.zeros([rows, cols, bands], dtype=np.uint8)

for i in range(0, rows) :
    for j in range(0, cols) :
        b, g, r = finalImage[i, j]
        outputImage[i,j] = [b, g, r]
cv2.imshow("output:", outputImage)
cv2.imwrite(name_output, outputImage);


# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
