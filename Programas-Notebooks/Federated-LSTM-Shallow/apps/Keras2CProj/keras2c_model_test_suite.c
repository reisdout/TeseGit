#include <stdio.h> 
#include <math.h> 
#include <time.h> 
#include "./include/k2c_include.h" 
#include "keras2c_model.h" 

float maxabs(k2c_tensor *tensor1, k2c_tensor *tensor2);
struct timeval GetTimeStamp(); 
 
float test1_dense_68_input_1_input_array[3] = {
+4.51775948e-01f,-3.56429958e-01f,+9.93329312e-01f,}; 
k2c_tensor test1_dense_68_input_1_input = {&test1_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test1_array[1] = {
+9.48265851e-01f,}; 
k2c_tensor keras_dense_70_1_test1 = {&keras_dense_70_1_test1_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test1_array[1] = {0}; 
k2c_tensor c_dense_70_1_test1 = {&c_dense_70_1_test1_array[0],1,1,{1,1,1,1,1}}; 
float test2_dense_68_input_1_input_array[3] = {
+1.90931978e+00f,+1.14131751e+00f,-1.23901988e+00f,}; 
k2c_tensor test2_dense_68_input_1_input = {&test2_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test2_array[1] = {0}; 
k2c_tensor keras_dense_70_1_test2 = {&keras_dense_70_1_test2_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test2_array[1] = {0}; 
k2c_tensor c_dense_70_1_test2 = {&c_dense_70_1_test2_array[0],1,1,{1,1,1,1,1}}; 
float test3_dense_68_input_1_input_array[3] = {
-1.83673505e+00f,+1.30552177e-01f,-1.04633697e-01f,}; 
k2c_tensor test3_dense_68_input_1_input = {&test3_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test3_array[1] = {
+6.63303079e-10f,}; 
k2c_tensor keras_dense_70_1_test3 = {&keras_dense_70_1_test3_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test3_array[1] = {0}; 
k2c_tensor c_dense_70_1_test3 = {&c_dense_70_1_test3_array[0],1,1,{1,1,1,1,1}}; 
float test4_dense_68_input_1_input_array[3] = {
-1.39397882e+00f,+7.00228111e-01f,-5.42151881e-01f,}; 
k2c_tensor test4_dense_68_input_1_input = {&test4_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test4_array[1] = {
+3.42496248e-15f,}; 
k2c_tensor keras_dense_70_1_test4 = {&keras_dense_70_1_test4_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test4_array[1] = {0}; 
k2c_tensor c_dense_70_1_test4 = {&c_dense_70_1_test4_array[0],1,1,{1,1,1,1,1}}; 
float test5_dense_68_input_1_input_array[3] = {
+6.25895789e-01f,-1.38190018e+00f,+1.26922591e+00f,}; 
k2c_tensor test5_dense_68_input_1_input = {&test5_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test5_array[1] = {
+9.99982953e-01f,}; 
k2c_tensor keras_dense_70_1_test5 = {&keras_dense_70_1_test5_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test5_array[1] = {0}; 
k2c_tensor c_dense_70_1_test5 = {&c_dense_70_1_test5_array[0],1,1,{1,1,1,1,1}}; 
float test6_dense_68_input_1_input_array[3] = {
+1.72473736e+00f,+1.98136322e+00f,-1.50407235e+00f,}; 
k2c_tensor test6_dense_68_input_1_input = {&test6_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test6_array[1] = {0}; 
k2c_tensor keras_dense_70_1_test6 = {&keras_dense_70_1_test6_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test6_array[1] = {0}; 
k2c_tensor c_dense_70_1_test6 = {&c_dense_70_1_test6_array[0],1,1,{1,1,1,1,1}}; 
float test7_dense_68_input_1_input_array[3] = {
-1.22306879e+00f,-3.00461227e-02f,+3.57808545e-01f,}; 
k2c_tensor test7_dense_68_input_1_input = {&test7_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test7_array[1] = {
+2.73886212e-06f,}; 
k2c_tensor keras_dense_70_1_test7 = {&keras_dense_70_1_test7_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test7_array[1] = {0}; 
k2c_tensor c_dense_70_1_test7 = {&c_dense_70_1_test7_array[0],1,1,{1,1,1,1,1}}; 
float test8_dense_68_input_1_input_array[3] = {
-1.73667832e-01f,-8.72971352e-01f,-7.88588221e-01f,}; 
k2c_tensor test8_dense_68_input_1_input = {&test8_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test8_array[1] = {0}; 
k2c_tensor keras_dense_70_1_test8 = {&keras_dense_70_1_test8_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test8_array[1] = {0}; 
k2c_tensor c_dense_70_1_test8 = {&c_dense_70_1_test8_array[0],1,1,{1,1,1,1,1}}; 
float test9_dense_68_input_1_input_array[3] = {
-9.98092022e-01f,-6.14715123e-01f,-2.39690086e-01f,}; 
k2c_tensor test9_dense_68_input_1_input = {&test9_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test9_array[1] = {
+1.39618525e-12f,}; 
k2c_tensor keras_dense_70_1_test9 = {&keras_dense_70_1_test9_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test9_array[1] = {0}; 
k2c_tensor c_dense_70_1_test9 = {&c_dense_70_1_test9_array[0],1,1,{1,1,1,1,1}}; 
float test10_dense_68_input_1_input_array[3] = {
+1.47401249e+00f,-4.48634071e-01f,-1.24697823e+00f,}; 
k2c_tensor test10_dense_68_input_1_input = {&test10_dense_68_input_1_input_array[0],1,3,{3,1,1,1,1}}; 
float keras_dense_70_1_test10_array[1] = {0}; 
k2c_tensor keras_dense_70_1_test10 = {&keras_dense_70_1_test10_array[0],1,1,{1,1,1,1,1}}; 
float c_dense_70_1_test10_array[1] = {0}; 
k2c_tensor c_dense_70_1_test10 = {&c_dense_70_1_test10_array[0],1,1,{1,1,1,1,1}}; 
int main(){
 float errors[10];
 size_t num_tests = 10; 
size_t num_outputs = 1; 
keras2c_model_initialize(); 
clock_t t0 = clock(); 
keras2c_model(&test1_dense_68_input_1_input,&c_dense_70_1_test1); 
keras2c_model(&test2_dense_68_input_1_input,&c_dense_70_1_test2); 
keras2c_model(&test3_dense_68_input_1_input,&c_dense_70_1_test3); 
keras2c_model(&test4_dense_68_input_1_input,&c_dense_70_1_test4); 
keras2c_model(&test5_dense_68_input_1_input,&c_dense_70_1_test5); 
keras2c_model(&test6_dense_68_input_1_input,&c_dense_70_1_test6); 
keras2c_model(&test7_dense_68_input_1_input,&c_dense_70_1_test7); 
keras2c_model(&test8_dense_68_input_1_input,&c_dense_70_1_test8); 
keras2c_model(&test9_dense_68_input_1_input,&c_dense_70_1_test9); 
keras2c_model(&test10_dense_68_input_1_input,&c_dense_70_1_test10); 

clock_t t1 = clock(); 
printf("Average time over 10 tests: %e s \n", 
 ((double)t1-t0)/(double)CLOCKS_PER_SEC/(double)10); 
errors[0] = maxabs(&keras_dense_70_1_test1,&c_dense_70_1_test1); 
errors[1] = maxabs(&keras_dense_70_1_test2,&c_dense_70_1_test2); 
errors[2] = maxabs(&keras_dense_70_1_test3,&c_dense_70_1_test3); 
errors[3] = maxabs(&keras_dense_70_1_test4,&c_dense_70_1_test4); 
errors[4] = maxabs(&keras_dense_70_1_test5,&c_dense_70_1_test5); 
errors[5] = maxabs(&keras_dense_70_1_test6,&c_dense_70_1_test6); 
errors[6] = maxabs(&keras_dense_70_1_test7,&c_dense_70_1_test7); 
errors[7] = maxabs(&keras_dense_70_1_test8,&c_dense_70_1_test8); 
errors[8] = maxabs(&keras_dense_70_1_test9,&c_dense_70_1_test9); 
errors[9] = maxabs(&keras_dense_70_1_test10,&c_dense_70_1_test10); 
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

