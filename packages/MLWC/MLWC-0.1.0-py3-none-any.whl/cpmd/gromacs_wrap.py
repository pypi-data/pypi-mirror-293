
def make_mdp_em(cutoff:float):
    '''
    make mdp file for energy minimization

    cutoff :: in Angstrom

    em.mdpファイルを作成する．
    '''

    # * hard code :: mdp file
    mdp_file = "em.mdp"
    cutoff_radius    = cutoff/10.0 #Ang to nm
    
    lines = [
    "; VARIOUS PREPROCESSING OPTIONS",
    ";title                    = Yo",
    ";cpp                      = /usr/bin/cpp",
    "include                  =", 
    "define                   =", 
    "    ",
    "; RUN CONTROL PARAMETERS",
    "integrator               = steep",
    "nsteps                   = 1000000",
    "emtol                    = 10",
    "emstep                   = 0.1",
    "nstlist                  = 1",
    "cutoff-scheme            = verlet",
    "vdw-type                 = cut-off",
    "rlist                    = {}".format(cutoff_radius),
    "rvdw                     = {}".format(cutoff_radius),
    "rcoulomb                 = {}".format(cutoff_radius),
    ]

    with open(mdp_file, mode='w') as f:
        f.write('\n'.join(lines))

    return 0


def make_mdp_nvt(temp,steps,dt,cutoff,nstxout:int=5):
    '''
    make mdp file for NVT run:
    run.mdpファイルを作成する．
    '''
    
    temperature      = temp
    simulation_steps = steps 
    time_step        = dt/1000.0  # ps
    cutoff_radius    = cutoff/10.0
    
    mdp_file = "run.mdp"

    lines = [
    "; VARIOUS PREPROCESSING OPTIONS",
    ";title                    = Yo",
    ";cpp                      = /usr/bin/cpp",
    "include                  =", 
    "define                   =", 
    "    ",
    "; RUN CONTROL PARAMETERS",
    "constraints              = none",
    "integrator               = md",
    "nsteps                   = {}".format(simulation_steps),
    "dt                       = {}".format(time_step),
    "nstlist                  = 1",
    "rlist                    = {}".format(cutoff_radius),
    "rvdw                     = {}".format(cutoff_radius),
    "rcoulomb                 = {}".format(cutoff_radius),
    "coulombtype              = pme",
    "cutoff-scheme            = verlet",
    "vdw-type                 = cut-off",        
    "tc-grps                  = system",
    "tau-t                    = 0.1",
    "gen-vel                  = yes",
    "gen-temp                 = {}".format(temperature),
    "ref-t                    = {}".format(temperature),
    "Pcoupl                   = no",
    "Tcoupl                    = v-rescale " , # 温度制御．
    "nstenergy                = {}".format(nstxout), # 何ステップごとにデータを出力するか．
    "nstxout                  = {}".format(nstxout), # 何ステップごとにデータを出力するか
    "nstfout                  = {}".format(nstxout), # 何ステップごとにデータを出力するか
    "DispCorr                 = EnerPres",
    ]

    with open(mdp_file, mode='w') as f:
        f.write('\n'.join(lines))
    return 0

def build_mixturegro(num_molecules:float,density:float,gro_filename:str="input1.gro"):
    '''
    making mixture.gro from input1.gro
    * ここではむしろ分子数をinputにした．
    '''
    import os
    # check whether input files exist.
    if not os.path.isfile(gro_filename):
        print(" ERROR :: "+str(gro_filename)+" does not exist !!")
        print(" ")
        return 1

    # import pandas as pd
    
    import MDAnalysis as mda

    #混合溶液を作成
    import mdapackmol
    import numpy as np
    from ase import units
    import shutil

    # load individual molecule files
    mol1 = mda.Universe(gro_filename)
    total_mol = num_molecules
    num_mols1 = total_mol
    print(" --------- ")
    print(" num_mol1(total_num_molecules) :: {0} ".format(num_mols1))
    print(" --------- ")
    
    # 質量を計算
    mw_mol1 = np.sum(mol1.atoms.masses)
    total_weight = num_mols1 * mw_mol1 
    
    # Determine side length of a box from the density of mixture 
    #L = 12.0 # Ang. unit 
    d = density / 1e24 # Density in g/Ang3 
    volume = (total_weight / units.mol) / d
    L = volume**(1.0/3.0)
    print(" --------------      ")
    print(" print parameters ...")
    print(" CELL PARAMETER(nm) :: ", L/10)
    print(" VOLUME(Ang^3)      :: ", volume)

    # 複数分子を含む系を作成する．（mdapackmolはMDAnalysisとpackmolのwrapperらしい．）
    print(" ")
    print(" making first cell via mdapackmol...")
    print(" ")
    system = mdapackmol.packmol(
    [ mdapackmol.PackmolStructure(
    mol1, number=num_mols1,
    instructions=["inside box "+str(0)+"  "+str(0)+"  "+str(0)+ "  "+str(L)+"  "+str(L)+"  "+str(L)]),])

    # 作成した系（system）をmixture.groへ保存
    system.atoms.write('mixture.gro')
    # bug-fix issue #17  
    import gc 
    del system 
    gc.collect() 
    #
    return L,num_mols1



