# -*- coding: utf-8 -*-
"""LS_Linear_Optimzation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-rIqnzG-FYG2wixDk6JkxZ54d-dY4ZrM

# **LINEAR OPTIMIZATION FINAL PROJECT**

# **ROBUST SHORTEST TIME DELIVERY PATHS**

<p align="justify">
The Amazon company has a startup project specializing in package delivery within the western areas of the United States. They advertise guaranteed delivery within a specified time. Their quoted times are not always shorter than other delivery companies, but delivery comes with a money-back guarantee if, for any reason, the delivery is not met on time. The company necessarily has a vested interest in finding delivery routes that are not only efficient (short) but robust (not likely to incur delays). In order to set their rates, the company is seeking a method for finding an optimal route between two given locations.

<p align="justify">
The problem of finding a shortest path between two locations can be easily solved as an integer program, provided that the number of possible routes is not too large. Also,the problem of finding the route least likely to incur a delay is similarly solved. Amazon would like to solve the problem of a compromise route that helps then maintain competitiveness without significant reduction in promised delivery time.

<p align="justify">
You are given the following tasks:
<p align="justify">
1. Use the provided network data to solve the shortest path problem for user-supplied starting and ending locations. Ignore any possible delays.
<p align="justify">
2. Use the provided network data to solve the minimum delay likelihood problem for user-supplied starting and ending locations. Ignore travel times.
<p align="justify">
3. Combine the two previous solution methods where the objective is to minimize the weighted sum of travel time and delay likelihood. The relative weight should be an adjustable parameter. Determine a reasonable relative weighting based on experiments you perform.
<p align="justify">
4. Solve the combined problem using your weight selection with starting city A and ending locations at every other city. Report your findings and make recommendations to the company.

<p align="justify">
The data set is provided as two files distance.csv and delay.csv which are commadelimited 15 x 15 arrays. The entry in the ith row and jth column of the respective arrays gives the distance (or delay probability) between city i and city j. If an array has entry zero,
this indicates that the cities are not connected by a path.
<p align="justify">
The networks we will consider are symmetric - distances and delays do not depend on the direction of travel.

# **MODELING THE PROBLEM**

---

Let $x_{ij}$ be a binary decision variable where:

$x_{ij} = 1$ if the path from city $i$ to city $j$ is included in the travel from city $A$ to city $O$ , and
$x_{ij} = 0$ otherwise.

The objective function to minimize is the total distance of the path:

\begin{equation}
\text{Minimize} \sum_{i,j} d_{ij} \cdot x_{ij}
\end{equation}

Subject to the following constraints:

Ensure that there is zero or one outgoing edge from each inner city(except for A, O):

\begin{equation}
\sum_{j} x_{ij} = y_{j} \quad \text{for} \quad i \in \{B, C, D, E, F, G, H, I, J, K, L, M, N\}
\end{equation}

Ensure that there is zero or one incoming edge to each inner city (except for A, O):

\begin{equation}
\sum_{i} x_{ij} = y_{i} \quad \text{for} \quad j \in \{B, C, D, E, F, G, H, I, J, K, L, M, N\}
\end{equation}

where $y_{j}  \in \{0, 1\}$, and $y_{i}  \in \{0, 1\}$. Note that although it seems we used different notations for the number of outgoing and incoming edges from a city, they ( $y_{j}$ and $y_{i}$) are the same numbers for the same city. For example, if the number of outgoing edges from city $B$ ($j=B$) is $y_{B}$, so is that of incoming edges to city $B$ ($i = B$), which means $y_{j}$ and $y_{i}$ are the same numbers for the same city.


Ensure that the destination city has exactly zero outgoing edges:

\begin{equation}
\sum_{j} x_{Oj} = 1 \quad \text{for} \quad j \in \{A, B, C, D, E, F, G, H, I, J, K, L, M, N, O\}
\end{equation}

Ensure that the starting city has exactly zero incoming edges:

\begin{equation}
\sum_{i} x_{iA} = 0 \quad \text{for} \quad i \in \{A, B, C, D, E, F, G, H, I, J, K, L, M, N, O\}
\end{equation}

Ensure that the destination city has exactly one incoming edge:

\begin{equation}
\sum_{i} x_{iO} = 1 \quad \text{for} \quad i \in \{A, B, C, D, E, F, G, H, I, J, K, L, M, N, O\}
\end{equation}

Ensure that the starting city has exactly one outgoing edge:

\begin{equation}
\sum_{j} x_{Aj} = 0 \quad \text{for} \quad j \in \{A, B, C, D, E, F, G, H, I, J, K, L, M, N, O\}
\end{equation}

$x_{ij}$, $y_{i}  \in \{0, 1\}$,  $\quad \forall i,j \in \{A, B, C, D, E, F, G, H, I, J, K, L, M, N, O\}$

These constraints ensure that:

- There is exactly one path from the starting city to the destination city.
- There are no cycles in the path.
- Each city (excluding the starting and destination cities) may not necessarily be visited exactly once.

Solving this linear programming problem will give us the shortest path between the given cities both in terms of distances and likelikood of delays.

# Receiving and reading the data
"""

