'''
Created on 20200702

Fixed on 20210922

@author: Zhang Yingjie
'''

from gurobipy import *
from Basics import *

ST =[(-1, 0, 0, 1, 0) ,
(0, -1, 0, 1, 0) ,
(1, 1, 0, -1, 0)]

class SIMECK_findKey():
    
    def __init__(self, N_S, M, alpha, beta):
        print(str(N_S)+" S-boxes Per Round.")
        self.N = N_S
        self.M = M
        self.alpha = alpha
        self.beta = beta
    
    
    def genVars_input_of_round(self, r):
        assert (r >= 1)
        return ['L' + str(i) + '_r' + str(r) for i in range(0, self.N)] + \
               ['R' + str(i) + '_r' + str(r) for i in range(0, self.N)]
               
    def genVars_afterAnd_of_round(self,r):
        return ['And' + str(i) + '_r' + str(r) for i in range(0, self.N)]
    
    def genVars_Copy(self,inVars,copyTime):
        return [[inVars[j]+'_C'+str(i) for j in range(0,len(inVars))] for i in range(0,copyTime)]
    
    def genVars_masterKey(self):
        masterKey = ['mk' + str(j)  for j in range(0, self.N*self.M)]
        return masterKey
    
    def genVars_roundKey(self,r):
        masterKey = self.genVars_masterKey()
        if r <= self.M:
            return masterKey[(r-1)*self.N:r*self.N]
        else:
            V = ['rk' + str(j)+'_r'+str(r)  for j in range(0, self.N)]
            return V
    
    def genConstraintsBegin(self,r):
        constraints = []
        
        XL = self.genVars_input_of_round(r)[0:self.N]
        XL_copy = self.genVars_Copy(XL, 3)
        for i in range(self.N):
            constraints = constraints + [XL[i] + ' - '+XL_copy[0][i] + ' >= 0']
            constraints = constraints + [XL[i] + ' - '+XL_copy[1][i] + ' >= 0']
            constraints = constraints + [XL[i] + ' - '+XL_copy[2][i] + ' >= 0']
        
        XL1 = Basics.leftCyclicRotation(XL_copy[0], 1) 
        XL5 = Basics.leftCyclicRotation(XL_copy[1], 5)
        XL0 = Basics.leftCyclicRotation(XL_copy[2], 0)
        
        A = self.genVars_afterAnd_of_round(r)
        XR = self.genVars_input_of_round(r)[self.N:]
        YL = self.genVars_input_of_round(r+1)[0:self.N]
        YR = self.genVars_input_of_round(r+1)[self.N:]
#         K = self.genVars_roundKey(r)
        if (r-1)>0:
            K1 = self.genVars_roundKey(r-1)
            
        for i in range(self.N):
            # AND
            constraints = constraints + [XL5[i]+' - '+A[i]+ ' >= 0']
            constraints = constraints + [XL0[i]+' - '+A[i]+ ' >= 0']
            
            # COPY
            constraints = constraints + [XL[i]+' - '+XL_copy[0][i]+ ' >= 0']
            constraints = constraints + [XL[i]+' - '+XL_copy[1][i]+ ' >= 0']
            constraints = constraints + [XL[i]+' - '+XL_copy[2][i]+ ' >= 0']
            constraints = constraints + [XL[i]+' - '+YR[i]+ ' >= 0']
            
            # XOR
            constraints = constraints + [A[i]+' - '+YL[i]+ ' >= 0']
            constraints = constraints + [XR[i]+' - '+YL[i]+ ' >= 0']
            constraints = constraints + [XL1[i]+' - '+YL[i]+ ' >= 0']
            
            # 2021-9-22 add
            if (r-1)>0:
                aa =XL_copy[1][i]
                bb = XL_copy[2][i]
                cc = XL_copy[0][i]
                kk = K1[i]
                constraints = constraints + Basics.genFromConstraintTemplate([aa,bb,cc], [kk], ST)

        return constraints
    
    def genConstraintsEnd(self,r):
        constraints = []
        
        XL = self.genVars_input_of_round(r)[0:self.N]
        XR = self.genVars_input_of_round(r)[self.N:]
        
        YL = self.genVars_input_of_round(r+1)[0:self.N]
        
        YR = self.genVars_input_of_round(r+1)[self.N:]
        
        YR_copy = self.genVars_Copy(YR, 3)
        YR1 = Basics.leftCyclicRotation(YR_copy[0], 1) # 2021-9-22 fixed
        YR5 = Basics.leftCyclicRotation(YR_copy[1], 5)
        YR0 = Basics.leftCyclicRotation(YR_copy[2], 0)
