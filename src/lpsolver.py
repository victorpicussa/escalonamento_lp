#!/usr/bin/python3
import pulp as plp

def solver(h, u, c, x, zeros, N, K):
    model = plp.LpProblem(name="Machine_Schedulling")

    # Decision Variables
    t = {(i,j):
        plp.LpVariable(cat=plp.LpContinuous, 
                lowBound=0.0, upBound= h[i],
                name="x_{0}_{1}".format(i,j)) 
        for i in N for j in K}

    # Objective
    objective = plp.lpSum(t[i,j]*c[j] 
                for i in N 
                for j in K)

    model.sense = plp.LpMinimize

    model.setObjective(objective)

    # Constraints
    constraints = {j : model.addConstraint(
        plp.LpConstraint(
            e=plp.lpSum(t[i,j]*x[i,j] for i in N),
            sense=plp.LpConstraintLE,
            rhs=u[j],
            name="constraint_maxtime_{0}".format(j)))
       for j in K}

    constraints = {i : model.addConstraint(
        plp.LpConstraint(
             e=plp.lpSum(t[i,j] for j in K),
             sense=plp.LpConstraintEQ,
             rhs=h[i],
             name="constraint_time_{0}".format(i)))
       for i in N}

    constraints = {j : model.addConstraint(
        plp.LpConstraint(
             e=t[zeros[j]],
             sense=plp.LpConstraintEQ,
             rhs=float(0),
             name="constraint_zero_{0}".format(j)))
       for j in range(0, len(zeros))}

    constraints = {j : model.addConstraint(
        plp.LpConstraint(
             e=t[i,j],
             sense=plp.LpConstraintGE,
             rhs=float(0),
             name="constraint_gezero_{0}_{1}".format(j,i)))
       for i in N for j in K}

    # Solver
    model.solve(plp.PULP_CBC_CMD(msg=0))

    if model.status != 1:
        print('Falha em encontrar a solução: %s' %plp.LpStatus[model.status])
        exit(-1)
    
    for j in K:
        for i in N:
            print("%s " % (t[i,j].varValue), end="")
        print()

    print(plp.value(model.objective))
    