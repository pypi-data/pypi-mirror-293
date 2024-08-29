import os
import sys
#------------------------------------------------------------------------------------------
inputjamfile='JAM.inp'
#-------------------------------------
def is_number(s):
    try:
        float(s).is_integer()
        return True
    except ValueError:
        pass
#-------------------------------------
def get_a_int(strchain):
    if os.path.isfile(inputjamfile):
        inputfile=open(inputjamfile,"r")
        for line in inputfile:
            line=line.strip(' \t\n\r')
            if len(line.strip()) != 0 :
                li = line.lstrip()
                if not li.startswith("#"):
                    readline=line.split()
                    if len(readline) == 2:
                        data0=readline[0].strip('\t\n\r') 
                        data1=readline[1].strip('\t\n\r')
                        if data0 == str(strchain):
                            if is_number(data1):
                                finalvalue=int(data1)
                                return finalvalue
                            else:
                                print('%s is not a number' %(strchain))
                                return False
        inputfile.close()
    print('%s is not specified.' %(strchain))
    return False
#-------------------------------------
def get_str_list(strchain):
    if os.path.isfile(inputjamfile):
        inputfile=open(inputjamfile,"r")
        for line in inputfile:
            line=line.strip(' \t\n\r')
            if len(line.strip()) != 0 :
                li = line.lstrip()
                if not li.startswith("#"):
                    readline=line.split()
                    data0=readline[0].strip('\t\n\r') 
                    if data0 == str(strchain):
                        del readline[0]
                        data1=[str(item) for item in readline]
                        finalvalue=data1
        inputfile.close()
    return finalvalue
#-------------------------------------
def get_a_float(strchain):
    if os.path.isfile(inputjamfile):
        inputfile=open(inputjamfile,"r")
        for line in inputfile:
            line=line.strip(' \t\n\r')
            if len(line.strip()) != 0 :
                li = line.lstrip()
                if not li.startswith("#"):
                    readline=line.split()
                    if len(readline) == 2:
                        data0=readline[0].strip('\t\n\r') 
                        data1=readline[1].strip('\t\n\r')
                        if data0 == str(strchain):
                            if is_number(data1):
                                finalvalue=float(data1)
                                return finalvalue
                            else:
                                print('%s is not a number' %(strchain))
                                return False
        inputfile.close()
    print('%s is not specified.' %(strchain))
    return False
#-------------------------------------
def get_float_list(strchain):
    if os.path.isfile(inputjamfile):
        inputfile=open(inputjamfile,"r")
        for line in inputfile:
            line=line.strip(' \t\n\r')
            if len(line.strip()) != 0 :
                li = line.lstrip()
                if not li.startswith("#"):
                    readline=line.split()
                    data0=readline[0].strip('\t\n\r') 
                    if data0 == str(strchain):
                        del readline[0]
                        data1=[float(item) for item in readline]
                        finalvalue=data1
        inputfile.close()
    return finalvalue
#-------------------------------------
longstring_authors = """# JAM 2.0
# Joining and Arrangement of Multilayers (JAM)
# Jessica Arcudia, Filiberto Ortiz-Chi, and Gabriel Merino
#
# Departamento de Fisica Aplicada,
# Centro de Investigacion y de Estudios Avanzados, Unidad Merida,
# Km 6 Antigua Carretera a Progreso, A.P. 73, Cordemex, 97310 Merida, Yucatan, Mexico
"""
#-------------------------------------
longstring_options = """#
# Options:
# 1. Planar (PL)
# 2. Binary planar (BPL)
# 3. Buckled (BU)
# 4. Binary  Buckled (BBU)
# 5. Binary  Buckled 1HPhase  
# 6. Binary  Buckled 1TPhase  
# 7. Ternary Buckled 1HPhase
# 8. Ternary Buckled 1TPhase
"""
#-------------------------------------
longstring_ex1 = """#
option       1
num_layers   5
poscargen    T
atom_list    C
latticep     2.46
z_vacuum     20.0
buckling     0.0
distance     3.0
"""
#-------------------------------------
longstring_ex2 = """#
option       2
num_layers   5
poscargen    T
atom_list    B N
latticep     2.5
z_vacuum     20.0
buckling     0.0
distance     3.0
"""
#-------------------------------------
longstring_ex3 = """#
option       3
num_layers   5
poscargen    T
atom_list    P
latticep     3.27
z_vacuum     20.0
buckling     1.2
distance     3.0
"""
#-------------------------------------
longstring_ex4 = """#
option       4
num_layers   4
poscargen    T
atom_list    As P
latticep     3.6
z_vacuum     20.0
buckling     1.4
distance     3.0
"""
#-------------------------------------
longstring_ex5 = """#
option       5
num_layers   5
poscargen    T
atom_list    Mo S 
latticep     3.3
z_vacuum     20.0
buckling     1.5
distance     3.6
"""
#-------------------------------------
longstring_ex6 = """#
option       6
num_layers   5
poscargen    T
atom_list    Mo S
latticep     3.3
z_vacuum     20.0
buckling     1.5
distance     3.6
"""
#-------------------------------------
longstring_ex7 = """#
option       7
num_layers   4
poscargen    T
atom_list    Mo S Se
latticep     3.3
z_vacuum     20.0
buckling     1.5 1.65
distance     3.6
"""
#-------------------------------------
longstring_ex8 = """#
option       8
num_layers   4
poscargen    T
atom_list    Mo S Se
latticep     3.30
z_vacuum     20.0
buckling     1.5 1.65
distance     3.6
"""
#-------------------------------------
longstring_exx="""
x.jam --ex1
x.jam --ex2
x.jam --ex3
x.jam --ex4
x.jam --ex5
x.jam --ex6
x.jam --ex7
x.jam --ex8
"""
#-------------------------------------
def get_inputfile():
    if not os.path.isfile(inputjamfile):
        args=sys.argv[1:]
        if len(args) < 1:
            print(longstring_authors)
            print(longstring_options)
            print("# %s do not found !!!" %(inputjamfile))
            print("# Build a valid %s file. You can try:" %(inputjamfile))
            print(longstring_exx)
            sys.exit()
        elif sys.argv[1] == "--ex1":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex1)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex2":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex2)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex3":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex3)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex4":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex4)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex5":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex5)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex6":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex6)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex7":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex7)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        elif sys.argv[1] == "--ex8":
            exfile = open(inputjamfile, "w")
            exfile.write(longstring_options)
            exfile.write(longstring_ex8)
            exfile.close()
            print("Edit the %s file and re-run: x.jam" %(inputjamfile))
        else:
            print('# Error in choose an example, try again please:')
            print(longstring_exx)
        sys.exit()
    else:
        return 
#------------------------------------------------------------------------------------------
