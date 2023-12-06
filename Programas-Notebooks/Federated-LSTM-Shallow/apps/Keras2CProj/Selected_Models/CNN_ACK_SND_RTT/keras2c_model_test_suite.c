#include <stdio.h> 
#include <math.h> 
#include <time.h> 
#include "./include/k2c_include.h" 
#include "keras2c_model.h" 

float maxabs(k2c_tensor *tensor1, k2c_tensor *tensor2);
struct timeval GetTimeStamp(); 
 
float test1_conv2d_2_input_1_input_array[9] = {
-1.45161142e+00f,+4.23019589e-01f,-1.69028777e+00f,-1.91388825e+00f,+1.37099029e+00f,
+1.53689883e+00f,+1.17184826e+00f,-1.82662693e+00f,-1.24438418e+00f,}; 
k2c_tensor test1_conv2d_2_input_1_input = {&test1_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test1_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test1 = {&keras_dense_5_1_test1_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test1_array[1] = {0}; 
k2c_tensor c_dense_5_1_test1 = {&c_dense_5_1_test1_array[0],1,1,{1,1,1,1,1}}; 
float test2_conv2d_2_input_1_input_array[9] = {
+4.08876700e-01f,+4.74917558e-01f,+1.17200325e+00f,+1.69190025e+00f,+1.77446811e+00f,
+3.35741727e-01f,-1.57664563e+00f,-1.72347305e+00f,-1.84434222e+00f,}; 
k2c_tensor test2_conv2d_2_input_1_input = {&test2_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test2_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test2 = {&keras_dense_5_1_test2_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test2_array[1] = {0}; 
k2c_tensor c_dense_5_1_test2 = {&c_dense_5_1_test2_array[0],1,1,{1,1,1,1,1}}; 
float test3_conv2d_2_input_1_input_array[9] = {
+8.61751636e-01f,+1.72719308e+00f,+9.63049281e-01f,+1.40552991e+00f,+1.68393183e+00f,
-1.37786412e-01f,-1.72687385e+00f,-1.71441995e+00f,+1.21537207e+00f,}; 
k2c_tensor test3_conv2d_2_input_1_input = {&test3_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test3_array[1] = {
+9.99999523e-01f,}; 
k2c_tensor keras_dense_5_1_test3 = {&keras_dense_5_1_test3_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test3_array[1] = {0}; 
k2c_tensor c_dense_5_1_test3 = {&c_dense_5_1_test3_array[0],1,1,{1,1,1,1,1}}; 
float test4_conv2d_2_input_1_input_array[9] = {
-5.91565820e-01f,-9.62186639e-01f,-2.74350508e-01f,+6.58597175e-01f,+3.08380537e-01f,
-1.04760986e+00f,+3.11025087e-01f,+7.70856843e-03f,-1.66826164e+00f,}; 
k2c_tensor test4_conv2d_2_input_1_input = {&test4_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test4_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test4 = {&keras_dense_5_1_test4_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test4_array[1] = {0}; 
k2c_tensor c_dense_5_1_test4 = {&c_dense_5_1_test4_array[0],1,1,{1,1,1,1,1}}; 
float test5_conv2d_2_input_1_input_array[9] = {
+1.30534366e+00f,-1.91549262e-01f,-1.83054249e+00f,-1.03473515e+00f,+1.50396088e+00f,
-7.03569631e-01f,+4.38279934e-01f,-2.82820500e-01f,-1.77526135e+00f,}; 
k2c_tensor test5_conv2d_2_input_1_input = {&test5_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test5_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test5 = {&keras_dense_5_1_test5_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test5_array[1] = {0}; 
k2c_tensor c_dense_5_1_test5 = {&c_dense_5_1_test5_array[0],1,1,{1,1,1,1,1}}; 
float test6_conv2d_2_input_1_input_array[9] = {
-1.83568077e-01f,-3.19003317e-02f,-2.53309261e-01f,-1.87145146e+00f,-4.32002475e-01f,
-1.99516482e+00f,+1.59642361e+00f,+1.84645194e+00f,-1.64380745e+00f,}; 
k2c_tensor test6_conv2d_2_input_1_input = {&test6_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test6_array[1] = {
+9.65697587e-01f,}; 
k2c_tensor keras_dense_5_1_test6 = {&keras_dense_5_1_test6_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test6_array[1] = {0}; 
k2c_tensor c_dense_5_1_test6 = {&c_dense_5_1_test6_array[0],1,1,{1,1,1,1,1}}; 
float test7_conv2d_2_input_1_input_array[9] = {
+7.41522519e-01f,-1.55039246e+00f,+2.47631734e-01f,-1.28602883e+00f,+9.79986144e-01f,
+1.26127326e+00f,-1.86309847e+00f,-7.17268085e-01f,-6.08272527e-01f,}; 
k2c_tensor test7_conv2d_2_input_1_input = {&test7_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test7_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test7 = {&keras_dense_5_1_test7_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test7_array[1] = {0}; 
k2c_tensor c_dense_5_1_test7 = {&c_dense_5_1_test7_array[0],1,1,{1,1,1,1,1}}; 
float test8_conv2d_2_input_1_input_array[9] = {
-1.37287818e+00f,+1.38909535e+00f,+1.86047367e+00f,+1.90383017e+00f,+6.61573968e-01f,
-1.27924717e+00f,-6.19807301e-01f,-9.26787982e-02f,+7.32122866e-02f,}; 
k2c_tensor test8_conv2d_2_input_1_input = {&test8_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test8_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test8 = {&keras_dense_5_1_test8_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test8_array[1] = {0}; 
k2c_tensor c_dense_5_1_test8 = {&c_dense_5_1_test8_array[0],1,1,{1,1,1,1,1}}; 
float test9_conv2d_2_input_1_input_array[9] = {
+9.24965584e-01f,-1.90500755e-02f,+6.87442237e-01f,+9.87652134e-01f,+1.95938237e+00f,
-1.62347895e+00f,+1.07930948e+00f,-9.93530086e-01f,+1.79416675e+00f,}; 
k2c_tensor test9_conv2d_2_input_1_input = {&test9_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test9_array[1] = {
+1.00000000e+00f,}; 
k2c_tensor keras_dense_5_1_test9 = {&keras_dense_5_1_test9_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test9_array[1] = {0}; 
k2c_tensor c_dense_5_1_test9 = {&c_dense_5_1_test9_array[0],1,1,{1,1,1,1,1}}; 
float test10_conv2d_2_input_1_input_array[9] = {
+1.94318517e+00f,-2.00516410e-01f,+1.72288692e+00f,+1.29957070e-01f,-1.65559306e+00f,
+1.27601055e+00f,-1.49723119e-01f,+4.56507434e-01f,-2.06763939e-01f,}; 
k2c_tensor test10_conv2d_2_input_1_input = {&test10_conv2d_2_input_1_input_array[0],3,9,{3,3,1,1,1}}; 
float keras_dense_5_1_test10_array[1] = {0}; 
k2c_tensor keras_dense_5_1_test10 = {&keras_dense_5_1_test10_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_1_test10_array[1] = {0}; 
k2c_tensor c_dense_5_1_test10 = {&c_dense_5_1_test10_array[0],1,1,{1,1,1,1,1}}; 
int main(){
 float errors[10];
 size_t num_tests = 10; 
size_t num_outputs = 1; 
keras2c_model_initialize(); 
clock_t t0 = clock(); 
keras2c_model(&test1_conv2d_2_input_1_input,&c_dense_5_1_test1); 
keras2c_model(&test2_conv2d_2_input_1_input,&c_dense_5_1_test2); 
keras2c_model(&test3_conv2d_2_input_1_input,&c_dense_5_1_test3); 
keras2c_model(&test4_conv2d_2_input_1_input,&c_dense_5_1_test4); 
keras2c_model(&test5_conv2d_2_input_1_input,&c_dense_5_1_test5); 
keras2c_model(&test6_conv2d_2_input_1_input,&c_dense_5_1_test6); 
keras2c_model(&test7_conv2d_2_input_1_input,&c_dense_5_1_test7); 
keras2c_model(&test8_conv2d_2_input_1_input,&c_dense_5_1_test8); 
keras2c_model(&test9_conv2d_2_input_1_input,&c_dense_5_1_test9); 
keras2c_model(&test10_conv2d_2_input_1_input,&c_dense_5_1_test10); 

clock_t t1 = clock(); 
printf("Average time over 10 tests: %e s \n", 
 ((double)t1-t0)/(double)CLOCKS_PER_SEC/(double)10); 
errors[0] = maxabs(&keras_dense_5_1_test1,&c_dense_5_1_test1); 
errors[1] = maxabs(&keras_dense_5_1_test2,&c_dense_5_1_test2); 
errors[2] = maxabs(&keras_dense_5_1_test3,&c_dense_5_1_test3); 
errors[3] = maxabs(&keras_dense_5_1_test4,&c_dense_5_1_test4); 
errors[4] = maxabs(&keras_dense_5_1_test5,&c_dense_5_1_test5); 
errors[5] = maxabs(&keras_dense_5_1_test6,&c_dense_5_1_test6); 
errors[6] = maxabs(&keras_dense_5_1_test7,&c_dense_5_1_test7); 
errors[7] = maxabs(&keras_dense_5_1_test8,&c_dense_5_1_test8); 
errors[8] = maxabs(&keras_dense_5_1_test9,&c_dense_5_1_test9); 
errors[9] = maxabs(&keras_dense_5_1_test10,&c_dense_5_1_test10); 
float maxerror = errors[0]; 
for(size_t i=1; i< num_tests*num_outputs;i++){ 
if (errors[i] > maxerror) { 
maxerror = errors[i];}} 
printf("Max absolute error for 10 tests: %e \n", maxerror);
keras2c_model_terminate(); 
if (maxerror > 1e-05) { 
return 1;} 
return 0;
} 

float maxabs(k2c_tensor *tensor1, k2c_tensor *tensor2){ 

    float x = 0; 

    float y = 0; 

    for(size_t i=0; i<tensor1->numel; i++){

    y = fabsf(tensor1->array[i]-tensor2->array[i]);
    if (y>x) {x=y;}}
    return x;}

