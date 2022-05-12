# MILP-based-Automatic-Key-Recovery-of-Feistel-Ciphers
The code of paper “Automatic Key Recovery of Feistel Ciphers: Application to SIMON and SIMECK” in ISPEC 2021
https://link.springer.com/chapter/10.1007/978-3-030-93206-0_10

Install:
- First, install python 3.x, anaconda,gurobi;
- Then, use anaconda to install gurobipy in python.

Download:
```
git clone git@github.com:zhangyingjie7/MILP-based-Automatic-Key-Recovery-of-Feistel-Ciphers.git
```
- Basics.pyd: some basic functions that can be used as black box. Including:
    - Basics.wordToBinaryString(word, size) # (0xF1, 8) -> '11110001'
    - Basics.ruduceTerm(Term) # ['a','a','b'] -> ['a','b']
    - Basics.leftCyclicRotation(in_vars, offset) # (['a','b','c'],1) -> ['b','c','a']
    - Basics.rightCyclicRotation(in_vars, offset) # (['a','b','c'],1) -> ['c','a','b']
    - Basics.plusTerm(in_vars) # ['a','b','c'] -> 'a+b+c'
    - Basics.getVariables_From_Constraints(C) # ['a+b=1','c+b=4'] -> {a,b,c}
    - Basics.genFromConstraintTemplate(in_vars, out_vars, ineq_template) # (['x0', 'x1'], ['y0'], [(-1, 2, 3, 1), (1, -1, 0, -2)] ) ->
            ['-1 x0 + 2 x1 + 3 y0 >= - 1', '1 x0 - 1 x1 + 0 y0 >= 2']
    - SolFilePaser.getBitPatternsFrom(vars_sequence) # get the string of values of vars in vars_sequence
- findKey_SIMON.py: functions to find the guessed keys of SIMON
- findKey_SIMECK.py: functions to find the guessed keys of SIMECK
- key.lp: MILP model
- key.sol: solution of the MILP model


Run:
```
python main.py
```
