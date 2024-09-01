import ase
import ase.io
import numpy as np

def calc_velocity(traj:list[ase.Atoms],timestep:float):
    """ calculate velocity of each MD frame

    Args:
        traj (ase.Atoms): _description_
        timestep (float): timestep in fs
    """
    import numpy as np
    L = traj[0].get_cell()[0][0] # get cell
    # logger.info("Lattice parameter :: {0}".format(L))
    # num_mol
    NUM_ATOM = int(len(traj[0].get_atomic_numbers()))
    print(f"NUM_ATOM :: {NUM_ATOM}")
    
    # logger.info("LEN(atomic_index)  :: {0}".format(np.shape(atomic_index)))
    # 速度の初期化
    atom_velocity = np.zeros([len(traj)-1,NUM_ATOM,3])

    for counter,atoms in enumerate(traj): # frameに関するloop 
        if counter == len(traj)-1: #最終フレームはskip
            break
        # 座標の座標
        coord_t    = traj[counter].get_positions()
        coord_t_dt = traj[counter+1].get_positions()
        # 座標の差分を計算
        diff = coord_t_dt - coord_t
        # pbcのチェック
        tmp = np.where(diff>L,diff-2.0*L,diff)
        diff_pbc = np.where(tmp<-L,tmp+2.0*L,tmp)        
        # 重心速度 (fs to ps)
        velocity = diff_pbc/(timestep/1000)  
        # 代入
        atom_velocity[counter] = velocity
    return atom_velocity


def calc_com_velocity(traj:list[ase.Atoms],NUM_ATOM_PER_MOL:int, timestep:float):
    
    L = traj[0].get_cell()[0][0] # get cell
    # 分子重心の速度を計算
    # 分子の重心座標をnumpyから出す．
    # 分子についてのloopが必要．
    # 先に分子のindexを取得する必要がある．
    # その際，BCとXを除く
    traj_atomic_number = traj[0].get_atomic_numbers()
    # TODO :: 現在C,H,Oのみ
    atomic_index = np.where( (traj_atomic_number == 1) | (traj_atomic_number == 6) | (traj_atomic_number == 8))[0]
    # 分子数
    NUM_MOL = int(len(atomic_index)/NUM_ATOM_PER_MOL)
    print(f"NUM_MOL :: {NUM_MOL}")
    # 速度の初期化
    com_velocity = np.zeros([len(traj)-1,NUM_MOL,3])
    for counter,atoms in enumerate(traj): # frameに関するloop 
        if counter == len(traj)-1: #最終フレームはskip
            break
        for mol_id in range(NUM_MOL):
            com_t    = atoms[atomic_index[NUM_ATOM_PER_MOL*mol_id:NUM_ATOM_PER_MOL*(mol_id+1)]].get_center_of_mass()
            com_t_dt = traj[counter+1][atomic_index[NUM_ATOM_PER_MOL*mol_id:NUM_ATOM_PER_MOL*(mol_id+1)]].get_center_of_mass()
            # 座標の差分を計算
            diff = com_t_dt - com_t
            # pbcのチェック
            tmp = np.where(diff>L,diff-2.0*L,diff)
            diff_pbc = np.where(tmp<-L,tmp+2.0*L,tmp)        
            # 重心速度 (fs to ps)
            velocity = diff_pbc/(timestep/1000)  
            # 代入
            com_velocity[counter,mol_id] = velocity
    return com_velocity


def calc_vel_acf(atom_velocity):
    """atom_velocityのACFを計算する

    Args:
        atom_velocity (_type_): [frame,NUM_ATOM,3]型

    Returns:
        acf _type_: [NUM_ATOM,acf]型，acfの長さはlen(frame)
    """
    
    import statsmodels.api as sm
    import numpy as np
    if np.shape(atom_velocity)[2] != 3:
        print("ERROR :: wrong shape ")
    if len(np.shape(atom_velocity)) != 3:
        print("ERROR :: wrong shape ")
        
    # 
    len_traj = len(atom_velocity)
    NUM_ATOM = len(atom_velocity[0])
    # * acfを計算する．
    acf = np.zeros([NUM_ATOM,len_traj])
    for atom_id in range(NUM_ATOM):
        acf_x = sm.tsa.stattools.acf(atom_velocity[:,atom_id,0],fft=True,nlags=len(atom_velocity))*np.std(atom_velocity[:,atom_id,0]) * np.std(atom_velocity[:,atom_id,0])
        acf_y = sm.tsa.stattools.acf(atom_velocity[:,atom_id,1],fft=True,nlags=len(atom_velocity))*np.std(atom_velocity[:,atom_id,1]) * np.std(atom_velocity[:,atom_id,1])
        acf_z = sm.tsa.stattools.acf(atom_velocity[:,atom_id,2],fft=True,nlags=len(atom_velocity))*np.std(atom_velocity[:,atom_id,2]) * np.std(atom_velocity[:,atom_id,2])
        # !! 内積なので足し上げるのが正解
        acf_mean = (acf_x+acf_y+acf_z) 
        acf[atom_id] = acf_mean
    # 最後に平均化（これは速度vdosのみ）
    # acf = acf/np.shape(atom_velocity)[1]
    # logger.info("LEN(ACF)  :: {0}".format(len(acf)))
    return acf

def average_vdos_atomic_species(acf, atoms, atomic_number:int):
    
    # 原子種に応じた平均
    # indexを取得([0]が必要)
    atomic_index = np.where(atoms.get_atomic_numbers()==atomic_number)[0]
    # TODO:: get_chemical_symbols()を使った方が（WC用に）良い．
    acf_mean = np.mean(acf[atomic_index],axis=0)
    return acf_mean

def average_vdos_specify_index(acf, atoms, index:list[int], num_atoms_per_mol:int):
    '''
    indexを自分で指定する場合
    とりあえずは原子の
    '''
    # indexに応じたindexを作成
    NUM_MOL = int(len(atoms)/num_atoms_per_mol)
    atomic_index = []
    for i in range(NUM_MOL):
        atomic_index = np.concatenate([np.array(atomic_index), np.array(index)+i*num_atoms_per_mol])
    # TODO:: get_chemical_symbols()を使った方が（WC用に）良い．
    acf_mean = np.mean(acf[atomic_index],axis=0)
    return acf_mean



def calc_vdos(acf, timestep:float):
    import numpy as np
    if len(np.shape(acf)) != 1:
        print("ERROR :: acf shape not correct")    
    TIMESTEP = timestep/1000 # fs to ps
    # logger.info("TIMESTEP [ps] :: {0}".format(TIMESTEP))

    time_data=len(acf) # データの長さ
    freq=np.fft.fftfreq(time_data, d=TIMESTEP) # omega
    length=freq.shape[0]//2 + 1 # rfftでは，fftfreqのうちの半分しか使わない．
    rfreq=freq[0:length] # これが振動数(in THz)

    #usage:: numpy.fft.fft(data, n=None, axis=-1, norm=None)
    ans=np.fft.rfft(acf, norm="forward") #こっちが1/Nがかかる規格化．(time_data?)
    #ans=np.fft.rfft(fft_data, norm="backward") #その他の規格化1:何もかからない
    #ans=np.fft.rfft(fft_data, norm="ortho")　　#その他の規格化2:1/sqrt(N))がかかる

    # VDOS:: time_data*TIMESTEPは合計時間をかける意味
    fftvdos = 2*ans.real*(time_data*TIMESTEP)
    
    # pandas化
    import pandas as pd
    df = pd.DataFrame()
    df["thz"] = rfreq
    df["freq_kayser"] = rfreq*33.3
    df["vdos"] = fftvdos
    return df
