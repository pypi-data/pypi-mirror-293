'''
descripterを作成するためのコード
'''

from ase.io import read
import ase
import sys
import torch
import numpy as np
# from types import NoneType
from cpmd.asign_wcs import raw_get_distances_mic # get_distances(mic)の計算用
    
#Cutoff関数の定義
import numpy as np
def fs(Rij:float,Rcs:float,Rc:float) -> float:
    """カットオフ関数
    
    現在利用しているカットオフ関数は，deepmdグループのもの．Rijが単一の実数である場合のversion．
    Rij<Rcsの時:1/Rij
    Rcs<Rcの時:(1/Rij)*(0.5*np.cos(np.pi*(Rij-Rcs)/(Rc-Rcs))+0.5)
    Rc<Rijの時:0
    を返す関数

    Args:
        Rij (float): 原子間距離 [ang. unit]
        Rcs (float): inner cut off [ang. unit] 
        Rc (float) : outer cut off [ang. unit] 

    Returns:
        float_: カットオフ関数の値
    """

    if Rij < Rcs :
        s = 1/Rij 
    elif Rij < Rc :
        s = (1/Rij)*(0.5*np.cos(np.pi*(Rij-Rcs)/(Rc-Rcs))+0.5)
    else :
        s = 0 
    return s 

def cutoff_func(Rij:np.array,Rcs:float,Rc:float) -> np.array:
    """cutoff function by numpy where
    
    np.whereを利用することで，Rijとしてnumpy arrayを受け付けて一挙の処理を可能にする．

    Args:
        Rij (np.array): 原子間距離 [ang. unit]
        Rcs (float): inner cut off [ang. unit] 
        Rc (float):  outer cut off [ang. unit] 

    Returns:
        np.array: _description_
    """
    # np.whereを入れ子にすることで，fs関数と全く同じ挙動をnp.arrayに対して実現する．
    s= np.where(Rij<Rcs,1/Rij,np.where(Rij<Rc,(1/Rij)*(0.5*np.cos(np.pi*(Rij-Rcs)/(Rc-Rcs))+0.5),0))  
    # use torch.where
    # s= torch.where(Rij<Rcs,1/Rij,torch.where(Rij<Rc,(1/Rij)*(0.5*torch.cos(torch.pi*(Rij-Rcs)/(Rc-Rcs))+0.5),0))      
    return s

def cutoff_func_torch(Rij:torch.Tensor,Rcs:float,Rc:float) -> torch.Tensor:
    """cutoff function by torch.where

    Args:
        Rij (torch.Tensor): _description_
        Rcs (float): _description_
        Rc (float): _description_

    Returns:
        torch.Tensor: _description_
    """
    s= torch.where(Rij<Rcs,1/Rij,torch.where(Rij<Rc,(1/Rij)*(0.5*torch.cos(torch.pi*(Rij-Rcs)/(Rc-Rcs))+0.5),0))      
    return s
    

#Rotate vector
def rot_vec(vec,ths):
    thx,thy,thz = np.pi*ths
    Rx = np.array([ [1.0, 0.0, 0.0],[0.0,np.cos(thx),np.sin(thx)],[0.0,-np.sin(thx),np.cos(thx)] ])
    Ry = np.array([ [np.cos(thy),0.0,np.sin(thy)],[0.0, 1.0, 0.0],[-np.sin(thy),0.0,np.cos(thy)] ])
    Rz = np.array([ [np.cos(thz),np.sin(thz),0.0],[-np.sin(thz),np.cos(thz),0.0], [0.0, 0.0, 1.0] ])
    new_vec = np.dot(Rz,np.dot(Ry,np.dot(Rx,vec)))
    return new_vec


