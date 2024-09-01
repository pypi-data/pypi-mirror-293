# -*- coding: utf-8 -*-
"""
convert WANNIER_CENTER to List of ase.atoms.
!! To read the unitcell vectors, We need std-output. (function from read_traj_cpmd)
"""

# 座標：wfcファイル
# 格子定数：他のファイルが必要
# WCsの数．：wfcファイルから取得可能．
    
from ase.io import read
import ase
import sys
import numpy as np
from types import NoneType
from cpmd.read_traj import raw_read_unitcell_vector
import cpmd.read_traj_cpmd
import cpmd.read_traj
import cpmd.read_core



def raw_cpmd_get_nbands(filename:str)->int:
    '''
    CPMDの作るTRAJECTORYファイルの最初のconfigurationを読み込んでWCsがいくつあるかをcount_lineで数える.
    get_nbandsと似た関数
    '''
    count_line:int=0
    check_line:int=0
    f = open(filename)

    while True:
        data = f.readline()
        count_line+=1
        if count_line == 1: # 1行目の時のtimestepを取得
            timestep:int = data.split()[0]
        if data.split()[0] == timestep: 
            check_line+=1
        else:
            break

    numatoms:int = count_line-1
    if not __debug__:
        print(" -------------- ")
        print(" finish reading nbands :: num WCs = ", numatoms)
        print("")
    return numatoms




def raw_cpmd_read_wfc(filename:str, wannier_reference:np.array):
    '''
    *.wfcファイルを読みこんでase.atomsのリストを返す.

    input
    ----------------
      - filename        :: str
            *.wfc filename
      - UNITCELL_VECTOR :: 3*3 numpy array --> DEPLICATE
            unitcell vectors in row wise
      - ifsave          :: bool -- > DEPLECATE
            if True, save trajectory to *.xyz and *.traj.

    Returns
    -------
      - wfc_list     :: list of atoms.ase

    Notes
    -----
    格子定数は与えなくても良い．その場合格子定数を保持しないatoms.aseとして出力される．
    '''

    print(" ")
    print(" --------  WARNING from raw_cpmd_read_wfc -------- ")
    print(" Please check you are correct inputs (WANNIER_CENTER) ")
    print(" This code does not check inputs format... ")
    print(" ")
    
    
    f   = open(filename, 'r') # read TRAJECTORY/FTRAJECTORY

    # nbands(wfcの数)を取得
    nbands=raw_cpmd_get_nbands(filename)
    
    # wfcのリスト 
    wfc_list = []

    with open(filename) as f:
        lines = f.read().splitlines()

    lines = [l.split() for l in lines] #
    for i,l in enumerate(lines) :
        if (i%(nbands) == 0) and (i==0) : #初めの行
            block = []
            block.append([float(l[1]), float(l[2]), float(l[3]) ])
        elif i%(nbands) == 0 : # numatom+1の時にpos_listとtimeにappend
            wfc_list.append(block)
            block = []
            block.append([float(l[1]), float(l[2]), float(l[3]) ])           
        else : #numatom個の座標を読み込み
            block.append([float(l[1]), float(l[2]), float(l[3]) ])
    # append final step
    wfc_list.append(block)

    # convert from bohr to Ang
    wfc_list = np.array(wfc_list) * ase.units.Bohr #wfcはbohr. Angへ変換

    
    # Atomsオブジェクトのリストを作成する
    wfc_array=[]

    # He原子を割り当てる
    new_atomic_num=["He" for i in range(nbands)]

    # 座標のリスト（2022/11/24: 原点を移動する．）
    new_coord=wfc_list+wannier_reference

    
    # ase.atomsのリストを作成
    for i in range(len(wfc_list)):
        mol_with_WC = ase.Atoms(new_atomic_num,
                                positions=new_coord[i],        
                                pbc=[0, 0, 0])  
        wfc_array.append(mol_with_WC)
            
    # traj形式で保存
    #if ifsave == True:
    #    ase.io.write(filename+"_refine.xyz",wfc_array, format="extxyz")
    #    ase.io.write(filename+"_refine.traj",wfc_array, format="traj")
    # ase.atomsのリストを返す
    return wfc_array


# def raw_merge_wfc_xyz(wfc_list:list, xyz_list:list):
#     '''
#     同じtrajectoryから得られたwfcのデータとxyzのデータを合体させて新しいase.atomsリストを作成する．
#     入力はどちらもextended xyzであることを想定している．

