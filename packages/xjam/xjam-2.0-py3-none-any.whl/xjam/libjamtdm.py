import numpy as np
#-------------------------------------
def split(word):
    return [char for char in word]
#-------------------------------------
def cambio_de_signo(a):
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            ichar=split(a[i,j])
            if ichar[1] != '0':
                if ichar[0] == '+': a[i,j]='-'+ichar[1]
                if ichar[0] == '-': a[i,j]='+'+ichar[1]
                if (ichar[0] == '(') and (ichar[2] != ichar[4]):
                    if ichar[1] == '+': a[i,j]='(-'+ichar[2]+'+'+ichar[4]+')'
                    if ichar[1] == '-': a[i,j]='(+'+ichar[2]+'-'+ichar[4]+')'
    return a
#-------------------------------------
def conv2pseudocanonic(a):
    if a[0,0]=='*j':
        a1=np.copy(a)
        return a1
    else:
        a2=np.array(a[:,[1, 2, 0]])
        if a2[0,0]=='*j':
            return a2
        else:
            a3=np.array(a[:,[2, 0, 1]])
            return a3
#-------------------------------------
#a,b IN PSEUDO-CANONIC FORM
def ask_equivalents1(a,b,optionx):
    b1=np.copy(b)
    b4=np.array(b[:,[0, 2, 1]])
    for bi in [b1,b4]:
        if np.array_equal(a,bi): return True
    return False
#-------------------------------------
#a,b IN PSEUDO-CANONIC FORM
def ask_equivalents2(a,b,optionx):
    b0=np.copy(b)
    b1=np.flipud(b0)
    b1=conv2pseudocanonic(b1)
    b4=np.array(b1[:,[0, 2, 1]])
    if optionx in [5,6,7,8]:
        b1=cambio_de_signo(b1)
        b4=cambio_de_signo(b4)
    for bi in [b1,b4]:
        if np.array_equal(a,bi):
            return True
    return False
#-------------------------------------
def disc_equivalents(stackinglist,optionx,eqnum):
    repetidos,norepetidos=[],[0]
    for i in range(1,len(stackinglist)):
        a=stackinglist[i]
        ic=True
        for j in norepetidos:
            b=stackinglist[j]
            ans=ask_equivalents1(a,b,optionx) if eqnum==1 else ask_equivalents2(a,b,optionx)
            if ans:
                repetidos.append(i)
                ic=False
                break
        if ic: norepetidos.append(i)
    noreparraylist=[]
    for i in norepetidos:
        noreparraylist.append(stackinglist[i])  
    return noreparraylist
#-------------------------------------
def nparray2chain(a):
    lista=[''.join(j for j in a[:,i]) for i in range(3)]
    chain='/'.join(k for k in lista)
    return chain
#-------------------------------------
def chain2nparray(largechain):
    chain=largechain.split('/')
    wyckoff=[]
    for ic in chain:
        fila,cont,cond=[],0,True
        s1=split(ic)
        while cond:
            if s1[cont] != '(':
                s2=s1[cont]+s1[cont+1]
                cont=cont+2
            else:
                s2=s1[cont]+s1[cont+1]+s1[cont+2]+s1[cont+3]+s1[cont+4]+s1[cont+5]
                cont=cont+6
            fila.append(s2)
            if cont == len(s1): break
        wyckoff.append(fila)
    nparray=np.array(wyckoff)
    nparray=nparray.transpose()
    #for irow in nparray: print(irow)
    return nparray
#-------------------------------------
def allatomsx(a, atom_list):
    cj,ck,cl=0,0,0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            ichar=split(a[i,j])
            if   ichar[1] == 'j': cj=cj+1
            elif ichar[1] == 'k': ck=ck+1
            elif ichar[1] == 'l': cl=cl+1
            elif (ichar[0] == '('):
                if   ichar[2] == 'k': ck=ck+1
                if   ichar[4] == 'k': ck=ck+1
                elif ichar[4] == 'l': cl=cl+1
    allatoms=list(zip(atom_list,[cj,ck,cl]))
    return allatoms
