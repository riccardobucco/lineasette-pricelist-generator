from ortools.constraint_solver import pywrapcp

def get_solution(mult, column_height, heights):
    slv = pywrapcp.Solver("listino")
    # Compute X domains
    cumulative_heights = [sum(heights[:idx+1]) for idx, h in enumerate(heights)]
    sum_heights = sum(heights)
    num_columns = 0    
    while column_height * num_columns < sum_heights:
        num_columns += mult
    domains = []
    for i in range(num_columns):
        domain = cumulative_heights
        try:
            index = next(idx for idx, x in enumerate(domain) if x > (i+1)*column_height)
        except StopIteration as err:
            index = len(domain)
        domain = domain[:index]
        domains += [domain]
    for i in range(num_columns-1, mult-1, -1):
        domains[i] = sorted(list(set(domains[i]) - set(domains[i-mult])))
    X_domains = [[] for h in heights]
    for idx, domain in enumerate(domains):
        for cum_height in domain:
            index = cumulative_heights.index(cum_height)
            X_domains[index] += [idx]
    # Define variables
    X = [] # X_i: column c where the i-th element should be placed
    for i, X_domain in enumerate(X_domains):
        X += [slv.IntVar(X_domain, "X_{}".format(i))]
    US = [] # US_c: space used on column c
    for c in range(num_columns):
        US += [slv.IntVar(0, column_height, "US_{}".format(c))]
    FS = [] # FS_c: free space on column c
    for c in range(num_columns):
        FS += [slv.IntVar(0, column_height, "FS_{}".format(c))]
    mean_FS = slv.IntVar(0, column_height, "mean_FS") # mean free space
    Z = slv.IntVar(0, column_height, "Z") # variance
    # Define contraints
    for i in range(len(X)-1):
        for j in range(i+1, len(X)):
            slv.Add(X[i] <= X[j])
    for c in range(num_columns):
        used_space_c = sum((X[i] == c)*heights[i] for i in range(len(heights)))
        slv.Add(US[c] == used_space_c)
        slv.Add(FS[c] == column_height - US[c])
    # Cost function
    slv.Add(Z == slv.Max([FS[c] for c in range(num_columns)]))
    m = slv.Minimize(Z, 1)
    # Find optimal solution
    variables = X
    decision_builder = slv.Phase(variables, slv.INT_VAR_DEFAULT, slv.INT_VALUE_DEFAULT)
    slv.NewSearch(decision_builder, [m])
    while slv.NextSolution():
        best_solution = [v.Value() for v in variables[:len(heights)]]
    slv.EndSearch()
    return best_solution, num_columns