class descripter:
    import ase
    '''
    関数をメソッドとしてこちらにうつしていく．
    その際，基本となる変数をinitで定義する
    '''
    def __init__(self, NUM_MOL:int, NUM_MOL_ATOMS:int, UNITCELL_VECTORS):
        self.NUM_MOL       = NUM_MOL
        self.NUM_MOL_ATOMS = NUM_MOL_ATOMS
        self.UNITCELL_VECTORS = UNITCELL_VECTORS
    # !! bond center descriptor for old version
    def get_desc_bondcent(self,atoms,bond_center,mol_id):
        return raw_get_desc_bondcent(atoms, bond_center, mol_id, self.UNITCELL_VECTORS, self.NUM_MOL_ATOMS)
    # !! lone pair for old version
    def get_desc_lonepair(self,atoms,bond_center,mol_id):
        return raw_get_desc_lonepair(atoms, bond_center, mol_id, self.UNITCELL_VECTORS, self.NUM_MOL_ATOMS)
    # !! calculate bondcenter descriptor （Pytorch）
    def calc_bond_descripter_at_frame(self,atoms_fr:ase.Atoms,list_bond_centers,bond_index, desctype:str, Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
        return raw_calc_bond_descripter_at_frame(atoms_fr,list_bond_centers,bond_index, self.NUM_MOL,self.UNITCELL_VECTORS, self.NUM_MOL_ATOMS, desctype, Rcs, Rc, MaxAt)
    # !! calculate lonepair descriptor (Pytorch)
    def calc_lonepair_descripter_at_frame(self,atoms_fr,list_mol_coords, at_list, atomic_index:int, desctype,Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
        return raw_calc_lonepair_descripter_at_frame(atoms_fr,list_mol_coords, at_list, self.NUM_MOL, atomic_index, self.UNITCELL_VECTORS, self.NUM_MOL_ATOMS, desctype, Rcs,Rc,MaxAt)
    # >>> 以下双極子 >>>
    # !! calculate bond mu 
    def calc_bondmu_descripter_at_frame(self, list_mu_bonds, bond_index):
        return raw_calc_bondmu_descripter_at_frame(list_mu_bonds, bond_index)
    
    # !! 多分現状使ってない．．
    @DeprecationWarning
    def calc_lonepairmu_descripter_at_frame(self,list_mu_lp, list_atomic_nums, at_list, atomic_index:int):
        return raw_calc_lonepairmu_descripter_at_frame(list_mu_lp, list_atomic_nums, at_list, atomic_index)
    
    # !! COHボンドのbond双極子用
    def calc_coh_bondmu_descripter_at_frame(self,list_mu_bonds, list_mu_lp, coh_index,co_bond_index,oh_bond_index):
        return raw_calc_coh_bondmu_descripter_at_frame(list_mu_bonds, list_mu_lp, coh_index,co_bond_index,oh_bond_index)
        
    def calc_coc_bondmu_descripter_at_frame(self,list_mu_bonds, list_mu_lp, coc_index,co_bond_index):
        return raw_calc_coc_bondmu_descripter_at_frame(list_mu_bonds, list_mu_lp, coc_index,co_bond_index)

    # !! 
    def calc_lonepair_descripter_at_frame_type2(self,atoms_fr,list_mol_coords, at_list, desctype:str,Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
        '''
        1つのframe中の一種のローンペアの記述子を計算する

        atomic__index : 原子量（原子のリストを取得するのと，原子座標の取得に使う）
        at_list      : 1分子内での原子のある場所のリスト
        分子ID :: 分子1~分子NUM_MOLまで
        '''

        # list_mol_coors:[NUM_MOL,NUM_MOL_ATOM,3]から，at_listに対応する原子の座標を抽出する
        # !! listだとこの形式は許されず，numpy array出ないといけない．
        list_lonepair_coords = np.array(list_mol_coords)[:,np.array(at_list),:]
        
        if len(at_list) != 0: # 中身が0でなければ計算を実行
            if desctype == "old":
                raise ValueError("calc_lonepair_descripter_at_frame_type2 :: desctype = old is not supported for torch descriptors!!")
            elif desctype == "allinone":
                # Descs = [raw_get_desc_lonepair_allinone(atoms_fr,bond_center,UNITCELL_VECTORS,NUM_MOL_ATOMS,Rcs,Rc,MaxAt) for bond_center in list_lonepair_coords]
                # using Torch
                Descs = raw_get_desc_lonepair_allinone_torch(atoms_fr,list_lonepair_coords, self.UNITCELL_VECTORS, Rcs, Rc, MaxAt)
                return np.array(Descs)

    # !! Descriptor for COC, COH bond
    def calc_coc_descripter_at_frame(self,atoms_fr:ase.Atoms, list_mol_coords:np.array, coc_bond_index:list, desctype:str = "allinone",Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
        '''
        1つのframe中の一種のローンペアの記述子を計算する
        at_list      : 1分子内での原子のある場所のリス
        分子ID :: 分子1~分子NUM_MOLまで
        '''
        # print(f"coc_bond_index = {coc_bond_index}")
        o_list = [coc_bond_index[i][1] for i in range(len(coc_bond_index))] # index list for O atom (use 1 instead of 0)
        list_lonepair_coords = np.array(list_mol_coords)[:,o_list,:] # O原子の座標リスト
        # print(f"o_list  = {o_list}")
        # print(f"list_mol_coords = {np.shape(list_mol_coords)}")
        # print("list_lonepair_coords.shape :: ", np.shape(list_lonepair_coords))
        
        if len(coc_bond_index) != 0: # 中身が0でなければ計算を実行
            if desctype == "old":
                raise ValueError("calc_coc_descripter_at_frame :: desctype = old is not supported for COC/COH calculations !!")
            elif desctype == "allinone":
                # using Torch
                Descs = raw_get_desc_lonepair_allinone_torch(atoms_fr,list_lonepair_coords, self.UNITCELL_VECTORS, Rcs, Rc, MaxAt)
                # Descs = raw_calc_coc_bondmu_descripter_at_frame(list_mu_bonds, list_mu_lp, coc_bond_index,co_bond_index)
                return np.array(Descs)
            else:
                raise ValueError("calc_coc_descripter_at_frame :: desctype = old is not supported for COC/COH calculations !!")
                


    
def raw_make_atoms(bond_center,atoms:ase.Atoms,UNITCELL_VECTORS) :
    '''
    ######INPUTS#######
    bond_center     # vector 記述子を求めたい結合中心の座標
    list_mol_coords # array  分子ごとの原子座標
    list_atomic_nums #array  分子ごとの原子座標
    '''
    from ase import Atoms
    list_mol_coords=atoms.get_positions()
    list_atomic_nums=atoms.get_atomic_numbers()
    
    #選択した結合中点の座標を先頭においたAtomsオブジェクトを作成する
    pos = np.array(list([bond_center,])+list(list_mol_coords))
    #結合中心のラベルはAuとする
    elements = {"Au":79}
    atom_id= list(["Au",])+list(list_atomic_nums)
    
    WBC = ase.Atoms(atom_id,
             positions=pos,        
             cell= UNITCELL_VECTORS,   
             pbc=[1, 1, 1]) 
    return WBC

def calc_descripter(dist_wVec,atoms_index,Rcs:float,Rc:float,MaxAt:int):
    """ある原子種に対する記述子を作成する．
    
    ある原子種に対する記述子を作成する．相対座標のリストをdist_wVecで受け取り，そのうち計算するべきindexをatoms_indexで渡す．
    実装上最重要の関数であり，ここで記述子の計算を行うので速度に気をつけた実装をしないといけない．
    
    Args:
        dist_wVec (list[numpy.ndarray]): ある原子種からの距離ベクトルを保持する．
        atoms_index (_type_): 計算したい原子のインデックス
        Rcs (float): inner cutoff
        Rc  (float): outer cutoff
        MaxAt (int): 記述子として考慮する最大の原子の数（現状24を想定）

    Returns:
        _type_: _description_
    """

    # TODO :: 変数の整理をやって，最初からdist_wVec[atoms_index]を引数にすれば良いように思う．
    # atoms_indexのみの要素を取り出す. dist_wVecはあくまでベクトルである．
    # drs =np.array([v for l,v in enumerate(dist_wVec) if (l in atoms_index) and (l!=0)]) # 相対ベクトル(x,y,z)
    # 2024/1/11 numpyに変更した．l=0のときのデータも含めたままにして，後段の処理でまとめて排除する．
    drs = dist_wVec[atoms_index] 

    # >>>> ここからで不要な要素の削除 >>>>>>    
    # もしdの中に0のもの（これは同一原子間の距離に対応しちゃってる）があったらそれを排除したい．
    # そこでnp.sum(np.abs(drs[j])) = 0（要するに全ての要素が0）のものを排除する．
    # drs_tmp = [] # 変更するための配列
    # for j in range(len(drs)):
    #     if np.sum(np.abs(drs[j])) > 0.001: # 0.001は適当な閾値．現状これでうまくいっている
    #         drs_tmp.append(drs[j])
    # drs = np.array(drs_tmp) #新しいもので置き換え

    # !! 2024/1/11 山崎さん提案の新しい排除手法
    drs = drs[np.sum(drs**2,axis=1)>0.001]
    # >>>> ここまでで不要な要素の削除 >>>>>>
    
    # 以下で4 component vectorを計算する．
    if np.shape(drs)[0] == 0: # 要素が0の時．dijは空とする（これをやらないと要素0時にエラーになる）
        dij = []    
    else:
        d:np.array = np.sqrt(np.sum(drs**2,axis=1)) # 原子間距離rのnp.array
        # s = np.array([fs(Rij,Rcs,Rc) for Rij in d ]) # cutoff関数 
        cutoff:np.array = cutoff_func(d,Rcs,Rc) # !! 2024/1/11 cutoff関数をnumpy whereで書き直した．
        order_indx = np.argsort(cutoff)[-1::-1]  # sの大きい順に並べる
        sorted_drs    = drs[order_indx]
        sorted_cutoff = cutoff[order_indx]
        sorted_d   = d[order_indx]
        # TODO :: リスト内包形式をやめる．もう少しスマートな書き方があるはず．
        # dij  = [ [si,]+list(si*vi/di) for si,vi,di in zip(sorted_cutoff,sorted_drs,sorted_d)]
        # 以下山崎さん提案のコード．np.newaxisで新たな次元を追加している？
        tmp = sorted_cutoff[:,np.newaxis]*sorted_drs/sorted_d[:,np.newaxis] # 3成分cutoff*(x/r,y/r,z/r)を計算
        dij  = np.insert(tmp, 0, sorted_cutoff, axis=1)

    #原子数がMaxAtよりも少なかったら０埋めして固定長にする。1原子あたり4要素(1,x/r,y/r,z/r)
    if len(dij) < MaxAt : # 0埋め
        dij_desc = list(np.array(dij).reshape(-1)) + [0]*(MaxAt - len(dij))*4
    else : # 切り詰め
        dij_desc = list(np.array(dij).reshape(-1))[:MaxAt*4]
    return dij_desc


def raw_get_desc_bondcent(atoms:ase.Atoms,bond_center,mol_id, UNITCELL_VECTORS:np.array, NUM_MOL_ATOMS:int) :
    """calculate descriptor for bond center (old version)

    calculate descriptor for bond center (old version), which separate inter and intra-molecular contribution.
    Args:
        atoms (_type_): _description_
        bond_center (_type_): _description_
        mol_id (_type_): _description_
        UNITCELL_VECTORS (_type_): _description_
        NUM_MOL_ATOMS (int): _description_
    """
    
    from ase import Atoms
    '''
    ボンドセンター用の記述子を作成
    ######Inputs########
    atoms : ASE atom object 構造の入力
    Rcs : float inner cut off [ang. unit]
    Rc  : float outer cut off [ang. unit] 
    MaxAt : int 記述子に記載する原子数（これにより固定長の記述子となる）
    #bond_center : vector 記述子を計算したい結合の中心
    ######Outputs#######
    Desc : 原子番号,[List O原子のSij x MaxAt : H原子のSij x MaxAt] x 原子数 の二次元リストとなる.
    ####################
    '''
    ###INPUTS###
    # parsed_results : 関数parse_cpmd_resultを参照 
    ######parameter入力######
    Rcs = 4.0 #[ang. unit] TODO : hard code
    Rc  = 6.0 #[ang. unit] TODO : hard code
    MaxAt = 12 # とりあえずは12個の原子で良いはず．
    ##########################

    # ボンドセンターを追加したatoms
    atoms_w_bc = raw_make_atoms(bond_center,atoms, UNITCELL_VECTORS)
    
    atoms_in_molecule = [i for i in range(mol_id*NUM_MOL_ATOMS+1,(mol_id+1)*NUM_MOL_ATOMS+1)] #結合中心を先頭に入れたAtomsなので+1
    
    # 記述子のうち各原子の分を作成する．
    Catoms_all   =  [i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 6) ]
    Hatoms_all   =  [i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 1) ]
    Oatoms_all   =  [i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 8) ]
    Catoms_intra =  [i for i in Catoms_all if i in atoms_in_molecule]
    Catoms_inter =  [i for i in Catoms_all if i not in atoms_in_molecule ]
    Hatoms_intra =  [i for i in Hatoms_all if i in atoms_in_molecule]
    Hatoms_inter =  [i for i in Hatoms_all if i not in atoms_in_molecule ]   
    Oatoms_intra =  [i for i in Oatoms_all if i in atoms_in_molecule]
    Oatoms_inter =  [i for i in Oatoms_all if i not in atoms_in_molecule ]   

    at_list = [i for i in range(len(atoms_w_bc))] # 全ての原子との距離を求める
    # dist_wVec = atoms_w_bc.get_distances(0,at_list,mic=True,vector=True)  #0-0間距離も含まれる
    dist_wVec = raw_get_distances_mic(atoms_w_bc,0, at_list, mic=True,vector=True) # 0-0間距離も含まれる
    # at_nums = atoms_w_bc.get_atomic_numbers()

    #for C atoms (intra) 
    dij_C_intra=calc_descripter(dist_wVec, Catoms_intra, Rcs,Rc,MaxAt)
    #for H atoms (intra)
    dij_H_intra=calc_descripter(dist_wVec, Hatoms_intra, Rcs,Rc,MaxAt)
    #for O  atoms (intra)
    dij_O_intra=calc_descripter(dist_wVec, Oatoms_intra, Rcs,Rc,MaxAt)
    #for C atoms (inter)
    dij_C_inter=calc_descripter(dist_wVec, Catoms_inter, Rcs,Rc,MaxAt)
    #for H atoms (inter)
    dij_H_inter=calc_descripter(dist_wVec, Hatoms_inter,Rcs,Rc,MaxAt)
    #for O atoms (inter)
    dij_O_inter=calc_descripter(dist_wVec, Oatoms_inter,Rcs,Rc,MaxAt)

    return(dij_C_intra+dij_H_intra+dij_O_intra+dij_C_inter+dij_H_inter+dij_O_inter)


def raw_get_desc_bondcent_allinone(atoms:ase.Atoms,bond_center,UNITCELL_VECTORS, NUM_MOL_ATOMS:int, Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24) :
    """calculate descriptor for a given bonc_center (all in one version)

    Args:
        atoms (ase.Atoms): _description_
        bond_center (_type_): _description_
        UNITCELL_VECTORS (_type_): _description_
        NUM_MOL_ATOMS (int): _description_
        Rcs (float, optional): _description_. Defaults to 4.0.
        Rc (float, optional): _description_. Defaults to 6.0.
        MaxAt (int, optional): _description_. Defaults to 24.
    """
    '''
    ボンドセンター用の記述子を作成
    2023/6/27 :: 分子内と分子間を分けない．その代わりMaxAtを24まで増やす．
    2023/10/19 :: Rcs，Rc，MaxAtを変数化
    ######Inputs########
    atoms : ASE atom object 構造の入力
    Rcs : float inner cut off [ang. unit]
    Rc  : float outer cut off [ang. unit] 
    MaxAt : int 記述子に記載する原子数（これにより固定長の記述子となる）
    bond_center : vector 記述子を計算したい結合の中心座標
    ######Outputs#######
    Desc : 原子番号,[List O原子のSij x MaxAt : H原子のSij x MaxAt] x 原子数 の二次元リストとなる.
    ####################
    '''
    ###INPUTS###
    # parsed_results : 関数parse_cpmd_resultを参照 
    ######parameter入力######
    # Rcs = 4.0 #[ang. unit] 
    # Rc  = 6.0 #[ang. unit] 
    # MaxAt = 24 # intraとinterを分けない分，元の12*2=24としている．
    ##########################

    # ボンドセンターを追加したatomsを作成（bond centerが先頭）
    atoms_w_bc = raw_make_atoms(bond_center,atoms, UNITCELL_VECTORS)
    
    # 各原子の記述子を作成する．
    # 原子種のインデックスを取得
    # Catoms_all   =  [i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 6) ]
    # Hatoms_all   =  [i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 1) ]
    # Oatoms_all   =  [i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 8) ]
    # !! 2024/1/11 numpyを使うように変更
    Catoms_all = np.argwhere(atoms_w_bc.get_atomic_numbers()==6).reshape(-1)
    Hatoms_all = np.argwhere(atoms_w_bc.get_atomic_numbers()==1).reshape(-1)
    Oatoms_all = np.argwhere(atoms_w_bc.get_atomic_numbers()==8).reshape(-1)

    # atoms_w_bc(atoms+1)の長さのリストを作成
    # at_list = [i for i in range(len(atoms_w_bc))] # 全ての原子との距離を求める
    at_list = np.arange(len(atoms_w_bc)) # !! 024/1/11 numpyに変更した．デバックが必要．
    # dist_wVec = atoms_w_bc.get_distances(0,at_list,mic=True,vector=True)  #0-0間距離も含まれる
    dist_wVec = raw_get_distances_mic(atoms_w_bc,0, at_list, mic=True,vector=True) # 0-0間距離も含まれるので，先頭が0になる．
    # at_nums = atoms_w_bc.get_atomic_numbers()

    #for C atoms 
    dij_C_all=calc_descripter(dist_wVec, Catoms_all, Rcs,Rc,MaxAt) 
    #for H atoms
    dij_H_all=calc_descripter(dist_wVec, Hatoms_all, Rcs,Rc,MaxAt)
    #for O  atoms
    dij_O_all=calc_descripter(dist_wVec, Oatoms_all, Rcs,Rc,MaxAt)

    return(dij_C_all+dij_H_all+dij_O_all)


# !! GPU acceleration by pytorch(bond center)
# !! added at 2024/1/11
def get_desc_bondcent_allinone_torch(atoms:ase.Atoms,bond_centers, UNITCELL_VECTORS, Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24) :
    """calculate descriptor for given bond_centers (all in one version) using torch

    Args:
        atoms (ase.Atoms): _description_
        bond_centers (_type_): _description_
        UNITCELL_VECTORS (_type_): _description_
        Rcs (float, optional): _description_. Defaults to 4.0.
        Rc (float, optional): _description_. Defaults to 6.0.
        MaxAt (int, optional): _description_. Defaults to 24.

    Returns:
        _type_: _description_
    """
    
    #import time 
    #init_time = time.time()
    
    from ase import Atoms
    
    ######Inputs########
    # atoms : ASE atom object 構造の入力
    # Rcs : float inner cut off [ang. unit]
    # Rc  : float outer cut off [ang. unit] 
    # MaxAt : int 記述子に記載する原子数（これにより固定長の記述子となる）
    #bond_center : vector 記述子を計算したい結合の中心
    ######Outputs#######
    # Desc : 原子番号,[List O原子のSij x MaxAt : H原子のSij x MaxAt] x 原子数 の二次元リストとなる.
    ####################
    
    ###INPUTS###
    # parsed_results : 関数parse_cpmd_resultを参照 
    
    list_mol_coords  = np.array(atoms.get_positions(),dtype="float32")
    list_atomic_nums = np.array(atoms.get_atomic_numbers(), dtype="int32") # 先にint32に変換しておく必要あり
    
    import torch  
    # check device
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available(): 
        device = "mps"
    else:
        device = 'cpu'

    # convert numpy array to torch
    list_mol_coords  = torch.tensor(list_mol_coords).to(device)
    list_atomic_nums = torch.tensor(list_atomic_nums).to(device)
    bond_centers     = torch.tensor(np.array(bond_centers,dtype="float32")).to(device)

    # get atomic numbers from atoms
    # ! CAUTION:: index is different from raw_get_desc_bondcent_allinone
    Catoms_all = torch.argwhere(list_atomic_nums==6).reshape(-1)
    Hatoms_all = torch.argwhere(list_atomic_nums==1).reshape(-1)
    Oatoms_all = torch.argwhere(list_atomic_nums==8).reshape(-1)

    # 分子座標-ボンドセンター座標を行列の形で実行する
    # list_mol_coords:: [Frame,]
    # mat_ij = atom_i - atom_
    matA = list_mol_coords[None,:,:].repeat(len(bond_centers),1,1)
    matB = bond_centers[None,:,:].repeat(len(list_mol_coords),1,1)
    matB = torch.transpose(matB, 1,0)
    drs = (matA - matB)

    # 簡易的なmic計算
    # TODO !! pytorchでのmic計算コードを実装したのでそれに置き換える
    L=UNITCELL_VECTORS[0][0]/2.0
    tmp = torch.where(drs>L,drs-2.0*L,drs)
    dist_wVec = torch.where(tmp<-L,tmp+2.0*L,tmp)

    #for C atoms (all) 
    #C原子のローンペアはありえないので原子間距離ゼロの判定は省く
    drs = dist_wVec[:,Catoms_all,:]
    d = torch.sqrt(torch.sum(drs**2,axis=2)) # 距離の二乗から1乗を導出
    s = cutoff_func_torch(d,Rcs,Rc)
    # s= torch.where(d<Rcs,1/d,torch.where(d<Rc,(1/d)*(0.5*torch.cos(torch.pi*(d-Rcs)/(Rc-Rcs))+0.5),0))
    order_indx1 = torch.argsort(s,descending=True)  # sの大きい順に並べる
    c = torch.arange(len(order_indx1))
    order_indx0 = torch.transpose(c[None,:],1,0) 
    order_indx = (order_indx0,order_indx1)
    sorted_drs = drs[order_indx]
    sorted_s   = s[order_indx]
    sorted_d   = d[order_indx]
    tmp = sorted_s[:,:,None]*sorted_drs/sorted_d[:,:,None]
    dij  = torch.cat([sorted_s[:,:,None],tmp],dim=2)
    #原子数がMaxAtよりも少なかったら０埋めして固定長にする。1原子あたり4要素(1,x/r,y/r,z/r)
    #####原子数が足りなかったときのゼロ埋めは後で考える
    #if len(dij) < MaxAt :
    #    dij_C_all = list(np.array(dij).reshape(-1)) + [0]*(MaxAt - len(dij))*4
    #else :
    #    dij_C_all = list(np.array(dij).reshape(-1))[:MaxAt*4] 
    dd = dij.shape
    dij_C_all=dij.reshape((dd[0],-1))[:,:MaxAt*4] 

    # 要素数が4*MaxAtよりも小さい場合、4*MaxAtになるように0埋めする
    if dij_C_all.size(1) < 4*MaxAt:
        padding = torch.zeros(dij_C_all.size(0), 4*MaxAt - dij_C_all.size(1)).to(device)
        dij_C_all = torch.cat([dij_C_all, padding], dim=1)

    dij_C_all = dij_C_all.to("cpu").detach().numpy()
        
    #for H atoms (all)
    #H原子のローンペアはありえないので原子間距離ゼロの判定は省く
    drs = dist_wVec[:,Hatoms_all,:]
    d = torch.sqrt(torch.sum(drs**2,axis=2))
    s= torch.where(d<Rcs,1/d,torch.where(d<Rc,(1/d)*(0.5*torch.cos(torch.pi*(d-Rcs)/(Rc-Rcs))+0.5),0))
    order_indx1 = torch.argsort(s,descending=True)  # sの大きい順に並べる
    c = torch.arange(len(order_indx1))
    order_indx0 = torch.transpose(c[None,:],1,0) 
    order_indx = (order_indx0,order_indx1)
    sorted_drs = drs[order_indx]
    sorted_s   = s[order_indx]
    sorted_d   = d[order_indx]
    tmp = sorted_s[:,:,None]*sorted_drs/sorted_d[:,:,None]
    dij  = torch.cat([sorted_s[:,:,None],tmp],dim=2)
    dd = dij.shape
    dij_H_all=dij.reshape((dd[0],-1))[:,:MaxAt*4] 
    # 要素数が4*MaxAtよりも小さい場合、4*MaxAtになるように0埋めする
    if dij_H_all.size(1) < 4*MaxAt:
        padding = torch.zeros(dij_H_all.size(0), 4*MaxAt - dij_H_all.size(1)).to(device)
        dij_H_all = torch.cat([dij_H_all, padding], dim=1)
    dij_H_all = dij_H_all.to("cpu").detach().numpy()
        
    #for O atoms (all)
    drs = dist_wVec[:,Oatoms_all,:]
    d = torch.sqrt(torch.sum(drs**2,axis=2))
    s= torch.where(d<Rcs,1/d,torch.where(d<Rc,(1/d)*(0.5*torch.cos(torch.pi*(d-Rcs)/(Rc-Rcs))+0.5),0))
    order_indx1 = torch.argsort(s,descending=True)  # sの大きい順に並べる
    c = torch.arange(len(order_indx1))
    order_indx0 = torch.transpose(c[None,:],1,0) 
    order_indx = (order_indx0,order_indx1)
    sorted_drs = drs[order_indx]
    sorted_s   = s[order_indx]
    sorted_d   = d[order_indx]
    tmp = sorted_s[:,:,None]*sorted_drs/sorted_d[:,:,None]
    dij  = torch.cat([sorted_s[:,:,None],tmp],dim=2)
    dd = dij.shape
    dij_O_all=dij.reshape((dd[0],-1))[:,:MaxAt*4] 
    # 要素数が4*MaxAtよりも小さい場合、4*MaxAtになるように0埋めする
    if dij_O_all.size(1) < 4*MaxAt:
        padding = torch.zeros(dij_O_all.size(0), 4*MaxAt - dij_O_all.size(1)).to(device)
        dij_O_all = torch.cat([dij_O_all, padding], dim=1)
    dij_O_all = dij_O_all.to("cpu").detach().numpy() 
        
    return np.concatenate([dij_C_all, dij_H_all,dij_O_all], 1)


def raw_get_desc_lonepair(atoms,lonepair_coord,mol_id, UNITCELL_VECTORS, NUM_MOL_ATOMS:int):
    """calculate descriptor for lone pair (old version)

    Args:
        atoms (_type_): _description_
        lonepair_coord (_type_): _description_
        mol_id (_type_): _description_
        UNITCELL_VECTORS (_type_): _description_
        NUM_MOL_ATOMS (int): _description_
    """
    
    from ase import Atoms
    '''
    古いタイプ（分子内外を分けるタイプ）の記述子を利用した計算
    ######Inputs########
    # atoms : ASE atom object 構造の入力
    # Rcs : float inner cut off [ang. unit]
    # Rc  : float outer cut off [ang. unit] 
    # MaxAt : int 記述子に記載する原子数（これにより固定長の記述子となる）
    #bond_center : vector 記述子を計算したい結合の中心
     mol_id : bond_centerが含まれる分子のid．
    ######Outputs#######
    # Desc : 原子番号,[List O原子のSij x MaxAt : H原子のSij x MaxAt] x 原子数 の二次元リストとなる.
    ####################
    
    ###INPUTS###
    # parsed_results : 関数parse_cpmd_resultを参照 
    '''
    ######parameter入力######
    Rcs = 4.0 #[ang. unit] TODO :: hard code 
    Rc  = 6.0 #[ang. unit] TODO :: hard code 
    MaxAt = 12 # とりあえずは12個の原子で良いはず．
    ##########################

    
    # ボンドセンターを追加したatoms
    atoms_w_bc = raw_make_atoms(lonepair_coord,atoms, UNITCELL_VECTORS)

    atoms_in_molecule = [i for i in range(mol_id*NUM_MOL_ATOMS+1,(mol_id+1)*NUM_MOL_ATOMS+1)] #結合中心を先頭に入れたAtomsなので+1

    # 各原子のインデックスを取得
    Catoms_all = [ i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 6) ]
    Hatoms_all = [ i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 1) ]
    Oatoms_all = [ i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 8) ]
    Catoms_intra =  [i for i in Catoms_all if i in atoms_in_molecule]
    Catoms_inter =  [i for i in Catoms_all if i not in atoms_in_molecule ]
    Hatoms_intra =  [i for i in Hatoms_all if i in atoms_in_molecule]
    Hatoms_inter =  [i for i in Hatoms_all if i not in atoms_in_molecule ]   
    Oatoms_intra =  [i for i in Oatoms_all if i in atoms_in_molecule]
    Oatoms_inter =  [i for i in Oatoms_all if i not in atoms_in_molecule ]   

    at_list = [i for i in range(len(atoms_w_bc))]
    # dist_wVec = atoms_w_bc.get_distances(0,at_list,mic=True,vector=True)  #0-0間距離も含まれる
    dist_wVec = raw_get_distances_mic(atoms_w_bc,0,at_list,mic=True,vector=True)  #0-0間距離も含まれる
    # at_nums = atoms_w_bc.get_atomic_numbers()

    # dist_wVec：ボンドセンターから他の原子までの距離
    #for C atoms (intra) 
    dij_C_intra=calc_descripter(dist_wVec, Catoms_intra,Rcs,Rc,MaxAt)    
    #for H atoms (intra)
    dij_H_intra=calc_descripter(dist_wVec, Hatoms_intra,Rcs,Rc,MaxAt)  
    #for O  atoms (intra)
    dij_O_intra=calc_descripter(dist_wVec, Oatoms_intra,Rcs,Rc,MaxAt)  
    #for C atoms (inter)
    dij_C_inter=calc_descripter(dist_wVec, Catoms_inter,Rcs,Rc,MaxAt) 
    #for H atoms (inter)
    dij_H_inter=calc_descripter(dist_wVec, Hatoms_inter,Rcs,Rc,MaxAt) 
    #for O atoms (inter)
    dij_O_inter=calc_descripter(dist_wVec, Oatoms_inter,Rcs,Rc,MaxAt)     

    return(dij_C_intra+dij_H_intra+dij_O_intra+dij_C_inter+dij_H_inter+dij_O_inter)