# Obtaining given data
import numpy as np
from numpy import genfromtxt


cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
start_city = cities[0]
destination_city = cities[-1]

# Number of cities
num_cities = len(cities)

my_distances = genfromtxt('distance.csv', delimiter=',')
my_delays = genfromtxt('delay.csv', delimiter=',')

d = my_distances.flatten()
rhs_binary = np.zeros(num_cities-2)
d = np.concatenate((d, rhs_binary))

p = my_delays.flatten()
rhs_binary = np.zeros(num_cities-2)
p = np.concatenate((p, rhs_binary))

# print(my_distances)
# print(my_delays)

"""# Creating the constraints"""

def get_constraints(file_name: str):

    """
    Generate constraints for an optimization problem based on given data.

    Args:
    - file_name (str): The name of the file containing the data.
                       It should be either 'distance.csv' or 'delay.csv'.

    Returns:
    - distances (numpy.ndarray): The distances between cities.
    - A_ineq (None): Inequality constraint matrix (None for this function).
    - b_ineq (None): Inequality bounds (None for this function).
    - Ae (numpy.ndarray): Equality constraint matrix.
    - be (numpy.ndarray): Equality bounds.
    """

    if file_name == 'distance.csv':
        distances = my_distances
    elif file_name == 'delay.csv':
        distances = my_delays
    else:
        print("File not found")


    # Distance between cities (replace with actual distances)
    # distances = my_distances[:4, :4]
    # distances = my_distances
    # delays = my_delays
    # distances[1, 3] = 6
    # distances[3, 1] = 6

    # Find the maximum distance
    max_distance = np.max(distances)

    # Update main diagonal elements
    np.fill_diagonal(distances, max_distance + 1)
    # print("distances:")
    # print(distances)

    # Inequality Constraints:

    # Constraint coefficients for exactly zero or one outgoing edge from each inner city(except for A, O)
    A_outgoing = []
    b_outgoing = []
    for i_index, i in enumerate(cities[1:-1]):  # Exclude the last city
        # print(i_index, i)
        row = np.zeros(num_cities ** 2)
        rhs_binary = np.zeros(num_cities-2) # to count # of outgoing edges from each inner cities, B, C, ..., N.
        rhs_binary[i_index] = -1 # outgoing = incoming, so same rhs binaries
        for j in cities:
            if j != i and distances[cities.index(i), cities.index(j)] > 0:
                j_index = cities.index(j)
                row[num_cities * cities.index(i) + cities.index(j)] = 1
        row = np.concatenate((row, rhs_binary))
        A_outgoing.append(row)
        b_outgoing.append(0)
    # print("A_outgoing:")
    # print(np.array(A_outgoing))

    # Constraint coefficients for exactly zero or one incoming edge from each inner city(except for A, O)
    A_incoming = []
    b_incoming = []

    for j_index, j in enumerate(cities[1:-1]):  # Exclude the last city
        row = np.zeros(num_cities ** 2)
        rhs_binary = np.zeros(num_cities-2) # to count # of incoming edges from each inner cities, B, C, ..., N.
        rhs_binary[j_index] = -1 # outgoing = incoming, so same rhs binaries
        for i_index, i in enumerate(cities):
            if i != j and distances[cities.index(i), cities.index(j)] > 0:
                row[num_cities * cities.index(i) + cities.index(j)] = 1
        row = np.concatenate((row, rhs_binary))
        A_incoming.append(row)
        b_incoming.append(0)
    # print("A_incoming:")
    # print(np.array(A_incoming))

    A = np.vstack((A_outgoing, A_incoming))
    b = np.concatenate((b_outgoing, b_incoming))
    # print("\nInequality Constraints (A):")
    # print(np.array(A))
    # print("\nInquality Bounds (b):")
    # print(np.array(b))

    # Equality Constraints
    A_eq = []
    b_eq = []

    # Destination city constraint for having 0 outgoing edges
    row = np.zeros(num_cities ** 2)
    rhs_binary = np.zeros(num_cities-2)
    for j in cities:
        if distances[cities.index(destination_city), cities.index(j)] > 0:
            row[num_cities * cities.index(destination_city) + cities.index(j)] = 1
    row = np.concatenate((row, rhs_binary))
    A_eq.append(row)
    b_eq.append(0)
    # print("A_eq:")
    # print(np.array(A_eq))


    # Starting city constraint for having zero incoming edges
    row = np.zeros(num_cities ** 2)
    rhs_binary = np.zeros(num_cities-2)
    for i in cities:
        if distances[cities.index(i), cities.index(start_city)] > 0:
            row[num_cities * cities.index(i) + cities.index(start_city)] = 1
    row = np.concatenate((row, rhs_binary))
    A_eq.append(row)
    b_eq.append(0)
    # print("A_eq:")
    # print(np.array(A_eq))

    # Destination city constraint for having 1 incoming edge
    row = np.zeros(num_cities ** 2)
    rhs_binary = np.zeros(num_cities-2)
    for i in cities:
        if distances[cities.index(i), cities.index(destination_city)] > 0:
            row[num_cities * cities.index(i) + cities.index(destination_city)] = 1
    row = np.concatenate((row, rhs_binary))
    A_eq.append(row)
    b_eq.append(1)
    # print("A_eq:")
    # print(np.array(A_eq))

    # Starting city constraint for having 1 outgoing edge
    row = np.zeros(num_cities ** 2)
    rhs_binary = np.zeros(num_cities-2)
    for j in cities:
        if distances[cities.index(start_city), cities.index(j)] > 0:
            row[num_cities * cities.index(start_city) + cities.index(j)] = 1
    row = np.concatenate((row, rhs_binary))
    A_eq.append(row)
    b_eq.append(1)
    # print("A_eq:")
    # print(np.array(A_eq))

    Ae = np.vstack((A, A_eq)) # stacking all LHS of constraints together
    be = np.concatenate((b, b_eq)) # stacking all RHS of constraints together
    A_ineq = None
    b_ineq = None


    return distances, A_ineq, b_ineq, Ae, be

