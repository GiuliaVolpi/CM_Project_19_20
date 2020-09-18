import sys
from os import path
sys.path.insert(0, "./ISANet/")
sys.path.insert(0, "./")

from isanet.model import Mlp
from isanet.optimizer import SGD, NCG, LBFGS
from isanet.datasets.monk import load_monk
from isanet.utils.model_utils import printMSE, printAcc, plotHistory
import numpy as np

#np.random.seed(seed=777)
def get_fitted_model(X_train, Y_train, optimizer, n_seed = 189, verbose = 1):
    np.random.seed(seed=n_seed)
    print("Build the model")
    model = Mlp()
    model.add(4, input= 17, kernel_initializer = 1/np.sqrt(17), kernel_regularizer = 0.001)
    model.add(1, kernel_initializer = 1/np.sqrt(4), kernel_regularizer = 0.001)

    model.set_optimizer(optimizer)

    model.fit(X_train,
            Y_train, 
            epochs=20000, 
            #batch_size=31,
            #validation_data = [X_test, Y_test],
            verbose=verbose)

    return model 


print("Load Monk DataSet")
X_train, Y_train = load_monk("2", "train")

seed = 189
ln_maxiter = 100


#############################
#          NCG f1
#############################
restart = 3
optimizer = NCG(beta_method="fr", c1=1e-4, c2=.3, restart=restart, ln_maxiter = ln_maxiter, tol = 1e-14)


model = get_fitted_model(X_train, Y_train, optimizer, seed, 1)
h_fr = model.history 

#############################
#          NCG pr
#############################

optimizer = NCG(beta_method="pr", c1=1e-4, ln_maxiter = ln_maxiter, c2=.9, tol = 1e-14)

model = get_fitted_model(X_train, Y_train, optimizer, seed, 1)
h_pr = model.history 

#############################
#          NCG Hs
#############################

optimizer = NCG(beta_method="hs", c1=1e-4, c2=.9, ln_maxiter = ln_maxiter, tol = 1e-14)

model = get_fitted_model(X_train, Y_train, optimizer, seed, 1)
h_hs = model.history 

#############################
#          L-BFGS
#############################
m = 20
optimizer = LBFGS(m=m, c1= 1e-4, c2=0.9, ln_maxiter = ln_maxiter, tol=1e-14)

model = get_fitted_model(X_train, Y_train, optimizer, seed, 1)
h_lbfgs = model.history 

##############################
# plot
##############################

import matplotlib.pyplot as plt

pos_train = (0,0)
figsize = (12, 4)

plt.plot(h_fr["loss_mse"], linestyle='-')
plt.plot(h_pr["loss_mse"], linestyle = '--')
plt.plot(h_hs["loss_mse"], linestyle='-.')
plt.plot(h_lbfgs["loss_mse"], linestyle=':')
plt.title('Monk2 - seed=189')
plt.ylabel("MSE")
plt.xlabel('Epoch')
plt.grid()
plt.yscale('log')
plt.legend(['NCG - FR - R={}'.format(restart),'NCG - PR+','NCG - HS+', 'L-BFGS - m={}'.format(m)], loc='upper right', fontsize='large')    
plt.show()