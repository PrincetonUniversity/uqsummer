import numpy as npy

def get_npc(dims,order):
    if dims < 1 or order < 0:
        print "get_npc() unexpected dims/order values: ",dims,order,", -> Abort !"
        quit()
    nterms=1;
    if order == 0: return nterms;
    for i in range(order):
        nterms = nterms*(dims+order-i)
    for i in range(order):
        nterms = nterms/(order-i)
    return nterms

def compute_err(type,arr1,arr2):
    if ( len(arr1) != len(arr2) ):
        print "compute_err(): lengths of arr1,arr2 do not match:",len(arr1),len(arr2)
        quit()
    if type == "Linf":
        return abs(arr1-arr2).max()
    elif type == "Linfrel":
        return (abs(arr1-arr2).max())/abs(arr1).max()
    elif type == "L1":
        return npy.average(abs(arr1-arr2))
    elif type == "L1rel":
        return npy.average(abs(arr1-arr2))/abs(arr1).max()
    elif type == "L2":
        return npy.sqrt(npy.dot(arr1-arr2,arr1-arr2)/len(arr1))
    elif type == "L2rel":
        return npy.sqrt(npy.dot(arr1-arr2,arr1-arr2)/npy.dot(arr1,arr1))
    else:
        print "compute_err(): unknown method (use Linf, L1, L2, Linfrel, L1rel, L2rel) -> exit"
        quit()