def build_mixturegro_fixlattice(num_molecules:float,latticeconstant:float,gro_filename:str="input1.gro"):
    '''
    making mixture.gro from input1.gro
    * ここではむしろ分子数をinputにした．
    * fixlatticeでは，密度から格子定数を計算せずに，手で入れた格子定数で固定して計算する．
    latticeconstant:Angstrom
    '''
    import os
    # check whether input files exist.
    if not os.path.isfile(gro_filename):
        print(" ERROR :: "+str(gro_filename)+" does not exist !!")
        print(" ")
        return 1

    # import pandas as pd
    
    import MDAnalysis as mda

    #混合溶液を作成
    import mdapackmol
    import numpy as np
    from ase import units
    import shutil

    # load individual molecule files
    mol1 = mda.Universe(gro_filename)
    total_mol = num_molecules
    num_mols1 = total_mol
    print(" --------- ")
    print(" num_mol1(total_num_molecules) :: {0} ".format(num_mols1))
    print(" --------- ")
    
    # 質量を計算
    mw_mol1 = np.sum(mol1.atoms.masses)
    total_weight = num_mols1 * mw_mol1 
    
    # Determine side length of a box from the input variable latticeconstant
    L = latticeconstant
    volume = L*L*L
    print(" --------------      ")
    print(" print parameters ...")
    print(" CELL PARAMETER(nm) :: ", L/10)
    print(" VOLUME(nm^3)      :: ", volume)

    # 複数分子を含む系を作成する．（mdapackmolはMDAnalysisとpackmolのwrapperらしい．）
    print(" ")
    print(" making first cell via mdapackmol...")
    print(" ")
    system = mdapackmol.packmol(
    [ mdapackmol.PackmolStructure(
    mol1, number=num_mols1,
    instructions=["inside box "+str(0)+"  "+str(0)+"  "+str(0)+ "  "+str(L)+"  "+str(L)+"  "+str(L)]),])

    # 作成した系（system）をmixture.groへ保存
    system.atoms.write('mixture.gro')
    return L,num_mols1


def build_initgro(L:float):
    """take mixture.gro as input, output init.gro

    Args:
        L (float): Lattice parameter in Angstrom

    Returns:
        _type_: _description_
    """
    #混合溶液を作成
    import mdapackmol
    import numpy as np
    from ase import units
    import shutil

    import os
    os.environ['GMX_MAXBACKUP'] = '-1'

    # for gromacs-5 or later (init.groを作成)
    # gmx editconf converts generic structure format to .gro, .g96 or .pdb.
    print(" build_initgro:: RUNNING :: gmx editconf ... ( making init.gro) ")
    os.system(f"gmx editconf -f mixture.gro  -box {L/10.0} {L/10.0} {L/10.0} -o init.gro")
    print(" ----------- ")
    print(" FINISH gmx editconf :: made init.gro")
    print(" ")
    return 0


def build_initial_cell_gromacs(dt,eq_cutoff,eq_temp,eq_steps,num_molecules:float,density:float,gro_filename:str="input1.gro",itp_filename:str="input1.itp",nstxout:int=5,iffixlattice:bool=False):
    '''
    gro_filename:: input用のgroファイル名
    itp_filename:: input用のitpファイル名
    iffixlattice=trueの時はdensityのところにL（Ang）を入れる．
    '''
    
    import os
    # check whether input files exist.
    if not os.path.isfile(gro_filename):
        print(" ERROR :: "+str(gro_filename)+" does not exist !!")
        print(" ")
        return 1
    if not os.path.isfile(itp_filename):
        print(" ERROR :: "+str(itp_filename)+" does not exist !!")
        print(" ")
        return 1
    
    # 最初のセルを作成（iffixlattice=trueの時は固定値で）
    if iffixlattice:
        print(" FIXLATTICE mode is actiated !!")
        inputlatticeconstant=density
        L,num_mols1=build_mixturegro_fixlattice(num_molecules,inputlatticeconstant,gro_filename)
    else:
        L,num_mols1=build_mixturegro(num_molecules,density,gro_filename)
    
    # import pandas as pd
    
    import time 
    init_time = time.time()
    
    dt = dt

    import MDAnalysis as mda