#     input
#     ----------------
#       - wfc_list :: ase.atoms list
#            input wfc list
#       - xyz_list :: ase.atoms list
#            input xyz list
#     '''
#     # まず与えられた二つのファイルの長さが同じか判定
#     if not len(wfc_list) == len(xyz_list):
#         print("ERROR :: steps of 2 files differ")
#         print(" steps of wfc_list :: ", len(wfc_list))
#         print(" steps of xyz_list :: ", len(xyz_list))
#         sys.exit()
    
#     # 原子リスト(trajectoryの最初のconfigurationから原子種を取得)
#     MERGE_SYMBOL_LIST=wfc_list[0].get_chemical_symbols()+xyz_list[0].get_chemical_symbols()

#     # 結晶ベクトルはxyzから取得
#     UNITCELL_VECTOR=xyz_list[0].get_cell()
    
#     merged_atoms_list=[]
    
#     for i in range(len(wfc_list)):
#         # step iでのatomsを作成. MERGE_SYMBOL_LISTと同じくwfc→xyzの順番でappendする．
#         tmp_positions=[]
#         for j in range(len(wfc_list[i].get_positions())):
#             tmp_positions.append(wfc_list[i].get_positions()[j])

#         for j in range(len(xyz_list[i].get_positions())):
#             tmp_positions.append(xyz_list[i].get_positions()[j])
#         # atomsを作成
#         tmp_atoms = ase.Atoms(MERGE_SYMBOL_LIST,
#                               positions=tmp_positions,        
#                               cell= UNITCELL_VECTOR,
#                               pbc=[1, 1, 1])  
#         merged_atoms_list.append(tmp_atoms)

#     # traj形式で保存
#     #if ifsave == True:
#     #    if prefix == None:
#     #        print(" WARNING :: prefix is not given. \n")
#     #        print(" prefix is used for output filenames. \n")
#     #    ase.io.write(prefix+"_wfc_merged.traj",merged_atoms_list, format="traj")
#     #    ase.io.write(prefix+"_wfc_merged.xyz",merged_atoms_list, format="extxyz")
#     #    merged_atoms_traj=ase.io.trajectory.Trajectory(prefix+"_wfc_merged.traj")
#     #
#     return merged_atoms_list
            


class ReadWFC(cpmd.read_core.custom_traj):
    '''
    *.wfcファイルを読み込んで操作するクラス．
    オプションとしてcppp.xの作るxyzファイルをxyzfilenameを与えればそこから格子定数を読み込んで付加することができる．
    wfcファイルのみを可視化したい場合にはこれがあると便利．
    custom_trajクラスを継承して作成しているので細かい関数などについてはそちらも参照すること．
    
    input
    -----------------
      - filename    :: str
            original wfc file from cp.x
    
      - xyzfilename :: str
            xyz files from cppp.x. if given, read unitcellvectors from this file.
    
    Notes
    -----------------
    xyzfilenameにはcppp.xで作成した生のxyzファイルを使うこと！！
    '''
    def __init__(self, filename:str):
        #self.filename=filename
        super().__init__(atoms_list=raw_cpmd_read_wfc(filename), unitcell_vector=None, filename=filename)
        #self.UNITCELL_VECTOR=None
        #self.ATOMS_LIST=raw_read_wfc(filename, unitcell_vector=None)
        # self.TRAJ=ase.io.trajectory.Trajectory(filename+"_refine.traj")

    #def nglview_traj(self):
    #    return cpmd.read_traj.raw_nglview_traj(self.ATOMS_LIST)
            
    def merge_wfc_xyz(self, xyz_list):
        '''
        xyz_list :: atoms trajectory (list of ase.atoms)
        '''
        merged_atoms=cpmd.read_wfc.raw_merge_wfc_xyz(self.ATOMS_LIST, xyz_list)
        return cpmd.read_core.custom_traj(atoms_list=merged_atoms)

    # メソッドのoverride
    def save(self):
        # DEPRECATED :: cpmd.read_traj.raw_save_aseatoms(self.ATOMS_LIST,  xyz_filename=self.filename+"_refine.xyz")
        ase.io.write(self.filename+"_refine.xyz", self.ATOMS_LIST, format="extxyz") 
        return 0
    
