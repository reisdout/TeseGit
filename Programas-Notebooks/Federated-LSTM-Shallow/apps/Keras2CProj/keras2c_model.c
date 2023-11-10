#include <math.h> 
 #include <string.h> 
#include "./include/k2c_include.h" 
#include "./include/k2c_tensor_include.h" 

 


void keras2c_model(k2c_tensor* dense_68_input_1_input, k2c_tensor* dense_70_1_output) { 

float dense_68_output_array[20] = {0}; 
k2c_tensor dense_68_output = {&dense_68_output_array[0],1,20,{20, 1, 1, 1, 1}}; 
float dense_68_kernel_array[60] = {
-1.04626305e-02f,-1.38489427e-02f,+2.80009620e-02f,-1.85167342e-02f,+4.69948538e-02f,
+5.33367507e-02f,+6.67548105e-02f,+5.29491790e-02f,+7.02229813e-02f,+6.99670464e-02f,
+2.77499240e-02f,+2.96481177e-02f,-9.24018025e-03f,+2.73745339e-02f,+5.35146743e-02f,
+1.64938085e-02f,+5.17090201e-01f,+5.21747023e-02f,+6.25099316e-02f,+2.03872323e-02f,
+7.23078772e-02f,+6.56160116e-02f,-2.32916605e-02f,+4.62371968e-02f,-2.54048835e-02f,
+1.54929012e-01f,+5.38166091e-02f,-3.95850977e-03f,-1.81149635e-02f,+4.20286171e-02f,
+1.97778419e-02f,+3.78378220e-02f,+1.17666069e-02f,-2.24352274e-02f,+6.32296223e-03f,
-3.99258137e-02f,+4.03960586e-01f,+3.40443105e-02f,+3.22912559e-02f,+1.09911161e-02f,
+4.45453852e-01f,+4.68047351e-01f,-4.56491970e-02f,-4.51814681e-02f,-2.98268437e-01f,
+3.55963588e-01f,-2.63597101e-01f,-2.97722369e-01f,-3.24177057e-01f,-2.71146625e-01f,
-3.52145359e-02f,-2.93273836e-01f,+4.34380114e-01f,-3.00387353e-01f,-2.96615452e-01f,
-1.49117485e-02f,+4.96367276e-01f,-2.38585681e-01f,-2.63561904e-01f,+4.08213526e-01f,
}; 
k2c_tensor dense_68_kernel = {&dense_68_kernel_array[0],2,60,{ 3,20, 1, 1, 1}}; 
float dense_68_bias_array[20] = {
-1.73081949e-01f,-1.52666703e-01f,+0.00000000e+00f,-2.88818800e-03f,+2.97965378e-01f,
-2.25618511e-01f,+2.52963334e-01f,+2.95977235e-01f,+3.18822175e-01f,+2.60306716e-01f,
-1.69478785e-02f,+2.91601866e-01f,-1.79613903e-01f,+3.05258811e-01f,+2.93904245e-01f,
+0.00000000e+00f,+3.70784014e-01f,+3.19830865e-01f,+2.53218174e-01f,-1.61594078e-01f,
}; 
k2c_tensor dense_68_bias = {&dense_68_bias_array[0],1,20,{20, 1, 1, 1, 1}}; 
float dense_68_fwork[63] = {0}; 

 
float dense_69_output_array[20] = {0}; 
k2c_tensor dense_69_output = {&dense_69_output_array[0],1,20,{20, 1, 1, 1, 1}}; 
float dense_69_kernel_array[400] = {
-3.85397196e-01f,+5.09656787e-01f,-3.37752074e-01f,-2.66992804e-02f,+5.20439073e-03f,
-3.57264578e-01f,+9.95030999e-03f,+5.70413291e-01f,-2.26451345e-02f,+5.59967399e-01f,
-1.00999698e-02f,+5.63598871e-01f,-2.69099548e-02f,-4.12786864e-02f,-4.74109501e-03f,
-4.24897075e-02f,+5.81233084e-01f,-3.33863407e-01f,+5.93070745e-01f,+5.88138938e-01f,
-2.98952639e-01f,+5.43506384e-01f,-2.98025966e-01f,+9.68527049e-04f,+1.83552764e-02f,
-2.46397093e-01f,-7.56958779e-03f,+5.31368077e-01f,-4.92364392e-02f,+5.29490709e-01f,
-1.58819556e-02f,+5.29311359e-01f,+2.18942296e-02f,-8.95177294e-03f,-1.58082470e-02f,
+4.16366719e-02f,+4.66275543e-01f,-2.93468118e-01f,+4.82279450e-01f,+5.03905118e-01f,
+3.91131639e-03f,+3.86275314e-02f,+4.55758721e-03f,-2.66187433e-02f,+3.14843692e-02f,
-4.28467169e-02f,+2.34055519e-03f,-4.92394678e-02f,-4.33937572e-02f,-7.42661953e-03f,
+1.65358298e-02f,+1.81110762e-02f,+1.76517032e-02f,+2.48308443e-02f,-4.42971960e-02f,
-2.80345324e-02f,-2.29685903e-02f,-3.82547602e-02f,+3.29499729e-02f,-1.99198127e-02f,
-2.64638457e-02f,+9.91214067e-03f,-4.20119055e-02f,-1.91298481e-02f,-4.76790778e-02f,
-1.09024001e-02f,+2.31794789e-02f,-2.60635577e-02f,+9.69947502e-03f,-2.51369551e-02f,
+1.66687258e-02f,+3.99711430e-02f,-4.33454774e-02f,-3.05947065e-02f,+9.65195894e-03f,
-1.80410966e-02f,+4.11953740e-02f,-3.73537652e-02f,-4.09501232e-02f,-1.10319508e-02f,
+1.53379130e+00f,-1.40518236e+00f,+1.52263319e+00f,+1.70237757e-02f,+1.10741034e-02f,
+1.48539305e+00f,-7.00845523e-03f,-1.36090577e+00f,+5.93452901e-03f,-1.32994998e+00f,
+3.67930792e-02f,-1.39605772e+00f,+1.92884374e-02f,-4.13335748e-02f,-3.72239724e-02f,
-3.63963731e-02f,-1.32336760e+00f,+1.48324871e+00f,-1.41327226e+00f,-1.41351330e+00f,
-4.87774938e-01f,+6.61341846e-01f,-5.33076704e-01f,+2.60858648e-02f,-3.62471342e-02f,
-4.78171170e-01f,+1.68394390e-02f,+7.14098811e-01f,-1.41904503e-03f,+7.23440051e-01f,
-2.98496373e-02f,+7.06165612e-01f,-2.18772888e-02f,-4.88546900e-02f,+6.05734438e-03f,
-4.98357303e-02f,+6.62748992e-01f,-5.03068626e-01f,+6.72694385e-01f,+6.48537695e-01f,
+7.83406496e-01f,-6.51272535e-01f,+8.39109302e-01f,+1.36000551e-02f,-1.46551616e-02f,
+8.32206547e-01f,-1.11169489e-02f,-6.63197756e-01f,-3.45032178e-02f,-6.32388592e-01f,
-1.49082057e-02f,-6.82266474e-01f,-4.05930355e-02f,-3.29342335e-02f,-3.54898199e-02f,
+3.94742228e-02f,-6.54973328e-01f,+7.61111259e-01f,-6.67895794e-01f,-7.27979958e-01f,
+1.26129866e+00f,-1.04815376e+00f,+1.25385165e+00f,-4.30358909e-02f,-1.52888894e-02f,
+1.20333946e+00f,+2.39984356e-02f,-1.09847867e+00f,+1.54623734e-02f,-1.09368289e+00f,
+7.45061785e-03f,-1.09556282e+00f,-4.30090949e-02f,+2.10665986e-02f,+6.59191608e-03f,
-2.82964949e-02f,-1.11746109e+00f,+1.21539688e+00f,-1.07119501e+00f,-1.08680689e+00f,
+1.35723245e+00f,-1.20508242e+00f,+1.37170994e+00f,-4.13223729e-02f,-1.30322091e-02f,
+1.35157263e+00f,-2.34962963e-02f,-1.22995257e+00f,+1.56132728e-02f,-1.21281052e+00f,
+3.26981805e-02f,-1.23373032e+00f,+3.06797959e-02f,-4.65849489e-02f,-2.42564678e-02f,
+2.67451648e-02f,-1.26209247e+00f,+1.34547770e+00f,-1.27341235e+00f,-1.24312532e+00f,
+8.69028986e-01f,-7.20446408e-01f,+8.25614691e-01f,+2.81867124e-02f,-1.02676451e-04f,
+8.78467262e-01f,-4.07832712e-02f,-7.09271848e-01f,+4.74971496e-02f,-7.01971829e-01f,
-3.60521302e-02f,-6.94885731e-01f,+9.51925479e-03f,-3.93821895e-02f,+4.89137657e-02f,
-2.19820663e-02f,-7.53106892e-01f,+8.12450409e-01f,-7.21417189e-01f,-7.46386766e-01f,
-2.05837917e-02f,+8.34818836e-03f,+2.73629818e-02f,-1.23942867e-02f,+3.35763805e-02f,
-1.82686374e-02f,-2.45493799e-02f,-2.51519401e-03f,-1.48776406e-02f,+3.29046473e-02f,
+2.53659487e-03f,-2.57264208e-02f,-1.19555481e-02f,+5.07080555e-03f,+1.23540759e-02f,
+1.40079595e-02f,-2.05001049e-02f,-2.78447587e-02f,-4.60850857e-02f,-4.25177030e-02f,
+1.06585419e+00f,-8.69791746e-01f,+1.08182847e+00f,+3.83786671e-02f,-1.43463239e-02f,
+1.10643172e+00f,+3.62811889e-03f,-9.79281068e-01f,+7.81753287e-03f,-9.34044540e-01f,
-4.73114103e-03f,-9.28387165e-01f,-4.16084342e-02f,+1.56591460e-02f,+4.14604582e-02f,
-5.02260141e-02f,-9.62241530e-01f,+1.06513739e+00f,-9.63749826e-01f,-9.76438522e-01f,
-3.96598369e-01f,+5.46195984e-01f,-4.68151271e-01f,-4.01077159e-02f,-3.32065001e-02f,
-4.47421581e-01f,-3.45606841e-02f,+6.26636505e-01f,-2.49604043e-02f,+5.99369526e-01f,
-2.23807823e-02f,+5.80478489e-01f,+2.34274212e-02f,+2.38910764e-02f,-3.26194167e-02f,
+9.83998179e-03f,+6.05702698e-01f,-4.68541026e-01f,+6.37316167e-01f,+6.54859424e-01f,
+1.77616119e+00f,-1.66435099e+00f,+1.78821325e+00f,+4.73709442e-02f,-2.82974243e-02f,
+1.83681500e+00f,-3.80005091e-02f,-1.63867235e+00f,-4.31464277e-02f,-1.72424376e+00f,
+9.02254507e-03f,-1.66256642e+00f,+2.02010944e-03f,+4.13754247e-02f,+2.71961726e-02f,
+4.45673289e-03f,-1.70053434e+00f,+1.82932460e+00f,-1.72847569e+00f,-1.69302690e+00f,
+1.12990129e+00f,-9.90832210e-01f,+1.14038658e+00f,-8.91583040e-03f,-7.50046968e-03f,
+1.18846822e+00f,-4.77159545e-02f,-1.04001462e+00f,+2.85845827e-02f,-1.02210748e+00f,
+4.84795012e-02f,-1.06511986e+00f,-2.27511171e-02f,+2.48458516e-03f,-1.18895397e-02f,
-4.20935750e-02f,-1.01999795e+00f,+1.18724024e+00f,-1.05071354e+00f,-9.94895995e-01f,
+2.57234685e-02f,-4.58918698e-02f,-3.75527628e-02f,+4.29569148e-02f,-2.94137727e-02f,
-4.86089587e-02f,+3.96998972e-03f,+1.49745680e-02f,+4.51897494e-02f,+4.50989716e-02f,
+4.76892479e-02f,+2.85195820e-02f,+1.29909627e-02f,+2.50298716e-02f,-4.90359217e-03f,
+3.41553614e-03f,-3.58113535e-02f,+1.25962608e-02f,-4.34868447e-02f,+3.77137549e-02f,
+2.02922314e-01f,+1.38928577e-01f,+2.25945815e-01f,-4.85238098e-02f,-2.30752472e-02f,
+1.41946957e-01f,+8.13155621e-03f,+1.16304874e-01f,-3.18641923e-02f,+9.73559916e-02f,
-4.68863249e-02f,+1.52455986e-01f,-1.33612175e-02f,+3.02363615e-02f,-4.20724750e-02f,
+1.30685400e-02f,+1.64476052e-01f,+1.96527377e-01f,+1.32092267e-01f,+1.19974121e-01f,
+6.61640942e-01f,-3.55341852e-01f,+6.37425780e-01f,+2.00060867e-02f,-3.22879702e-02f,
+6.00427747e-01f,-9.27764643e-03f,-3.61444890e-01f,-1.09636551e-02f,-3.42013955e-01f,
-1.19641796e-02f,-4.41914141e-01f,+1.93036476e-03f,-2.66199373e-02f,-1.75905451e-02f,
+3.44001167e-02f,-4.27433521e-01f,+6.42621577e-01f,-3.90010208e-01f,-3.67320925e-01f,
+9.14639413e-01f,-7.61388302e-01f,+9.03136432e-01f,-3.21783312e-02f,-3.56589332e-02f,
+8.52368236e-01f,-8.95810872e-03f,-7.56954312e-01f,-7.70175550e-03f,-7.92674363e-01f,
-3.81845348e-02f,-7.92820036e-01f,-4.69163954e-02f,-5.10256886e-02f,-4.29488532e-02f,
-4.96749245e-02f,-7.44225383e-01f,+9.31214452e-01f,-7.60567367e-01f,-7.92179465e-01f,
-3.93839896e-01f,+5.93696475e-01f,-3.55380267e-01f,-4.13213484e-02f,+7.41857290e-03f,
-4.00234133e-01f,-1.17573887e-02f,+5.96965134e-01f,+4.32186611e-02f,+6.14825189e-01f,
+2.19235905e-02f,+5.44224858e-01f,-7.38622574e-03f,-5.54922186e-02f,+2.93644108e-02f,
-3.87400761e-02f,+5.15622795e-01f,-3.83491814e-01f,+5.98149955e-01f,+5.90536416e-01f,
}; 
k2c_tensor dense_69_kernel = {&dense_69_kernel_array[0],2,400,{20,20, 1, 1, 1}}; 
float dense_69_bias_array[20] = {
+3.63068700e-01f,-1.31568015e-01f,+3.57771635e-01f,+0.00000000e+00f,+0.00000000e+00f,
+3.77913207e-01f,-8.59138556e-03f,-1.27643049e-01f,-1.21768913e-03f,-1.08335465e-01f,
+0.00000000e+00f,-1.32023335e-01f,-2.94946507e-03f,-6.34667045e-03f,+0.00000000e+00f,
-2.31411913e-03f,-1.27542943e-01f,+3.68214726e-01f,-1.20084248e-01f,-1.07094616e-01f,
}; 
k2c_tensor dense_69_bias = {&dense_69_bias_array[0],1,20,{20, 1, 1, 1, 1}}; 
float dense_69_fwork[420] = {0}; 

 
float dense_70_kernel_array[20] = {
-1.87414479e+00f,+2.29306459e+00f,-1.73712051e+00f,+1.49234772e-01f,-1.46947861e-01f,
-1.74225116e+00f,-4.25239176e-01f,+2.17575288e+00f,+3.13818362e-03f,+2.04557562e+00f,
+1.94336593e-01f,+2.18858910e+00f,-4.71287400e-01f,+4.29412037e-01f,+1.01463735e-01f,
-7.23239966e-03f,+2.20640707e+00f,-1.66779339e+00f,+2.01018310e+00f,+1.94010377e+00f,
}; 
k2c_tensor dense_70_kernel = {&dense_70_kernel_array[0],2,20,{20, 1, 1, 1, 1}}; 
float dense_70_bias_array[1] = {
-2.99396485e-01f,}; 
k2c_tensor dense_70_bias = {&dense_70_bias_array[0],1,1,{1,1,1,1,1}}; 
float dense_70_fwork[40] = {0}; 

 
k2c_dense(&dense_68_1_output,dense_68_input_1_input,&dense_68_kernel, 
	&dense_68_bias,k2c_relu,dense_68_fwork); 
k2c_dense(&dense_69_1_output,&dense_68_1_output,&dense_69_kernel, 
	&dense_69_bias,k2c_relu,dense_69_fwork); 
k2c_dense(dense_70_1_output,&dense_69_1_output,&dense_70_kernel, 
	&dense_70_bias,k2c_sigmoid,dense_70_fwork); 

 } 

void keras2c_model_initialize() { 

} 

void keras2c_model_terminate() { 

} 