if __name__ == "__main__":

    distances_received, A_ineq, b_ineq, Ae, be = get_constraints('distance.csv')
    print("distances_received :")
    print(distances_received)

    print("\nEquality Constraints (Ae):")
    print(np.array(Ae))
    print("\nEquality Bounds (be):")
    print(np.array(be))
    print("Ae.shape: ", np.array(Ae).shape)

"""# **SOLVING THE INTEGER PROBLEM PROBLEM**"""

import pandas as pd
import numpy as np
import scipy.optimize as opt
from os import strerror

"""
All decision variables Xij, Yi are binaries from {0, 1}:
"""


def solve_IP(file_name: str, objective_vector):

    """
    Solves an Integer Programming (IP) problem given the data file and the objective vector.

    Args:
    - file_name (str): The name of the file containing the data.
    - objective_vector (numpy.ndarray): The objective vector for the IP problem.

    Returns:
    - objecvtive_value (float): The optimal objective value.
    - solution (numpy.ndarray): The optimal solution vector.
    """

    # The problem we will solve is:

    # min z  =  dAA*xAA +  dAB*xAB + ... + dOA*xOA + ...+ dOO*xOO + 0*yB + 0*yC + ... + 0*yN

    # s.t.    Ae x = be

    #         xAA, xAB, ... ,  xOO, yB, yC, ..., yN in {0, 1}


    # First build the objective vector ( matrix dij of distances from city i to j):
    c = objective_vector
    distances, A_ineq, b_ineq, Ae, be = get_constraints(file_name = file_name)


    # Next, create the coefficient array for the inequality constraints.
    # Note that the inequalities must be Ax <= b, so some sign
    # changes result when converting >= into <=.
    # A_ineq = None # if no inequality constraints


    # Next the right-hand-side vector for the inequalities
    # Sign changes can occur here too.
    # b_ineq = None # if no inequality constraints



    #The coefficient matrix for the equality constraints and
    # the right hand side vector.
    # Ae = None # if no equality constraints

    # be = None # if no equality constraints

    # Next, we provide any lower and upper bound vectors, one
    # value for each decision variable.  In this example all
    # lower bound are zero and there are no upper bounds.
    bounds = [(0, 1) for _ in range(num_cities**2 + num_cities - 2)] # considering added rhs_binary variables
    # print("bounds.shape = ", bounds.shape )

    # Lastly, we can specify which variables are required to be integer.
    # If no variables are integer then isint=[];  In our example, only x2 is integer.
    # isint = np.ones(num_cities + num_cities - 2)
    isint = [1 for _ in range(num_cities**2 + num_cities - 2)]
    # print("isint.shape = ", isint.shape)

    # The call to the mixed integer solver looks like the following.
    # Notice that we pass usual "c" when we have a minimization
    # problem, we send "-c" when we have max problem.
    # This is because the solver is expecting a minimization.

    res=opt.linprog(c, A_ineq, b_ineq, Ae, be, bounds, integrality = isint)

    # The result is stored in the dictionary variable "res".
    # In particular, to show the optimal objective value and the
    # optimal decision variable values:

    objecvtive_value = res['fun']
    solution = np.array(res['x'])

    return objecvtive_value, solution