#    from nglview.datafiles import PDB, XTC # これ，使ってなくない？

    #混合溶液を作成
    import mdapackmol
    import numpy as np
    from ase import units
    import shutil

    import os 
    os.environ['GMX_MAXBACKUP'] = '-1'

    # for gromacs-5 or later (init.groを作成)
    build_initgro(L)

    #make top file for GAFF
    top_file = "system.top"
    mol_name1 = "input"
 
    lines = [
        "; input_GMX.top created by acpype (v: 2020-07-25T09:06:13CEST) on Fri Jul 31 07:59:08 2020",
        ";by acpype (v: 2020-07-25T09:06:13CEST) on Fri Jul 31 07:59:08 2020",
        "   ",
        "[ defaults ]",
        "; nbfunc        comb-rule       gen-pairs       fudgeLJ fudgeQQ",
        "1               2               yes             0.5     0.8333",
        "    ",
        "; Include input.itp topology", 
        "#include \"{}\"".format(itp_filename), # * hard code :: input1.itpに固定されている．
        "    ",
        "[ system ]",
        "input",
        "     ",
        "[ molecules ]",
        "; Compound        nmols" ,
        mol_name1 + "          {} ".format(num_mols1), 
    ]
    
    with open(top_file, mode='w') as f:
        f.write('\n'.join(lines))

    # Energy minimization
    import os
    print(" -----------")
    print(' Minimizing energy')
    print(" ")
    
    os.environ['GMX_MAXBACKUP'] = '-1'

    # make mdp em ?
    make_mdp_em(eq_cutoff)

    # ============  ここからgromacsの実行なので，分けた方が良いな．．．
    #grompp
    os.environ['OMP_NUM_THREADS'] = '1'    
    os.system("gmx grompp -f em.mdp -p system.top -c init.gro -o em.tpr -maxwarn 10 ")
    print(" ")
    print(" FINISH gmx grompp :: made em.tpr")
    print(" ")
    
    #mdrun for Equilibration
    os.environ['OMP_NUM_THREADS'] = '1' 
    os.system("gmx mdrun -s em.tpr -o em.trr -e em.edr -c em.gro -nb cpu")
    print(" ")
    print(" FINISH gmx mdrun for Equilibration :: made em.trr")
    print(" ")

    # nvt計算用のinputを作成する．
    temp = eq_temp
    dt   = dt 
    steps = eq_steps
    make_mdp_nvt(temp,steps,dt,eq_cutoff,nstxout)

    #grompp (入力ファイルを作成)
    os.environ['OMP_NUM_THREADS'] = '1'
    os.system("gmx grompp -f run.mdp -p system.top -c em.gro -o eq.tpr -maxwarn 10 ".format(str(temp)))
    print(" ")
    print(" FINISH gmx grompp")
    print(" ")
  
    #mdrun (eq.groを作成)
    # !! 2023/5/31 念の為gmx mdrunの並列数を4に抑える．．．
    os.environ['OMP_NUM_THREADS'] = '1' 
    os.system("gmx mdrun -nt 4 -s eq.tpr -o eq.trr -e eq.edr -c eq.gro -nb cpu")
    print(" ")
    print(" FINISH gmx mdrun ")
    print(" ")
    
    print(" ------------- ")
    print(" summary")
    print(" elapsed time= {} sec.".format(time.time()-init_time))
    print(" ")
    return 0