#         K = self.genVars_roundKey(r)
        K1 = self.genVars_roundKey(r+1)
        A = self.genVars_afterAnd_of_round(r)
        
        for i in range(self.N):
            # Copy
            constraints = constraints + [YR[i] + ' - '+YR_copy[0][i] + ' >= 0']
            constraints = constraints + [YR[i] + ' - '+YR_copy[1][i] + ' >= 0']
            constraints = constraints + [YR[i] + ' - '+YR_copy[2][i] + ' >= 0']
            constraints = constraints + [YR[i] + ' - '+XL[i] + ' >= 0']
        
            # AND
            constraints = constraints + [YR5[i]+' - '+A[i]+ ' >= 0']
            constraints = constraints + [YR0[i]+' - '+A[i]+ ' >= 0']
            
            # XOR
            constraints = constraints + [A[i]+' - '+XR[i]+ ' >= 0']
            constraints = constraints + [YR1[i]+' - '+XR[i]+ ' >= 0']
            constraints = constraints + [YL[i]+' - '+XR[i]+ ' >= 0']
#             constraints = constraints + [K[i]+' - '+XR[i]+ ' >= 0']
            
            # 2021-9-22 add
            aa = YR_copy[1][i]
            bb = YR_copy[2][i]
            cc = YR_copy[0][i]
            kk = K1[i]
            constraints = constraints + Basics.genFromConstraintTemplate([aa,bb,cc], [kk], ST)
            
        return constraints
    
    def genObjective(self,r1,r,r2):
        terms = []
        for i in range(1,r1+1):
            terms = terms + self.genVars_roundKey(i)
        for i in range(r1+r+1,r1+r+r2+1):
            terms = terms + self.genVars_roundKey(i)
        return Basics.plusTerm(terms)

    def genModel(self,ofile,r1,r,r2,alpha,beta):
        C = []
        V = set([])
        
        outVars = self.genVars_input_of_round(r1+1)
        for i in range(2*self.N):
            C = C+[outVars[i]+' >= '+alpha[i]]
        for i in range(1,r1+1):
            C = C + self.genConstraintsBegin(i)
        
        inVars = self.genVars_input_of_round(r1+r+1)
        for i in range(2*self.N):
            C = C+[inVars[i]+' >= '+beta[i]]
        for i in range(r1+r+1,r1+r+r2+1):
            C = C + self.genConstraintsEnd(i)
        
        V = Basics.getVariables_From_Constraints(C)
        myfile=open(ofile,'w')
        print('Minimize', file = myfile)
        print(self.genObjective(r1,r,r2), file = myfile)
        print('\n', file = myfile)
        print('Subject To', file = myfile)
        for c in C:
            print(c, file = myfile)
        print('\n', file = myfile)
        print('Binary', file = myfile)
        for v in V:
            print(v, file = myfile)
        myfile.close()

    

    def traceSol(self, f, r1,r,r2):
        F = SolFilePaser(f)
        
        print('\multirow{2}{*}{$\\bar{k}_0$}')
        for i in range(1, 3):
            x = self.genVars_roundKey(i)
            pa = F.getBitPatternsFrom(x)
            ss = []
            for j in range(len(pa)):
                if pa[j]=='1':
                    ss.append(str(j))
            print('&',i,'&','$k_{'+str(i)+'}['+','.join(ss)+']$','\\'+'\\')
        print('\hline')
        print('\multirow{'+str(r1-2)+'}{*}{$\\bar{k}_1$}')
        for i in range(3,r1+1):
            x = self.genVars_roundKey(i)
            pa = F.getBitPatternsFrom(x)
            ss = []
            for j in range(len(pa)):
                if pa[j]=='1':
                    ss.append(str(j))
            print('&',i,'&','$k_{'+str(i)+'}['+','.join(ss)+']$','\\'+'\\')
            
