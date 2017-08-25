from mosek.fusion import *
import sys

n, p, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) 

M = Model()
x = M.variable([n,n], Domain.integral(Domain.unbounded()))
M.constraint(Expr.sum(x), Domain.lessThan(-1))
t = M.variable([n, n], Domain.integral(Domain.unbounded()))

M.constraint(Expr.add(t, x), Domain.greaterThan(0.0))
M.constraint(Expr.sub(t, x), Domain.greaterThan(0.0))

for l in [p,q]:
    for a in range(0,n+1-l):
        for b in range(0,n):
            M.constraint(Expr.sum(x.slice([a,b], [a+l,b+1])), Domain.greaterThan(0))
    for a in range(0,n):
        for b in range(0,n+1-l):
            M.constraint(Expr.sum(x.slice([a,b], [a+1,b+l])), Domain.greaterThan(0))

M.objective(ObjectiveSense.Minimize, Expr.sum(t))
M.setLogHandler(sys.stdout)
M.solve()

if M.getProblemStatus(SolutionType.Integer) == ProblemStatus.PrimalInfeasible:
    print "No answer"
else:
    xx = x.level()
    for a in range(0,n):
        for b in range(0,n):
            v = int(round(xx[n*a+b]))
            print v, ',',
        print