if __name__ == "__main__":

    objecvtive_value, solution = solve_IP(file_name = 'delay.csv', objective_vector = p)
    print("objective vector :")
    print(d)
    print("\nmin z = ", objecvtive_value)
    print("\nat optimal solution x :")
    print(solution)

"""# **PRESENTING SOLUTIONS**"""

import pandas as pd
import numpy as np
import scipy.optimize as opt
from os import strerror

# Define lists to store the data
alfa_list = []
beta_list = []
optimal_path_list = []
cost_of_optimal_path_list = []
total_distance_list = []
delay_likelihood_list = []

def call_LP_solver(alfa: float, beta:float, file_name: str):
    """
      Solves the integer programming problem with the given alfa and beta values.

      Args:
      - alfa (float): Weighting factor for distance in the objective function.
      - beta (float): Weighting factor for delay in the objective function.
      - file_name (str): Name of the file containing distance and delay data.

      Returns:
      None

      """

    global alfa_list, beta_list, optimal_path_list, cost_of_optimal_path_list, total_distance_list, delay_likelihood_list
    # call_LP_solver does  c = alfa*distance + beta*delay as an objective vector to solve IP
    average_d = d/np.mean(d)
    average_p = p/np.mean(p)
    c = alfa*average_d + beta*average_p
    # c = alfa*d + beta*p
    objecvtive_value, solution = solve_IP(file_name = file_name, objective_vector = c)
    # print(objecvtive_value)
    # print(solution)
    # print("Optimal path in binary matrix form:")
    # print(solution[:num_cities**2].reshape(num_cities, num_cities))

    # Store the data in lists
    alfa_list.append(alfa)
    beta_list.append(beta)

    # Execute the code
    if any(solution):
        # print("Optimal path:")
        path = [start_city]  # Start from city 'A'
        path_distance = []
        next_city_index = 0  # Start from the first city in the solution vector
        while path[-1] != destination_city:  # Continue until we reach the destination city 'E'
            # Find the index of the next city with a value of 1 in the solution vector
            solution_slice = solution[next_city_index * len(cities): (next_city_index + 1) * len(cities)]
            # destination_slice = d[next_city_index * len(cities): (next_city_index + 1) * len(cities)]
            destination_slice = alfa*d[next_city_index * len(cities): (next_city_index + 1) * len(cities)] + beta*p[next_city_index * len(cities): (next_city_index + 1) * len(cities)]
            next_city_index = np.where(solution_slice == 1)[0][0]

            # print(np.dot(solution_slice, destination_slice))
            dist = str(np.dot(solution_slice, destination_slice))
            path_distance.append(dist)

            # Convert the index to the corresponding city label
            next_city = cities[next_city_index]
            path.append(next_city)

        # Print the optimal path
        print(' --> '.join(path))
        print(' + '.join(path_distance), f' = {eval("+ ".join(path_distance))}')
        # Splitting into integer and fractional parts
        int_parts = [int(float(num)) for num in path_distance]
        frac_parts = [float(num) - int(float(num)) for num in path_distance]
        # Creating integ and frac parts

        integ = ' + '.join([f'{num:.6f}' for num in int_parts])
        frac = ' + '.join([f'{num:.6f}' for num in frac_parts])
        print(integ, f' = {eval(integ)}', ' - "total" distance')
        print(frac, f' = {eval(frac)}', ' - delay likelihood')

        optimal_path_list.append(' --> '.join(path))
        # cost_of_optimal_path_list.append(' + '.join(map(str, path_distance)))
        # cost_of_optimal_path_list.append(' + '.join(path_distance) + f' = {eval("+ ".join(path_distance))}')
        cost_of_optimal_path_list.append(f'{eval("+ ".join(path_distance))}'[:4])
        # total_distance_list.append(integ + f' = {eval(integ)}')
        total_distance_list.append(f'{eval(integ)}'[:4])
        # delay_likelihood_list.append(frac + f' = {eval(frac)}')
        delay_likelihood_list.append(f'{eval(frac)}'[:9])
    else:
        # print("No solution found.")
        optimal_path_list.append("No solution found.")
        cost_of_optimal_path_list.append("No solution found.")
        total_distance_list.append("No solution found.")
        delay_likelihood_list.append("No solution found.")

