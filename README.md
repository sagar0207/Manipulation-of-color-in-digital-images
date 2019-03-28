# Manipulation of color in digital images

## Description
This project deals with the linear stretching in the Luv domain, histogram equalization and linear stretching in xyY domain of the images from a particular window of the image.
It contains three programs:
1.	A program that gets as input a colour image, performs linear scaling in the Luv domain in the specified window, and writes the scaled image as output. The scaling is applied only on luminance values with range 0 to 100.
2.	Histogram Equalization in Luv applied to the luminance values, as computed in the specified window. Performing discretization step, where the real-valued L is discretized into 101 values.
3.	A program that gets as input a colour image, performs linear scaling in the xyY domain in the specified window, and writes the scaled image as output. The scaling is applied only on luminance value Y with range 0 to 1.

## Command execution
Instructions for running the code: Navigate to the folder containing the code files and from the cmd/ terminal, type (for example):
For Program 1: python proj1_q1.py 0.3 0.3 0.7 0.7 good-test-image-for-proj1.bmp result1.jpg 
For Program 2: python proj1_q2.py 0.3 0.3 0.7 0.7 good-test-image-for-proj1.bmp result2.jpg
For Program 3: python proj1_q3.py 0.3 0.3 0.7 0.7 good-test-image-for-proj1.bmp result3.jpg
All the values of w1, w2, h1, h2 must be between 0 and 1.

## Assumption and criteria decision
1.	Input RGB out of [0,255] truncate to [0,1] by dividing it every value by 255.  
2.	For converting values to XYZ domain from xyY domain, when y = 0 return X = Z = 0 and Y = Y.
3.	For converting values to XYZ domain from Luv domain, when v’ = 0 return X=Z=0
4.	Cliff values into 0 and 1 if r, g, b values are less than 0 or more than 1 while performing XYZ to RGB.
5.	adjusted L = 0 (new L = 0) return all values 0 (Original: u__ = (u + 13uwnL) / (13nL) and v__ = (v + 13vwnL) / (13nL) )
6.	Output RGB out of [0,1] to range [0,255] by multiplying it by 255.
7.	All the assumptions are made so that no transformation will occur NaN values.

## Results
According to my results obtained by applying linear scaling and histogram equalization in Luv domain, Linear scaling is more likely to produce better image than Histogram Equalization. Histogram Equalization tends to spread the histogram out, which in cases where the image having white level of black pixel will be boost and will make the image grainier. 
In program 1, applying linear scaling on luminance in Luv domain made the output image brighter and sharper, exposing the edges of original image. While the output of program 2 after applying histogram Equalization made the result more exposed i.e. whose pixels having bright area turned out to be more very dark and pixels having dark area turned out to be very bright.	

## Questions
### How did I handle the divide by zero situations ? 
Ans. In such situations, I pre-assigned them to 0, and then reassigned them by putting the condition that if the denominator is not 0, then it will perform the original formula’s for transformations.
### Situations where the image looked bad ? 
Ans. I usually tried the window 0.3 0.3 0.7 0.7, which was mostly the centre of the image. However, when I made the entire image as a window, i.e. 0 0 1 1, the colour of the output image became quite clear, But, according to me, it made the image quite sharp with distinct borders.
