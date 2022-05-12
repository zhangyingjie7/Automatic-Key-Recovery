from findKey_SIMON import*
from findKey_SIMECK import*

def main(cipher,n,k_len,alpha,beta,ofile,solfile,r1,r,r2):
    alpha_binary = list(Basics.wordToBinaryString(alpha, n))
    beta_binary = list(Basics.wordToBinaryString(beta,n))
    if cipher == "SIMON":
        Test = SIMON_findKey(n//2,2*k_len//n,alpha_binary,beta_binary)
    elif cipher == "SIMECK":
        Test = SIMON_findKey(n//2,2*k_len//n,alpha_binary,beta_binary)
    else:
        print("Wrong cipher name")
        
    Test.genModel(ofile, r1, r, r2, alpha_binary, beta_binary)
    model = read(ofile)
    model.optimize()
    model.write(solfile)
    print("--------------------------------------------------------------------------")
    Test.countkeyBits(solfile, r1, r, r2) # Print the number of guessed subkeys
    print("--------------------------------------------------------------------------")
    outkey = Test.traceSol_ReturnKey(solfile, r1, r, r2) # Print the guessed subkeys
    for v in outkey:
        print(v)
    print("--------------------------------------------------------------------------")
    Test.traceSol(solfile, r1, r, r2) # Print latex version of the guessed subkeys
    print("--------------------------------------------------------------------------")    



if __name__ == '__main__':
    cipher,n,k_len,alpha,beta,ofile,solfile,r1,r,r2 = "SIMON",64,96, 0x4000000400000001,0x1000000044000004,'key.lp','key.sol',4,23,4
    main(cipher,n,k_len,alpha,beta,ofile,solfile,r1,r,r2)

    cipher,n,k_len,alpha,beta,ofile,solfile,r1,r,r2 = "SIMECK",48,96, 0x800000000001,0x200000500001,'key.lp','key.sol',5,22,4
    main(cipher,n,k_len,alpha,beta,ofile,solfile,r1,r,r2)    