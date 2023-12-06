#include <stdio.h> 
#include <math.h> 
#include <time.h> 
#include "./include/k2c_include.h" 
#include "keras2c_model.h" 

float maxabs(k2c_tensor *tensor1, k2c_tensor *tensor2);
struct timeval GetTimeStamp(); 
 
float test1_dense_8_input_input_array[2] = {
+1.94286746e-01f,-1.48177682e+00f,}; 
k2c_tensor test1_dense_8_input_input = {&test1_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test1_array[1] = {0}; 
k2c_tensor keras_dense_11_test1 = {&keras_dense_11_test1_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test1_array[1] = {0}; 
k2c_tensor c_dense_11_test1 = {&c_dense_11_test1_array[0],1,1,{1,1,1,1,1}}; 
float test2_dense_8_input_input_array[2] = {
+1.44148281e+00f,-1.70337838e+00f,}; 
k2c_tensor test2_dense_8_input_input = {&test2_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test2_array[1] = {0}; 
k2c_tensor keras_dense_11_test2 = {&keras_dense_11_test2_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test2_array[1] = {0}; 
k2c_tensor c_dense_11_test2 = {&c_dense_11_test2_array[0],1,1,{1,1,1,1,1}}; 
float test3_dense_8_input_input_array[2] = {
-3.07671661e-01f,+1.95906149e+00f,}; 
k2c_tensor test3_dense_8_input_input = {&test3_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test3_array[1] = {
+9.99998510e-01f,}; 
k2c_tensor keras_dense_11_test3 = {&keras_dense_11_test3_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test3_array[1] = {0}; 
k2c_tensor c_dense_11_test3 = {&c_dense_11_test3_array[0],1,1,{1,1,1,1,1}}; 
float test4_dense_8_input_input_array[2] = {
+1.95568878e+00f,-1.75498954e+00f,}; 
k2c_tensor test4_dense_8_input_input = {&test4_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test4_array[1] = {0}; 
k2c_tensor keras_dense_11_test4 = {&keras_dense_11_test4_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test4_array[1] = {0}; 
k2c_tensor c_dense_11_test4 = {&c_dense_11_test4_array[0],1,1,{1,1,1,1,1}}; 
float test5_dense_8_input_input_array[2] = {
-1.60390435e+00f,+1.70968408e+00f,}; 
k2c_tensor test5_dense_8_input_input = {&test5_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test5_array[1] = {
+9.99998033e-01f,}; 
k2c_tensor keras_dense_11_test5 = {&keras_dense_11_test5_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test5_array[1] = {0}; 
k2c_tensor c_dense_11_test5 = {&c_dense_11_test5_array[0],1,1,{1,1,1,1,1}}; 
float test6_dense_8_input_input_array[2] = {
+1.59842408e+00f,+1.46053775e+00f,}; 
k2c_tensor test6_dense_8_input_input = {&test6_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test6_array[1] = {
+8.90848160e-01f,}; 
k2c_tensor keras_dense_11_test6 = {&keras_dense_11_test6_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test6_array[1] = {0}; 
k2c_tensor c_dense_11_test6 = {&c_dense_11_test6_array[0],1,1,{1,1,1,1,1}}; 
float test7_dense_8_input_input_array[2] = {
+7.85794483e-01f,+1.98119404e+00f,}; 
k2c_tensor test7_dense_8_input_input = {&test7_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test7_array[1] = {
+9.99907136e-01f,}; 
k2c_tensor keras_dense_11_test7 = {&keras_dense_11_test7_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test7_array[1] = {0}; 
k2c_tensor c_dense_11_test7 = {&c_dense_11_test7_array[0],1,1,{1,1,1,1,1}}; 
float test8_dense_8_input_input_array[2] = {
-1.21270883e+00f,+6.74770568e-01f,}; 
k2c_tensor test8_dense_8_input_input = {&test8_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test8_array[1] = {
+7.03608721e-14f,}; 
k2c_tensor keras_dense_11_test8 = {&keras_dense_11_test8_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test8_array[1] = {0}; 
k2c_tensor c_dense_11_test8 = {&c_dense_11_test8_array[0],1,1,{1,1,1,1,1}}; 
float test9_dense_8_input_input_array[2] = {
+1.79625448e+00f,-3.63862853e-01f,}; 
k2c_tensor test9_dense_8_input_input = {&test9_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test9_array[1] = {0}; 
k2c_tensor keras_dense_11_test9 = {&keras_dense_11_test9_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test9_array[1] = {0}; 
k2c_tensor c_dense_11_test9 = {&c_dense_11_test9_array[0],1,1,{1,1,1,1,1}}; 
float test10_dense_8_input_input_array[2] = {
+4.17881536e-01f,-9.62245183e-01f,}; 
k2c_tensor test10_dense_8_input_input = {&test10_dense_8_input_input_array[0],1,2,{2,1,1,1,1}}; 
float keras_dense_11_test10_array[1] = {0}; 
k2c_tensor keras_dense_11_test10 = {&keras_dense_11_test10_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_11_test10_array[1] = {0}; 
k2c_tensor c_dense_11_test10 = {&c_dense_11_test10_array[0],1,1,{1,1,1,1,1}}; 
int main(){
 float errors[10];
 size_t num_tests = 10; 
size_t num_outputs = 1; 
keras2c_model_initialize(); 
clock_t t0 = clock(); 
keras2c_model(&test1_dense_8_input_input,&c_dense_11_test1); 
keras2c_model(&test2_dense_8_input_input,&c_dense_11_test2); 
keras2c_model(&test3_dense_8_input_input,&c_dense_11_test3); 
keras2c_model(&test4_dense_8_input_input,&c_dense_11_test4); 
keras2c_model(&test5_dense_8_input_input,&c_dense_11_test5); 
keras2c_model(&test6_dense_8_input_input,&c_dense_11_test6); 
keras2c_model(&test7_dense_8_input_input,&c_dense_11_test7); 
keras2c_model(&test8_dense_8_input_input,&c_dense_11_test8); 
keras2c_model(&test9_dense_8_input_input,&c_dense_11_test9); 
keras2c_model(&test10_dense_8_input_input,&c_dense_11_test10); 

clock_t t1 = clock(); 
printf("Average time over 10 tests: %e s \n", 
 ((double)t1-t0)/(double)CLOCKS_PER_SEC/(double)10); 
errors[0] = maxabs(&keras_dense_11_test1,&c_dense_11_test1); 
errors[1] = maxabs(&keras_dense_11_test2,&c_dense_11_test2); 
errors[2] = maxabs(&keras_dense_11_test3,&c_dense_11_test3); 
errors[3] = maxabs(&keras_dense_11_test4,&c_dense_11_test4); 
errors[4] = maxabs(&keras_dense_11_test5,&c_dense_11_test5); 
errors[5] = maxabs(&keras_dense_11_test6,&c_dense_11_test6); 
errors[6] = maxabs(&keras_dense_11_test7,&c_dense_11_test7); 
errors[7] = maxabs(&keras_dense_11_test8,&c_dense_11_test8); 
errors[8] = maxabs(&keras_dense_11_test9,&c_dense_11_test9); 
errors[9] = maxabs(&keras_dense_11_test10,&c_dense_11_test10); 
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

