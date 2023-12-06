#include <stdio.h> 
#include <math.h> 
#include <time.h> 
#include "./include/k2c_include.h" 
#include "keras2c_model.h" 

float maxabs(k2c_tensor *tensor1, k2c_tensor *tensor2);
struct timeval GetTimeStamp(); 
 
float test1_conv2d_2_input_input_array[6] = {
-2.88279892e-02f,-1.24774077e+00f,+1.77777383e+00f,-5.26989686e-01f,+6.28295032e-01f,
+6.60732552e-01f,}; 
k2c_tensor test1_conv2d_2_input_input = {&test1_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test1_array[1] = {
+2.06983042e-11f,}; 
k2c_tensor keras_dense_5_test1 = {&keras_dense_5_test1_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test1_array[1] = {0}; 
k2c_tensor c_dense_5_test1 = {&c_dense_5_test1_array[0],1,1,{1,1,1,1,1}}; 
float test2_conv2d_2_input_input_array[6] = {
+4.07935710e-01f,-1.06603760e+00f,+5.07932430e-01f,-1.39297120e+00f,-3.24112686e-01f,
-5.46597945e-01f,}; 
k2c_tensor test2_conv2d_2_input_input = {&test2_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test2_array[1] = {0}; 
k2c_tensor keras_dense_5_test2 = {&keras_dense_5_test2_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test2_array[1] = {0}; 
k2c_tensor c_dense_5_test2 = {&c_dense_5_test2_array[0],1,1,{1,1,1,1,1}}; 
float test3_conv2d_2_input_input_array[6] = {
-4.40866638e-01f,+1.08707466e+00f,+1.06668863e+00f,-9.15273340e-01f,-6.91288249e-01f,
+1.63115261e+00f,}; 
k2c_tensor test3_conv2d_2_input_input = {&test3_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test3_array[1] = {
+1.43035864e-02f,}; 
k2c_tensor keras_dense_5_test3 = {&keras_dense_5_test3_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test3_array[1] = {0}; 
k2c_tensor c_dense_5_test3 = {&c_dense_5_test3_array[0],1,1,{1,1,1,1,1}}; 
float test4_conv2d_2_input_input_array[6] = {
-1.45712368e+00f,-1.17529280e+00f,+1.20599601e+00f,+1.72215835e+00f,-1.23208151e+00f,
+1.55309134e+00f,}; 
k2c_tensor test4_conv2d_2_input_input = {&test4_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test4_array[1] = {
+1.10540465e-02f,}; 
k2c_tensor keras_dense_5_test4 = {&keras_dense_5_test4_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test4_array[1] = {0}; 
k2c_tensor c_dense_5_test4 = {&c_dense_5_test4_array[0],1,1,{1,1,1,1,1}}; 
float test5_conv2d_2_input_input_array[6] = {
-1.93937946e+00f,+1.31637813e+00f,+7.57149716e-01f,-2.86961983e-01f,-1.26707135e+00f,
+3.03446880e-01f,}; 
k2c_tensor test5_conv2d_2_input_input = {&test5_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test5_array[1] = {0}; 
k2c_tensor keras_dense_5_test5 = {&keras_dense_5_test5_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test5_array[1] = {0}; 
k2c_tensor c_dense_5_test5 = {&c_dense_5_test5_array[0],1,1,{1,1,1,1,1}}; 
float test6_conv2d_2_input_input_array[6] = {
-1.19137764e-01f,-1.20327098e+00f,-9.64329819e-01f,+1.17766386e+00f,-1.86144664e+00f,
+1.85580602e+00f,}; 
k2c_tensor test6_conv2d_2_input_input = {&test6_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test6_array[1] = {
+4.28140891e-04f,}; 
k2c_tensor keras_dense_5_test6 = {&keras_dense_5_test6_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test6_array[1] = {0}; 
k2c_tensor c_dense_5_test6 = {&c_dense_5_test6_array[0],1,1,{1,1,1,1,1}}; 
float test7_conv2d_2_input_input_array[6] = {
+2.98097215e-01f,-6.07658169e-01f,-6.52279187e-01f,+1.24953086e+00f,-1.96114166e+00f,
-1.86782254e+00f,}; 
k2c_tensor test7_conv2d_2_input_input = {&test7_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test7_array[1] = {0}; 
k2c_tensor keras_dense_5_test7 = {&keras_dense_5_test7_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test7_array[1] = {0}; 
k2c_tensor c_dense_5_test7 = {&c_dense_5_test7_array[0],1,1,{1,1,1,1,1}}; 
float test8_conv2d_2_input_input_array[6] = {
+1.66796861e+00f,-6.75623097e-01f,-7.25481381e-01f,+1.78728106e+00f,+1.87666960e+00f,
+1.26147223e+00f,}; 
k2c_tensor test8_conv2d_2_input_input = {&test8_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test8_array[1] = {
+1.48088380e-03f,}; 
k2c_tensor keras_dense_5_test8 = {&keras_dense_5_test8_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test8_array[1] = {0}; 
k2c_tensor c_dense_5_test8 = {&c_dense_5_test8_array[0],1,1,{1,1,1,1,1}}; 
float test9_conv2d_2_input_input_array[6] = {
-8.92853720e-01f,+4.03513971e-01f,-7.37970730e-01f,-1.86415715e+00f,-4.82378081e-01f,
+3.45822490e-01f,}; 
k2c_tensor test9_conv2d_2_input_input = {&test9_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test9_array[1] = {0}; 
k2c_tensor keras_dense_5_test9 = {&keras_dense_5_test9_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test9_array[1] = {0}; 
k2c_tensor c_dense_5_test9 = {&c_dense_5_test9_array[0],1,1,{1,1,1,1,1}}; 
float test10_conv2d_2_input_input_array[6] = {
-7.26600479e-01f,-9.04715090e-01f,+1.21243985e+00f,+6.07914466e-02f,+1.19333494e+00f,
+1.75927831e+00f,}; 
k2c_tensor test10_conv2d_2_input_input = {&test10_conv2d_2_input_input_array[0],3,6,{3,2,1,1,1}}; 
float keras_dense_5_test10_array[1] = {
+2.94746278e-04f,}; 
k2c_tensor keras_dense_5_test10 = {&keras_dense_5_test10_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_5_test10_array[1] = {0}; 
k2c_tensor c_dense_5_test10 = {&c_dense_5_test10_array[0],1,1,{1,1,1,1,1}}; 
int main(){
 float errors[10];
 size_t num_tests = 10; 
size_t num_outputs = 1; 
keras2c_model_initialize(); 
clock_t t0 = clock(); 
keras2c_model(&test1_conv2d_2_input_input,&c_dense_5_test1); 
keras2c_model(&test2_conv2d_2_input_input,&c_dense_5_test2); 
keras2c_model(&test3_conv2d_2_input_input,&c_dense_5_test3); 
keras2c_model(&test4_conv2d_2_input_input,&c_dense_5_test4); 
keras2c_model(&test5_conv2d_2_input_input,&c_dense_5_test5); 
keras2c_model(&test6_conv2d_2_input_input,&c_dense_5_test6); 
keras2c_model(&test7_conv2d_2_input_input,&c_dense_5_test7); 
keras2c_model(&test8_conv2d_2_input_input,&c_dense_5_test8); 
keras2c_model(&test9_conv2d_2_input_input,&c_dense_5_test9); 
keras2c_model(&test10_conv2d_2_input_input,&c_dense_5_test10); 

clock_t t1 = clock(); 
printf("Average time over 10 tests: %e s \n", 
 ((double)t1-t0)/(double)CLOCKS_PER_SEC/(double)10); 
errors[0] = maxabs(&keras_dense_5_test1,&c_dense_5_test1); 
errors[1] = maxabs(&keras_dense_5_test2,&c_dense_5_test2); 
errors[2] = maxabs(&keras_dense_5_test3,&c_dense_5_test3); 
errors[3] = maxabs(&keras_dense_5_test4,&c_dense_5_test4); 
errors[4] = maxabs(&keras_dense_5_test5,&c_dense_5_test5); 
errors[5] = maxabs(&keras_dense_5_test6,&c_dense_5_test6); 
errors[6] = maxabs(&keras_dense_5_test7,&c_dense_5_test7); 
errors[7] = maxabs(&keras_dense_5_test8,&c_dense_5_test8); 
errors[8] = maxabs(&keras_dense_5_test9,&c_dense_5_test9); 
errors[9] = maxabs(&keras_dense_5_test10,&c_dense_5_test10); 
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