def raw_get_desc_lonepair_allinone(atoms,lonepair_coord, UNITCELL_VECTORS, NUM_MOL_ATOMS:int,Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
    
    from ase import Atoms
    '''
    ######Inputs########
    # atoms : ASE atom object 構造の入力
    # Rcs : float inner cut off [ang. unit]
    # Rc  : float outer cut off [ang. unit] 
    # MaxAt : int 記述子に記載する原子数（これにより固定長の記述子となる）
    #bond_center : vector 記述子を計算したい結合の中心
     mol_id : bond_centerが含まれる分子のid．
    ######Outputs#######
    # Desc : 原子番号,[List O原子のSij x MaxAt : H原子のSij x MaxAt] x 原子数 の二次元リストとなる.
    ####################
    
    ###INPUTS###
    # parsed_results : 関数parse_cpmd_resultを参照 
    Rcs = 4.0 #[ang. unit] 
    Rc  = 6.0 #[ang. unit] 
    MaxAt = 24 # とりあえずは12個の原子で良いはず．
    
    '''
    
    # ボンドセンターを追加したatoms
    atoms_w_bc = raw_make_atoms(lonepair_coord,atoms, UNITCELL_VECTORS)

    # atoms_in_molecule = [i for i in range(mol_id*NUM_MOL_ATOMS+1,(mol_id+1)*NUM_MOL_ATOMS+1)] #結合中心を先頭に入れたAtomsなので+1

    # 各原子のインデックスを取得
    # Catoms_all = [ i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 6) ]
    # Hatoms_all = [ i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 1) ]
    # Oatoms_all = [ i for i,j in enumerate(atoms_w_bc.get_atomic_numbers()) if (j == 8) ]
    # !! 2024/1/11 numpyを使うように変更
    Catoms_all = np.argwhere(atoms_w_bc.get_atomic_numbers()==6).reshape(-1)
    Hatoms_all = np.argwhere(atoms_w_bc.get_atomic_numbers()==1).reshape(-1)
    Oatoms_all = np.argwhere(atoms_w_bc.get_atomic_numbers()==8).reshape(-1)
 
    # at_list = [i for i in range(len(atoms_w_bc))]
    at_list = np.arange(len(atoms_w_bc)) # !! 024/1/11 numpyに変更した．デバックが必要．
    # TODO :: ローンペアの場合，lpの座標が2回入っているので，0が2回入っている．ここをもう少しきれいにしたい．
    # dist_wVec = atoms_w_bc.get_distances(0,at_list,mic=True,vector=True)  #0-0間距離も含まれる
    dist_wVec = raw_get_distances_mic(atoms_w_bc,0,at_list,mic=True,vector=True)  #0-0間距離も含まれる
    # at_nums = atoms_w_bc.get_atomic_numbers()

    # dist_wVec：ボンドセンターから他の原子までの距離
    #for C atoms
    dij_C_all=calc_descripter(dist_wVec, Catoms_all,Rcs,Rc,MaxAt)    
    #for H atoms 
    dij_H_all=calc_descripter(dist_wVec, Hatoms_all,Rcs,Rc,MaxAt)  
    #for O  atoms
    dij_O_all=calc_descripter(dist_wVec, Oatoms_all,Rcs,Rc,MaxAt)  
    return(dij_C_all+dij_H_all+dij_O_all)


def raw_get_desc_lonepair_allinone_torch(atoms:ase.Atoms,lonepair_coords:np.array, UNITCELL_VECTORS:np.array, Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
    
    #import time 
    #init_time = time.time()
    
    from ase import Atoms
    
    ######Inputs########
    # atoms : ASE atom object 構造の入力
    # Rcs : float inner cut off [ang. unit]
    # Rc  : float outer cut off [ang. unit] 
    # MaxAt : int 記述子に記載する原子数（これにより固定長の記述子となる）
    #bond_center : vector 記述子を計算したい結合の中心
    ######Outputs#######
    # Desc : 原子番号,[List O原子のSij x MaxAt : H原子のSij x MaxAt] x 原子数 の二次元リストとなる.
    ####################
    
    ###INPUTS###
    # parsed_results : 関数parse_cpmd_resultを参照 
    
    list_mol_coords  = np.array(atoms.get_positions(),dtype="float32")
    list_atomic_nums = np.array(atoms.get_atomic_numbers(), dtype="int32") # 先にint32に変換しておく必要あり

    
    import torch  
    # check device
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available(): 
        device = "mps"
    else:
        device = 'cpu'

    list_mol_coords  = torch.tensor(list_mol_coords).to(device)
    list_atomic_nums = torch.tensor(list_atomic_nums).to(device)
    lonepair_coords  = lonepair_coords.reshape(-1,3) # reshape [num_mol,o_index,coord] to 2D array ( これが必要？)
    lonepair_coords     = torch.tensor(np.array(lonepair_coords,dtype="float32")).to(device)
    # print("lonepair_coords", np.shape(lonepair_coords))
    # print("list_mol_coords", np.shape(list_mol_coords))


    # get atomic numbers from atoms
    # ! CAUTION:: index is different from raw_get_desc_bondcent_allinone(
    Catoms_all = torch.argwhere(list_atomic_nums==6).reshape(-1)
    Hatoms_all = torch.argwhere(list_atomic_nums==1).reshape(-1)
    Oatoms_all = torch.argwhere(list_atomic_nums==8).reshape(-1)

    # 分子座標-ボンドセンター座標を行列の形で実行する
    matA = list_mol_coords[None,:,:].repeat(len(lonepair_coords),1,1) # 原子座標
    matB = lonepair_coords[None,:,:].repeat(len(list_mol_coords),1,1) # lonepair座標
    matB = torch.transpose(matB, 1,0)
    drs = (matA - matB)

    # TODO :: pytorch版MIC計算を実装したのでそれに置き換える
    L=UNITCELL_VECTORS[0][0]/2.0
    tmp = torch.where(drs>L,drs-2.0*L,drs)
    dist_wVec = torch.where(tmp<-L,tmp+2.0*L,tmp)

    #for C atoms (all) 
    #C原子のローンペアはありえないので原子間距離ゼロの判定は省く
    drs = dist_wVec[:,Catoms_all,:]
    d = torch.sqrt(torch.sum(drs**2,axis=2))
    s= torch.where(d<Rcs,1/d,torch.where(d<Rc,(1/d)*(0.5*torch.cos(torch.pi*(d-Rcs)/(Rc-Rcs))+0.5),0))
    order_indx1 = torch.argsort(s,descending=True)  # sの大きい順に並べる
    c = torch.arange(len(order_indx1))
    order_indx0 = torch.transpose(c[None,:],1,0) 
    order_indx = (order_indx0,order_indx1)
    sorted_drs = drs[order_indx]
    sorted_s   = s[order_indx]
    sorted_d   = d[order_indx]
    tmp = sorted_s[:,:,None]*sorted_drs/sorted_d[:,:,None]
    dij  = torch.cat([sorted_s[:,:,None],tmp],dim=2)
    #原子数がMaxAtよりも少なかったら０埋めして固定長にする。1原子あたり4要素(1,x/r,y/r,z/r)
    #####原子数が足りなかったときのゼロ埋めは後で考える
    #if len(dij) < MaxAt :
    #    dij_C_all = list(np.array(dij).reshape(-1)) + [0]*(MaxAt - len(dij))*4
    #else :
    #    dij_C_all = list(np.array(dij).reshape(-1))[:MaxAt*4] 
    dd = dij.shape
    dij_C_all=dij.reshape((dd[0],-1))[:,:MaxAt*4] 
    # 要素数が4*MaxAtよりも小さい場合、4*MaxAtになるように0埋めする
    if dij_C_all.size(1) < 4*MaxAt:
        padding = torch.zeros(dij_C_all.size(0), 4*MaxAt - dij_C_all.size(1)).to(device)
        dij_C_all = torch.cat([dij_C_all, padding], dim=1)

    dij_C_all = dij_C_all.to("cpu").detach().numpy()
        
    #for H atoms (all)
    #H原子のローンペアはありえないので原子間距離ゼロの判定は省く
    drs = dist_wVec[:,Hatoms_all,:]
    d = torch.sqrt(torch.sum(drs**2,axis=2))
    s= torch.where(d<Rcs,1/d,torch.where(d<Rc,(1/d)*(0.5*torch.cos(torch.pi*(d-Rcs)/(Rc-Rcs))+0.5),0))
    order_indx1 = torch.argsort(s,descending=True)  # sの大きい順に並べる
    c = torch.arange(len(order_indx1))
    order_indx0 = torch.transpose(c[None,:],1,0) 
    order_indx = (order_indx0,order_indx1)
    sorted_drs = drs[order_indx]
    sorted_s   = s[order_indx]
    sorted_d   = d[order_indx]
    tmp = sorted_s[:,:,None]*sorted_drs/sorted_d[:,:,None]
    dij  = torch.cat([sorted_s[:,:,None],tmp],dim=2)
    dd = dij.shape
    dij_H_all=dij.reshape((dd[0],-1))[:,:MaxAt*4] 
    # 要素数が4*MaxAtよりも小さい場合、4*MaxAtになるように0埋めする
    if dij_H_all.size(1) < 4*MaxAt:
        padding = torch.zeros(dij_H_all.size(0), 4*MaxAt - dij_H_all.size(1)).to(device)
        dij_H_all = torch.cat([dij_H_all, padding], dim=1)

    dij_H_all = dij_H_all.to("cpu").detach().numpy()
        
    #for O atoms (all)
    #先頭のO原子と重複している原子を除去する
    tmp = dist_wVec[:,Oatoms_all,:]
    dd  = tmp.shape
    drs = tmp[torch.sum(tmp**2,axis=2)>0.0001].reshape((dd[0],-1,3)) #各行に１つづつ重複した原子が存在するはず
    d = torch.sqrt(torch.sum(drs**2,axis=2))
    s= torch.where(d<Rcs,1/d,torch.where(d<Rc,(1/d)*(0.5*torch.cos(torch.pi*(d-Rcs)/(Rc-Rcs))+0.5),0))
    order_indx1 = torch.argsort(s,descending=True)  # sの大きい順に並べる
    c = torch.arange(len(order_indx1))
    order_indx0 = torch.transpose(c[None,:],1,0) 
    order_indx = (order_indx0,order_indx1)
    sorted_drs = drs[order_indx]
    sorted_s   = s[order_indx]
    sorted_d   = d[order_indx]
    tmp = sorted_s[:,:,None]*sorted_drs/sorted_d[:,:,None]
    dij  = torch.cat([sorted_s[:,:,None],tmp],dim=2)
    dd = dij.shape
    dij_O_all=dij.reshape((dd[0],-1))[:,:MaxAt*4] 
    # 要素数が4*MaxAtよりも小さい場合、4*MaxAtになるように0埋めする
    if dij_O_all.size(1) < 4*MaxAt:
        padding = torch.zeros(dij_O_all.size(0), 4*MaxAt - dij_O_all.size(1)).to(device)
        dij_O_all = torch.cat([dij_O_all, padding], dim=1)

    dij_O_all = dij_O_all.to("cpu").detach().numpy() 
        
    return np.concatenate([dij_C_all, dij_H_all,dij_O_all], 1)
#
# TODO :: ここは将来的にはボンドをあらかじめ分割するようにして無くしてしまいたい．

def find_specific_bondcenter(list_bond_centers:np.array, bond_index:list)->np.array:
    """ list_bond_centersからbond_index情報をもとに特定のボンド（CHなど）だけ取り出す．

    Args:
        list_bond_centers (_type_): bond_centerの配列 [mol_id,bond,coord(3)]
        bond_index (_list_): bond_index in one molecule (see document)

    Returns:
        _type_: extracted bond_center in [frame*num_bond,3]
    """
    
    # extract specific bond_centers
    cent_mol = np.array(list_bond_centers)[:,bond_index,:]
    # reshape to [num_mol*num_bond,3]
    cent_mol = np.array(cent_mol).reshape((-1,3))
    return cent_mol


def find_specific_bondmu(list_mu_bonds:np.ndarray, bond_index:list)->np.ndarray:
    """list_mu_bondsからbond_indexに対応する特定のボンドだけ取り出す

    Args:
        list_mu_bonds (_type_): _description_
        bond_index (_list_): _description_

    Returns:
        np.ndarray: _description_
    """
    '''
    list_bond_centersからbond_index情報をもとに特定のボンド（CHなど）だけ取り出す．
    '''
    # mu_mol  = []
    # # ボンドセンターの座標と双極子をappendする．
    # for mol_mu_bond in list_mu_bonds: #UnitCellの分子ごとに分割 
    #     # chボンド部分（chボンドの重心と双極子をappend）
    #     mu_mol.append(mol_mu_bond[bond_index])
    
    # mol_mu_bondからbond_indexに対応するものだけを抽出
    mu_mol = np.array(list_mu_bonds)[:,bond_index,:]
    return np.array(mu_mol)

def find_specific_ringcenter(list_bond_centers, ring_index):
    ring_cent_mol = []
    # ボンドセンターの座標と双極子をappendする．
    for mol_bc in list_bond_centers: #UnitCellの分子ごとに分割 
        # ring部分（リングの重心とリングの双極子を計算）
        ring_center = np.mean(mol_bc[ring_index],axis=0)
        ring_cent_mol.append([ring_center])
    # reshape
    ring_cent_mol = np.array(ring_cent_mol).reshape((-1,3))
    return ring_cent_mol

def find_specific_ringmu(list_mu_bonds,list_mu_pai,ring_index):
    ring_mu_mol = []
    # ボンドセンターの座標と双極子をappendする．
    for mol_mu_bond,mol_mu_pai in zip(list_mu_bonds,list_mu_pai) : #UnitCellの分子ごとに分割 
        ## ring_center = mol_bc[ring_bond_index][0] # 2023/3/31: 試しにここを変更してみる！（あまり意味なかった．．．）
        ring_mu     = np.sum(mol_mu_bond[ring_index],axis=0) + np.sum(mol_mu_pai,axis=0)
        ring_mu_mol.append([ring_mu])
    return ring_mu_mol

def find_specific_lonepair(list_mol_coords, aseatoms, atomic_index:int, NUM_MOL:int)->np.array:
    '''
    与えられたaseatomとlist_mol_coordsの中から，atomic_indexに対応する原子の座標を抽出する
    '''
    
    # ローンペアのために，原子番号がatomic_indexの原子があるところのリストを取得
    at_list = raw_find_atomic_index(aseatoms, atomic_index, NUM_MOL)

    cent_mol=[]
    # 原子にまつわる（ローンペア系）座標と双極子をappendする．
    for atOs,mol_coords in zip(at_list,list_mol_coords):
        # oローンペア部分
        cent_mol.append(mol_coords[atOs]) #ここはatomic_indexに対応した原子（酸素なら8）の座標をappendする
    # reshape
    cent_mol = np.array(cent_mol).reshape((-1,3)) #最後フラットな形に変更
    return cent_mol


def find_specific_lonepairmu(list_mu_lp, list_atomic_nums, atomic_index:int):
    '''
    list_mu_lp: lonepairのdipoleリスト[mol_index,atomic_index, dipole(3)]
    list_atomic_nums: 
    
    output
    ----------
    mu_mol :: 
    '''
    
    # ローンペアのために，原子があるところのリストを取得
    at_list = []
    for js in list_atomic_nums:
        at = np.argwhere(js==atomic_index).reshape(-1).tolist() #リストにしておく
        at_list.append(at)

    mu_mol = []
    # print(at_list)
    # 原子にまつわる（ローンペア系）座標と双極子をappendする．(Nがある場合に対応してなくない？)
    # TODO :: 多分これバグだと思う．Nが入ってくると対応してなくない？
    for mol_mu_lone in list_mu_lp:
        # oローンペア部分
        mu_mol.append(mol_mu_lone)
    return mu_mol


def raw_calc_bond_descripter_at_frame(atoms_fr, list_bond_centers:np.array, bond_index:list, NUM_MOL:int, UNITCELL_VECTORS, NUM_MOL_ATOMS:int, desctype="allinone", Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
    """
    1つのframe中の一種のボンドの記述子を計算する．
    2024/1/11 :: cent_molについてのfor文を回しているところが非常に遅いので，これをまとめてnumpy/pytorchで実行するようにすると高速になるというのが山崎さんの提案で，それを実装する．
    Args:
        atoms_fr (_type_): _description_
        list_bond_centers (_type_): [mol_id,bond,coord(3)]
        bond_index (_type_): _description_
        NUM_MOL (int): The number of molecules in the system
        UNITCELL_VECTORS (_type_): _description_
        NUM_MOL_ATOMS (int): _description_
        desctype (str, optional): _description_. Defaults to "allinone".
        Rcs (float, optional): _description_. Defaults to 4.0.
        Rc (float, optional): _description_. Defaults to 6.0.
        MaxAt (int, optional): _description_. Defaults to 24.

    Returns:
        _type_: _description_
    """
    
    Descs = []
    cent_mol   = find_specific_bondcenter(list_bond_centers, bond_index) #特定ボンドの座標だけ取得
    if len(bond_index) != 0: # 中身が0でなければ計算を実行
        if desctype == "old":        
            i=0 # bond_centerのカウンター
            for bond_center in cent_mol:
                mol_id = i % NUM_MOL // len(bond_index) # 対応する分子ID（mol_id）を出すように書き直す．ボンドが1分子内に複数ある場合，その数で割らないといけない．（メタノールならCH結合が3つあるので3でわる）
                Descs.append(raw_get_desc_bondcent(atoms_fr,bond_center,mol_id,UNITCELL_VECTORS,NUM_MOL_ATOMS))
                i += 1
        elif desctype == "allinone":
            # 2023/6/27 ここをallinoneへ変更
            # Descs = [raw_get_desc_bondcent_allinone(atoms_fr,bond_center,UNITCELL_VECTORS,NUM_MOL_ATOMS, Rcs, Rc, MaxAt) for bond_center in cent_mol]
            Descs = get_desc_bondcent_allinone_torch(atoms_fr, cent_mol, UNITCELL_VECTORS, Rcs, Rc, MaxAt)
    return np.array(Descs)



def raw_calc_bondmu_descripter_at_frame(list_mu_bonds, bond_index:list)->np.array:
    '''
    各種ボンドの双極子の真値を計算するコード
    （元のコードでいうところのdata_y_chとか）
    まず，list_mu_bondsからbond_indexに対応するデータだけをmu_molに取り出す．
    '''
    mu_mol = find_specific_bondmu(list_mu_bonds, bond_index)
    mu_mol = mu_mol.reshape((-1,3)) # !! descriptorと形を合わせる
    return mu_mol


# !! COHボンド対応のTrue_y計算用
def raw_calc_coh_bondmu_descripter_at_frame(list_mu_bonds:np.array, list_mu_lp:np.array, coh_index:list,co_bond_index:list[int],oh_bond_index:list[int])->np.array:
    """COC/COHボンド用にTrue_yを計算する

    まず，list_mu_bondsからbond_indexに対応するデータだけをmu_molに取り出す．
    TODO :: 現状COHのみ対応している．もう少し汎用的な形にしたい．
    

    Args:
        list_mu_bonds (_type_): List of bond dipole [mol,num_bond,dipole(3)]
        list_mu_lp (_type_): [mol,atom,dipole(3)]
        coh_index (_type_): _description_
        co_bond_index (_type_): _description_
        oh_bond_index (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    data_y = [] # resultant COH bond dipole
    # print("coh_index =", coh_index)
    # COC/COHのindexからbond_indexおよびatomic_indexを取得
    if len(coh_index) != 0: # 中身が0でなければ計算を実行
        # print("coh_index =", coh_index)
        o_list  = [ index[0] for index in coh_index]
        co_list = [co_bond_index[index[2]["CO"]] for index in coh_index]
        oh_list = [oh_bond_index[index[2]["OH"]] for index in coh_index] 
        # print(f"{o_list} : {co_list} : {oh_list}")
        o_mu_mol = list_mu_lp[:,o_list,:] # [mol,num_o,3]
        co_mu_mol = find_specific_bondmu(list_mu_bonds, co_list)
        oh_mu_mol = find_specific_bondmu(list_mu_bonds, oh_list)
        coh_bonddipole = (o_mu_mol + co_mu_mol + oh_mu_mol).reshape(-1,3)
        # print(f" coh_bonddipole {np.shape(coh_bonddipole)}")
        # print(f"list_mu_bonds = {np.shape(list_mu_bonds)}")
        
        # for index in coh_index: #indexは[o_num, o_index, {"CO":index_co, "OH":index_oh}]の形            
        #     # Oの双極子を計算(list_mu_lp)
        #     # print(f"index = {index} :: index[0] = {index[0]} :: list_mu_lp = {np.shape(list_mu_lp)}")
        #     o_mu_mol = list_mu_lp[:,index[0],:] # [mol,3]
        #     # 二つのボンドの双極子を計算
        #     # まず，bond_indexへ変換する必要がある！！
        #     # find two adjacent bond dipole (CO&OH)
        #     bond1_mu_mol = find_specific_bondmu(list_mu_bonds, co_bond_index[index[2]["CO"]])
        #     bond2_mu_mol = find_specific_bondmu(list_mu_bonds, oh_bond_index[index[2]["OH"]])
        #     # mu_mol = mu_mol.reshape((-1,3)) # !! descriptorと形を合わせる
        #     coh_bonddipole = o_mu_mol+bond1_mu_mol+bond2_mu_mol
        #     data_y.append(coh_bonddipole)
        # print(f"MAX DIFF = {np.max(np.abs(coh_bonddipole-data_y))}")
        # print(f"data_y :: {np.shape(data_y)}") # この方法だと，data_yが(2,NUM_MOL,3)型になってしまい，descriptorと逆になる．
        # # return np.array(data_y).reshape((-1,3))
    return coh_bonddipole


def raw_calc_coc_bondmu_descripter_at_frame(list_mu_bonds:np.array, list_mu_lp:np.array, coc_index:list,co_bond_index:list[int]):
    """COCボンドの双極子を計算する

    Args:
        list_mu_bonds (_type_): _description_
        list_mu_lp (_type_): _description_
        coh_index (_type_): _description_
        co_bond_index (_type_): _description_

    Returns:
        _type_: _description_
    """ 
    data_y = []
    # COC/COHのindexからbond_indexおよびatomic_indexを取得
    if len(coc_index) != 0: # 中身が0でなければ計算を実行
        # print("coh_index =", coh_index)
        o_list = [ index[0] for index in coc_index]
        co1_list = [co_bond_index[index[2]["CO1"]] for index in coc_index]
        co2_list = [co_bond_index[index[2]["CO2"]] for index in coc_index]
        # print(f"{o_list} : {co_list} : {oh_list}")
        o_mu_mol = list_mu_lp[:,o_list,:] # [mol,num_o,3]
        co1_mu_mol = find_specific_bondmu(list_mu_bonds, co1_list)
        co2_mu_mol = find_specific_bondmu(list_mu_bonds, co2_list)
        coc_bonddipole = (o_mu_mol + co1_mu_mol + co2_mu_mol).reshape(-1,3)
    # if len(coc_index) != 0: # 中身が0でなければ計算を実行
    #     for index in coc_index: #indexは[o_num, o_index, {"CO1":index_co1, "CO2":index_co2}]の形
    #         # Oの双極子を計算(list_mu_lp)
    #         o_mu_mol = list_mu_lp[:,index[0],:]
    #         # 二つのボンドの双極子を計算
    #         # まず，bond_indexへ変換する必要がある！！
    #         # print(co_bond_index[index[1]["CO"]])
    #         # print(oh_bond_index[index[1]["OH"]])
            
    #         bond1_mu_mol = find_specific_bondmu(list_mu_bonds, co_bond_index[index[2]["CO1"]])
    #         bond2_mu_mol = find_specific_bondmu(list_mu_bonds, co_bond_index[index[2]["CO2"]])
    #         # mu_mol = mu_mol.reshape((-1,3)) # !! descriptorと形を合わせる
    #         coh_bonddipole = o_mu_mol+bond1_mu_mol+bond2_mu_mol
    #         data_y.append(coh_bonddipole)
    # # print("data_y :: ", data_y)
    # return np.array(data_y).reshape((-1,3))
    return coc_bonddipole


def raw_find_atomic_index(aseatoms, atomic_index:int, NUM_MOL:int):
    '''
    ase.atomsの中で特定の原子番号の部分のリストを作成する
    '''
    list_atomic_nums = list(np.array(aseatoms.get_atomic_numbers()).reshape(NUM_MOL,-1)) # atomic_numbersを分子ごとにreshape
    at_list = [ np.argwhere(js==atomic_index).reshape(-1).tolist() for js in list_atomic_nums] # atomic_indexに対応するindexを返す
    return at_list


def raw_calc_lonepair_descripter_at_frame(atoms_fr, list_mol_coords, at_list, NUM_MOL:int, atomic_index:int, UNITCELL_VECTORS, NUM_MOL_ATOMS:int, desctype = "allinone",Rcs:float=4.0, Rc:float=6.0, MaxAt:int=24):
    '''
    1つのframe中の一種のローンペアの記述子を計算する

    atomic__index : 原子量（原子のリストを取得するのと，原子座標の取得に使う）
    at_list      : 1分子内での原子のある場所のリスト
    TODO :: at_listは単に1分子内のO原子の数を数えるのに使っているだけなので，もっとよい方法を考える．
    TODO :: そもそもここではatomic_indexを入力としているが，よく考えると現在はitp_data.o_listがあるのだから，それを使ってcent_molの抽出ができるのでは？

    分子ID :: 分子1~分子NUM_MOLまで
    '''

    # ローンペアのために，原子があるところのリストを取得
    # !! こうやってatomic_indexからat_listを取得できるようになった．
    # !! したがって，入力のat_listはもういらん．
    # at_list2 = raw_find_atomic_index(atoms_fr, atomic_index, NUM_MOL)
    # print(" at_list & at_list2  :: {}, {}".format(at_list,at_list2))  # !! debug

    list_lonepair_coords = find_specific_lonepair(list_mol_coords, atoms_fr, atomic_index, NUM_MOL) #atomic_indexに対応した原子の座標を抜き取る
    # >>> 古いコード．新しくat_listを入力に与えるようにしたので不要に >>>>>
    # get_atomic_numbersから与えられた原子種の数を取得
    # at_list = raw_find_atomic_index(atoms_fr,atomic_index, NUM_MOL)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # print("DEBUG :: cent_mol :: ", cent_mol)
    
    if len(at_list) != 0: # 中身が0でなければ計算を実行
        if desctype == "old":
            Descs = []
            i=0
            for bond_center in list_lonepair_coords:
                mol_id = i % NUM_MOL // len(at_list) # 対応する分子ID（mol_id）を出すように書き直す．（1分子内のO原子の数（len(at_list）でわって分子idを出す）
                Descs.append(raw_get_desc_lonepair(atoms_fr,bond_center,mol_id,UNITCELL_VECTORS,NUM_MOL_ATOMS))
                i += 1 
        elif desctype == "allinone":
            # Descs = [raw_get_desc_lonepair_allinone(atoms_fr,bond_center,UNITCELL_VECTORS,NUM_MOL_ATOMS,Rcs,Rc,MaxAt) for bond_center in list_lonepair_coords]
            # using Torch
            Descs = raw_get_desc_lonepair_allinone_torch(atoms_fr,list_lonepair_coords, UNITCELL_VECTORS, Rcs, Rc, MaxAt)
    return np.array(Descs)

def raw_calc_lonepair_descripter_at_frame2(atoms_fr, list_mol_coords, at_list, NUM_MOL:int, UNITCELL_VECTORS, NUM_MOL_ATOMS:int, desctype = "allinone"):
    '''
    TODO :: desctypeとしてはallaloneのみ対応．
    1つのframe中の一種のローンペアの記述子を計算する．version2
    入力を見直す．
    せっかくat_listがあるので，これを使ってlist_lonepair_coordsを作成する．
    
    atomic__index : 原子量（原子のリストを取得するのと，原子座標の取得に使う）
    at_list      : atoms_frの中で求めたい原子の場所のリスト（0~NUM_ATOMSの中から）
    
    最も使いやすいかたちとしては，at_list
    
    TODO :: at_listは単に1分子内のO原子の数を数えるのに使っているだけなので，もっとよい方法を考える．
    TODO :: そもそもここではatomic_indexを入力としているが，よく考えると現在はitp_data.o_listがあるのだから，それを使ってcent_molの抽出ができるのでは？

    分子ID :: 分子1~分子NUM_MOLまで
    '''

    if desctype == "old":
        print("ERROR :: desctype = old is not supported.")
        sys.exit(1)
    
    # 記述子を求めたい原子座標の取得
    list_lonepair_coords = [coord for coord in list_mol_coords.reshape(-1,3)[at_list]]
    # 実際の記述子の計算
    Descs = [raw_get_desc_lonepair_allinone(atoms_fr,bond_center,UNITCELL_VECTORS,NUM_MOL_ATOMS) for bond_center in list_lonepair_coords]

    return np.array(Descs)


def raw_calc_lonepairmu_descripter_at_frame(list_mu_lp, list_atomic_nums, at_list, atomic_index:int):
    '''
    各種ローンペアの双極子の真値を計算するコード
    （元のコードでいうところのdata_y_chとか）
    まず，list_mu_bondsからbond_indexに対応するデータだけをmu_molに取り出す．
    '''
    data_y = []
    mu_mol = find_specific_lonepairmu(list_mu_lp, list_atomic_nums, atomic_index)
    if len(at_list) != 0: # 中身が0でなければ計算を実行
        for mu_b in mu_mol:
            data_y.append(mu_b)
    return np.array(data_y)