def build_initial_cell_gromacs_fugaku(dt,eq_cutoff,eq_temp,eq_steps,num_molecules:float,density:float,gro_filename:str="input1.gro",itp_filename:str="input1.itp",nstxout:int=5,iffixlattice:bool=False):
    '''
    gro_filename:: input用のgroファイル名
    itp_filename:: input用のitpファイル名
    iffixlattice=trueの時はdensityのところにL（Ang）を入れる．
    '''
    
    import os
    # check whether input files exist.
    if not os.path.isfile(gro_filename):
        print(" ERROR :: "+str(gro_filename)+" does not exist !!")
        print(" ")
        return 1
    if not os.path.isfile(itp_filename):
        print(" ERROR :: "+str(itp_filename)+" does not exist !!")
        print(" ")
        return 1

    # 最初のセルを作成（iffixlattice=trueの時は固定値で）
    if iffixlattice:
        print(" FIXLATTICE mode is actiated !!")
        inputlatticeconstant=density
        L,num_mols1=build_mixturegro_fixlattice(num_molecules,inputlatticeconstant,gro_filename)
    else:
        L,num_mols1=build_mixturegro(num_molecules,density,gro_filename)

    print(" ======================== ")    
    print(f" Lattice parameter = {L}")
    print(f" num_mols1         = {num_mols1}")
    print(" ======================== ")    

    
    # import pandas as pd
    
    import time 
    init_time = time.time()
    
    dt = dt

    import MDAnalysis as mda
#    from nglview.datafiles import PDB, XTC # これ，使ってなくない？

    #混合溶液を作成
    import mdapackmol
    import numpy as np
    from ase import units
    import shutil

    import os 
    os.environ['GMX_MAXBACKUP'] = '-1'

    # for gromacs-5 or later (init.groを作成)
    build_initgro(L)

    #make top file for GAFF
    top_file = "system.top"
    mol_name1 = "input"
 
    lines = [
        "; input_GMX.top created by acpype (v: 2020-07-25T09:06:13CEST) on Fri Jul 31 07:59:08 2020",
        ";by acpype (v: 2020-07-25T09:06:13CEST) on Fri Jul 31 07:59:08 2020",
        "   ",
        "[ defaults ]",
        "; nbfunc        comb-rule       gen-pairs       fudgeLJ fudgeQQ",
        "1               2               yes             0.5     0.8333",
        "    ",
        "; Include input.itp topology", 
        "#include \"{}\"".format(itp_filename), # * hard code :: input1.itpに固定されている．
        "    ",
        "[ system ]",
        "input",
        "     ",
        "[ molecules ]",
        "; Compound        nmols" ,
        mol_name1 + "          {} ".format(num_mols1), 
    ]
        
    with open(top_file, mode='w') as f:
        f.write('\n'.join(lines))

    # Energy minimization
    import os

    # make mdp em ?
    make_mdp_em(eq_cutoff)

    # nvt計算用のinputを作成する．
    temp = eq_temp
    dt   = dt 
    steps = eq_steps
    make_mdp_nvt(temp,steps,dt,eq_cutoff,nstxout)

    return 0




def make_gro_for_qeinput():
    import sys
    import mdtraj
    # ParmEd Imports
    # from parmed import load_file
    # from parmed.openmm.reporters import NetCDFReporter
    # from parmed import unit as u
    
    #analysis
    import os
    
    print(" ------- ")
    print(" make inputs/ directory")
    print(" ")
    os.system("mkdir inputs/")
    os.system('echo "System" > ./inputs/anal.txt')
    
    os.system("gmx trjconv -s eq.tpr -f eq.trr -dump 0 -o eq.pdb < ./inputs/anal.txt")
    print(" -------- ")
    print(" FINISH gmx trajconv to make eq.pdb")
    print(" ")
    
    os.system("gmx trjconv -s eq.tpr -f eq.trr -pbc mol -force -o eq_pbc.trr < ./inputs/anal.txt")
    print(" -------- ")
    print(" FINISH gmx trajconv to make eq_pbc.trr")
    print(" ")
    
    #
    import mdtraj
    traj=mdtraj.load("eq_pbc.trr", top="eq.pdb")
    
    # トラジェクトリの最後をfinal_structure.groというファイル名で保存．
    traj[-1].save_gro("final_structure.gro")
    # atoms1 = ase.io.read('temp.gro')
    return 0


def make_gro_for_qeinput_fugaku():

    '''
    ファイルの変換をやるだけのversion．
    gromacsを避ける方法．
    '''
    #
    import mdtraj
    traj=mdtraj.load("eq_pbc.trr", top="eq.pdb")
    
    # トラジェクトリの最後をfinal_structure.groというファイル名で保存．
    traj[-1].save_gro("final_structure.gro")
    # atoms1 = ase.io.read('temp.gro')
    return 0
