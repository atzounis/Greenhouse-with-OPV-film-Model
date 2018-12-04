# The modeling and optimization code for my graduate research "Modeling and Optimization of crop production and energy generation for economic profit in an organic photovoltaics integrated greenhouse" by Kensaku Okada, Murat Kacira, Young-Jun Son, Lingling An

This simulation program was developed for my graduate reserach. The simulator estimates the overall economic profit of lettuce crop production in a greenhouse integrated with OPV film as part of the greenhouse cover. The model calculated the solar irradiance to a tilted surface, electric energy generated by OPV modules installed on greenhouse roof, transmittance through multi-span greenhouse roof, solar irradiance to lettuce in the greenhouse, the growth of lettuce yield, energy consumed by cooling and heating, cost and sales of electric energy and lettuce respectively, and finally the total economic profit. It enables evaluating various organic PV coverage ratios as well as traditional inorganic PV module by changing the model specification.

MIDACO solver (http://www.midaco-solver.com/) was adopted for the optimization. It solved mixed integer non-linear programming (MINLP) problem by combining an extended evolutionary Ant Colony Optimization (ACO) algorithm with the Oracle Penalty Method for constrained handling.

# Big picture of the simulator:
![fig 2](https://user-images.githubusercontent.com/6435299/45592781-d9d89580-b9b1-11e8-9433-6ff1bba15c25.png)



# Optimization model:
![image](https://user-images.githubusercontent.com/6435299/49426796-f46a2000-f7e4-11e8-836a-3148a503497d.png)


# How to run the simulator

<li>Open SimulatorMain.py</li>
<li>If you want to run the model only with the manually defined values, let case = "OneCaseSimulation" at Line 22 </li>
<li>If you want to iterate the simulation only with different OPV coverage ratio, let case = "OptimizeOnlyOPVCoverageRatio" at Line 23 </li>
<li>If you want to optimize the parameters (OPV coverage ratio, Summer period start date, Summer period end date) with the model using MIDACO Solver, let case = "OptimizationByMINLPSolver" at Line 24 (This option needs MIDACO solver (http://www.midaco-solver.com/) paid license. Please purchase it at the website and crease a new folder called MIDACO having the dll file you gonna get). </li>

Please claim issues if you face any problem in the program.
