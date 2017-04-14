#
# Demonstrates the usage of hierarchical partial pooling
# See http://mc-stan.org/documentation/case-studies/pool-binary-trials.html for more details
#

import pymc3 as pm
import numpy as np
import theano

data = np.loadtxt( 'data/efron-morris-75-data.tsv', delimiter="\t", skiprows=1, usecols=(2,3) )

theano.config.floatX = 'float32'
atBats = data[:,0]
hits = data[:,1]

N = len( hits )

model = pm.Model()

# we want to bound the kappa below
BoundedKappa = pm.Bound( pm.Pareto, lower=1.0 )

with model:
    phi = pm.Uniform( 'phi', lower=0.0, upper=1.0 )
    kappa = BoundedKappa( 'kappa', alpha=1.0001,  m=1.5 )
    thetas = pm.Beta( 'thetas', alpha=phi.astype(theano.config.floatX)*kappa.astype(theano.config.floatX) , beta=((1.0-phi)*kappa).astype(theano.config.floatX), shape=N )
    ys = pm.Binomial( 'ys', n=atBats.astype(theano.config.floatX), p=thetas, observed=hits.astype(theano.config.floatX) )

def run( n=100000 ):
    with model:
        # initialize NUTS() with ADVI under the hood
        trace = pm.sample( n )

    # drop some first samples as burnin
    pm.traceplot( trace[1000:] )

if __name__ == '__main__':
    run()