#-------------------------------------
def build_poscarx(a,inamex,filename,z_vacuum,num_layers,d,latticep,atom_list,buckling):
    if   len(buckling)==1: bk=float(2.0)*buckling[0]
    elif len(buckling)==2: bk=sum(buckling)
    zaux=float(num_layers - 1)*d
    core=zaux + float(num_layers)*bk
    zlattice=z_vacuum + core
    zmax = 0.5 + core/(2.0*zlattice)
    zdlist,listaxyz,bkma,correcion=[],[],0.0,0.0 
    for ii in range(num_layers):
        bkplist, bkmlist = [], []
        for jj,ichar in enumerate(a[ii,:]):
            bkp, bkm = 0.0, 0.0
            if (ichar[1] != '0'):
                if   jj==0: xd,yd=0.0000000000,0.0000000000
                elif jj==1: xd,yd=0.3333333333,0.6666666667
                elif jj==2: xd,yd=0.6666666667,0.3333333333
                if len(ichar) == 2:
                    signo,letra=ichar[0],ichar[1]
                    if   letra == 'j': zi=0
                    elif letra == 'k': zi,bk=1,buckling[0]
                    elif letra == 'l': zi,bk=2,buckling[1]
                    if   signo == '*': zd=0.0
                    elif signo == '-': bkm,zd=bk,-bk/zlattice
                    elif signo == '+': bkp,zd=bk,+bk/zlattice
                    listaxyz.append([xd, yd, zd, zi, ii])
                elif len(ichar) == 6:
                    signo,letra=ichar[1],ichar[2]
                    if   letra == 'k': zi,bk=1,buckling[0]
                    elif letra == 'l': zi,bk=2,buckling[1]
                    if   signo == '-': bkm,zd=bk,-bk/zlattice
                    elif signo == '+': bkp,zd=bk,+bk/zlattice
                    listaxyz.append([xd, yd, zd, zi, ii])
                    signo,letra=ichar[3],ichar[4]
                    if   letra == 'k': zi,bk=1,buckling[0]
                    elif letra == 'l': zi,bk=2,buckling[1]
                    if   signo == '-': bkm,zd=bk,-bk/zlattice
                    elif signo == '+': bkp,zd=bk,+bk/zlattice
                    listaxyz.append([xd, yd, zd, zi, ii])
            bkplist.append(bkp)
            bkmlist.append(bkm)
        bkp=max(bkplist)
        bkm=max(bkmlist)
        ##print("%s up = %f    dn = %f" %(a[ii,:], bkp, bkm))
        correcion=correcion + bkp + bkma
        zd=zmax - (correcion + float(ii)*d)/zlattice
        zdlist.append(zd)
        bkma = bkm
    listaxdydzd=sorted(listaxyz, key=lambda x: int(x[3]))
    listaxdydzd=list([[xyz[0],xyz[1],xyz[2]+zdlist[xyz[4]],xyz[3]] for xyz in listaxdydzd])
    fopen = open(filename,'w')
    print("%s" %(inamex), file=fopen)
    print("%f" %(latticep), file=fopen)
    print("0.500000000  -0.866025403  0.000000000", file=fopen)
    print("0.500000000   0.866025403  0.000000000", file=fopen)
    print("0.000000000   0.000000000  %11.9f" %(zlattice/latticep), file=fopen)
    allatoms=allatomsx(a,atom_list)
    print(' '.join([str(item[0]) for item in allatoms if item[1] != 0]), file=fopen)
    print(' '.join([str(item[1]) for item in allatoms if item[1] != 0]), file=fopen)
    print("Direct", file=fopen)
    for ixyz in listaxdydzd:
        xd, yd, zd, si=ixyz[0],ixyz[1],ixyz[2],atom_list[ixyz[3]]
        print("%12.10f %12.10f %12.10f !%s" %(xd, yd, zd, si), file=fopen)
    fopen.close()
#-------------------------------------