#             print(F.getBitPatternsFrom(x))
        print('\hline')
        print('\multicolumn{3}{c}{Approximations of '+str(r)+' rounds} \\'+'\\')
        print('\hline')
        

        print('\multirow{'+str(r2-2)+'}{*}{$\\bar{k}_2$}')
        for i in range(r1+r+1,r1+r+r2+1-2):
            x = self.genVars_roundKey(i)
            pa = F.getBitPatternsFrom(x)
            ss = []
            for j in range(len(pa)):
                if pa[j]=='1':
                    ss.append(str(j)) 
            print('&',i,'&','$k_{'+str(i)+'}['+','.join(ss)+']$','\\'+'\\')
#             print(F.getBitPatternsFrom(x))
        
        print('\hline')
        print('\multirow{2}{*}{$\\bar{k}_3$}')
        for i in range(r1+r+r2+1-2,r1+r+r2+1):
            x = self.genVars_roundKey(i)
            pa = F.getBitPatternsFrom(x)
            ss = []
            for j in range(len(pa)):
                if pa[j]=='1':
                    ss.append(str(j)) 
            print('&',i,'&','$k_{'+str(i)+'}['+','.join(ss)+']$','\\'+'\\')
 

    def traceSol_ReturnKey(self, f, r1,r,r2):
        F = SolFilePaser(f)
        outKey = []
        for i in range(1, r1+1):
            x = self.genVars_roundKey(i)
            pa = F.getBitPatternsFrom(x)
            ss = []
            for j in range(len(pa)):
                if pa[j]=='1':
                    ss.append(str(j))
            outKey.append(ss)
        for i in range(r1+r+1,r1+r+r2+1):
            x = self.genVars_roundKey(i)
            pa = F.getBitPatternsFrom(x)
            ss = []
            for j in range(len(pa)):
                if pa[j]=='1':
                    ss.append(str(j))
            outKey.append(ss)
        return outKey
    
    def countkeyBits(self,f,r1,r,r2):
        F = SolFilePaser(f)
        k0,k1,k2,k3 = 0,0,0,0
        
        for i in range(1,3):
            x = self.genVars_roundKey(i)
            xPattern = list(F.getBitPatternsFrom(x))
            for j in range(self.N):
                if (xPattern[j] == '1'):
                    k0=k0+1

        for i in range(3,r1+1):
            x = self.genVars_roundKey(i)
            xPattern = list(F.getBitPatternsFrom(x))
            for j in range(self.N):
                if (xPattern[j] == '1'):
                    k1=k1+1

        for i in range(r1+r+1,r1+r+r2+1-2):
            x = self.genVars_roundKey(i)
            xPattern = list(F.getBitPatternsFrom(x))
            for j in range(self.N):
                if (xPattern[j] == '1'):
                    k2=k2+1
        
        for i in range(r1+r+r2+1-2,r1+r+r2+1):
            x = self.genVars_roundKey(i)
            xPattern = list(F.getBitPatternsFrom(x))
            for j in range(self.N):
                if (xPattern[j] == '1'):
                    k3=k3+1
        print(k0+k1+k2+k3,'['+str(k0)+','+str(k1)+','+str(k2)+','+str(k3)+']')
        print('sum= ',k0+k1+k2+k3)