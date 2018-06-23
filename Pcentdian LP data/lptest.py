# p-median & p-center problem use linear programing

from pulp import *
#import pandas as pd
import sys

prob = LpProblem('pmedian',LpMaximize)

'''x11 = LpVariable('x11', lowBound = 0,upBound = 1.0)
x12 = LpVariable('x12', lowBound = 0)
x13 = LpVariable('x13', lowBound = 0)
x21 = LpVariable('x21', lowBound = 0)
x22 = LpVariable('x22', lowBound = 0)
x23 = LpVariable('x23', lowBound = 0)
x31 = LpVariable('x31', lowBound = 0)
x32 = LpVariable('x32', lowBound = 0)
x33 = LpVariable('x33', lowBound = 0)
#z = LpVariable('z', lowBound = 0)'''
x = LpVariable('x', cat='Integer',lowBound = 0, upBound = 2)
y = LpVariable('y', lowBound = 0)

prob += 2.5*x + 1.2*y

prob += 2*x - y <= 4
prob += x + 2*y <= 9
prob += -x + y <= 3

GLPK().solve(prob)

for i in prob.variables():
    print(i.name + "=" + str(i.varValue))

print "objective = ", value(prob.objective)
sys.exit('stop')

# Number of customers
n = 29
# Set of candidate locations
M = list(range(n))
# Set of customer nodes
N = list(range(n))

# Number of facilities
p = 3
# c[i,j] - unit cost of satisfying customer j from facility i
#model.c = Param(model.M, model.N, initialize=lambda i, j, model : random.uniform(1.0,2.0), within=Reals)
c = []
bay = open('nbayg29.csv')
for b in bay:
    f = b.strip('\n').split(' ')
    num = []
    for q in f:
        q = float(q)
        num.append(q)
    c.append(num)
#D = dict(zip(M,[dict(zip(M,c[z] for z in M ))]))
D = dict(zip(M,[dict(zip(M,c[0])),
    dict(zip(M,c[1])),
    dict(zip(M,c[2])),
    dict(zip(M,c[3])),
    dict(zip(M,c[4])),
    dict(zip(M,c[28]))]))
# x[i,j] - fraction of the demand of customer j that is supplied by facility i
x = LpVariable.dicts('X_%s_%s', (M,M), cat = 'Continuous', lowBound = 0.0, upBound = 1.0)

# Minimize the demand-weighted total cost
prob = LpProblem('P Median',LpMinimize)
prob += sum(sum(c[i][j]*x[i][j] for j in M) for i in M)
# All of the demand for customer j must be satisfied
for i in M:
    prob += sum(x[i][j] for j in M) == 1
# Exactly p facilities are located
    prob += sum(x[i][i] for i in M) == p
# Demand nodes can only be assigned to open facilities
for i in M:
    for j in M:
        prob += x[i][j] <= x[j][j]

prob.writeLP("p-median.lp")

print(prob)

prob.solve()
print("Status:",LpStatus[prob.status])
print("Objective:",value(prob.objective))
for v in prob.variables():
    if v.varValue == 1:
        print(v.name, "=", v.varValue)