if __name__ == "__main__":

    alfa = 1
    beta = 0
    file_name = 'distance.csv'
    call_LP_solver(alfa, beta, file_name)

"""# **1. Printing the solution for shortest distance part by ignoring any possible delays**"""

call_LP_solver(alfa = 1, beta = 0, file_name = 'distance.csv')

"""# **2. Printing the solution for minimum delay likelihood part by ignoring any possible long distances**"""

call_LP_solver(alfa = 0, beta = 1, file_name = 'delay.csv')

"""# **3. Printing the solution for minimizing the weighted sum of travel time and delay likelihood**"""

print("alfa*distances + beta*delays likelihood:")
alfa = float(input('alfa = '))
beta = float(input('beta = '))
file_name = 'distance.csv'
call_LP_solver(alfa = alfa, beta = beta, file_name = file_name)

print("alfa*distances + beta*delays likelihood:")
alfa = float(input('alfa = '))
# beta = float(input('beta = '))
file_name = 'distance.csv'
for beta in np.arange(0, 1.1, 0.1):
  # print(f"when alfa = {alfa}, beta = {beta} optimal path:")
  call_LP_solver(alfa = alfa, beta = beta, file_name = file_name)
  print()

print("alfa*distances + beta*delays likelihood:")
alfa = float(input('alfa = '))
# beta = float(input('beta = '))
file_name = 'distance.csv'
for beta in np.arange(0.1, 0.2, 0.01):
  # print(f"when alfa = {alfa}, beta = {beta} optimal path:")
  call_LP_solver(alfa = alfa, beta = beta, file_name = file_name)
  print()

def create_dataframe():
    # Create DataFrame from the lists
    df = pd.DataFrame({
        'alfa': alfa_list,
        'beta': beta_list,
        'optimal path': optimal_path_list,
        'cost of path': cost_of_optimal_path_list,
        'distance': total_distance_list,
        'delay': delay_likelihood_list
    })
    return df

if __name__ == "__main__":
    result_df = create_dataframe()
    print(result_df)

"""# **4. Printing the solution for the combined problem using weight selection with starting city A and ending location at city O.**

**Report about out findings and recommendations to the company:**

<p align="justify">
In conclusion, our experiments reveal that in real-life scenarios, the distances between cities remain constant, indicating that alfa is always equal to 1. By running a loop for beta within the range of [0, 1], we observe a transition in the optimal path from "A → D → B → O" to "A → D → E → O" as beta increases from 0.1 to 0.2. To gain deeper insights into the range of beta values where the optimal path changes, we conduct a secondary loop within the range of [0.1, 0.2].
Our research indicates that this transition occurs between beta = 0.16 and beta = 0.17. At beta = 0.16, the optimal path is "A → D → B → O" with a total distance of 75.0 miles and a delay likelihood of 0.008937. However, at beta = 0.17, the optimal path shifts to "A → D → E → O" with a total distance of 96.0 miles and a delay likelihood of 0.002703.

Ultimately, the choice between these two options rests on the company's resources. Opting for a shorter travel distance of 75 miles may result in a higher delay likelihood of 0.008937, whereas selecting the longer route of 96 miles offers a lower delay likelihood of 0.002703. The decision should be made considering the company's financial resources and the trade-off between travel distance and delay likelihood.
"""

# To download:
# !sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic
# !jupyter nbconvert --to pdf /content/project_all_in_one.ipynb