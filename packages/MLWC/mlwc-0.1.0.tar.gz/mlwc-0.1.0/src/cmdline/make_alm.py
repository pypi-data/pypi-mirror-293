#!/usr/bin/env python3

# make_alm.py
#
# Simple script to make alm input from pw.in or POSCAR (supercell).
#
# caution 1 : ase is used for extract crystal structure from pw.in and POSCAR.
# 
#
# ase is using cartesian coordinates, while ALAMODE is using fractional coordinate.
# We need to convert these coordinates.
#

import numpy as np
import sys

# ====================
# parserの設定

def parse_cml_args(cml):
  import argparse
  '''
  CML parser.
  '''
  
  description='''
  Simple script for making alamode alm input
  Usage:
  $ python make_alm.py file
  
  For details of available options, please type
  $ python make_alm.py -h
  '''

  # make parser
  arg = argparse.ArgumentParser(description=description, add_help=True)
  
  arg.add_argument('input', help='POSCAR-type or QE-type file. default is SPOSCAR',default='SPOSCAR')
  arg.add_argument('output', help='ALAMODE-type output file', default="sugeest.in")
  arg.add_argument('-f', '--format', help='input file format (QE or VASP). \
  If not specified, make_alm.py automatically detect the format from input filenames. \
  If a input filename ends with POSCAR, format is VASP. \
  If a input filename ends with pw.in or scf.in, format is QE.' ) 
  return arg.parse_args(cml)
  

def VASP_write(VASP_input, ALM_output):
  '''
  VASP POSCAR parser
  --------
  
  '''
  import linecache
  #
  f   = open(VASP_input, 'r') # read SPOSCAR
  f2  = open(ALM_output, "w") # output suggest.in

  # カウンター
  counter=0  #行数をカウント
  counter2=0 #原子数カウント
  #
  f2.write("&general \n")
  f2.write("PREFIX = suggest\n")
  f2.write(" MODE = suggest \n")

  # 最初にNAT/NKD/KDを取得しておく
  KD = linecache.getline(VASP_input, 6) # atomic species
  NKD = len(KD.split())                 # # of species
  NAT_str = linecache.getline(VASP_input, 7).split()
  NAT = np.sum(np.array([int(s) for s in NAT_str])) # # of atoms
  # https://qiita.com/Kodaira_/items/eb5cdef4c4e299794be3
  linecache.clearcache()
  #
  f2.write(" NAT = "+ str(NAT) + " \n")
  f2.write(" NKD = "+ str(NKD) + " \n")
  f2.write(" KD = "+KD+" \n")
  f2.write("/\n")
  #
  #
  while True:
    data = f.readline()
    # dataが空行になったら出る．POSCARには速度情報が入ることがあるのでこれを除去するため．
    # 単にdata=="\n"だと"  \n"のような場合を排除できないので，splitするのが確実．
    if data.split() == []:
      break
    # debug:: print(data.split())
    ##
    ##
    if counter==2:
      f2.write("&interaction\n")
      f2.write("NORDER = 1  # 1: harmonic, 2: cubic, ..\n")
      f2.write("/\n")
      f2.write("&cell\n")
      f2.write("1.8897259886\n")  # convert from bohr to Ang
    #
    ## lattice constantを出力
    if counter==2 or counter==3 or counter==4:
        f2.write(data)  #print (data)
    #
    if counter==4:
      f2.write("/\n")
      f2.write("&cutoff\n")
      f2.write("*-* None\n")
      f2.write("/\n")
      f2.write("&position\n")


    #
    ## 各原子の数をget
    if counter==6:
      num_spices=data.strip("\n").split()
      num_atoms=[int(i) for i in num_spices]
      #print("原子種")
      #print(num_atoms)
      # num_atomに沿ったリストを作成( 1スタートなのでi+1になっている)
      ans=[int(i)+1 for i,num in enumerate(num_atoms) for k in range(num) ]
    #
    ## 座標を出力
    if counter >= 8:
      f2.write(str(ans[counter2])+" "+ data)
      counter2=counter2+1
    #
    counter=counter+1

  f.close()
  f2.close()
  # 成功チェック
  if counter2 == np.array(ans).shape[0]:
    print("")
    print(" convert from POSCAR to suggest.in :: SUCCESS")
    print(" # of atoms ::                    : %s" % counter2)
    print("")
  #
  return 0


def QE_write(QE_input, ALM_output):
  import numpy as np
  import ase.units
  from   ase.io import read

  # get atoms object
  atoms = read(QE_input)
  
  # 原子の種類とそのリスト(重複なし)
  symbols=atoms.get_chemical_symbols()
  symbols_key=list(dict.fromkeys(symbols))

  # 原子種を数字に置換
  symbols_num=[]
  for index, value in enumerate(symbols):
    for sub_index, sub_value in enumerate(symbols_key):
      if value == sub_value:
        symbols_num.append(sub_index+1)

  # 結晶ベクトル(Angstrom, デカルト座標)
  cells=atoms.get_cell()
  
  # 原子座標(Angstrom, デカルト座標)
  positions=atoms.get_positions()
  '''
  aseの原子座標は通常のデカルト座標だが，それをfractional coordinateに変換
  '''
  # 格子ベクトル
  A = np.array(cells).T
  A_inv = np.linalg.inv(A)
  
  # Perform the inverse operation to get fractional coordinates. 
  B = np.matmul(A_inv, positions.T).T
  
  # あまりに成分が小さいやつは0で置換しちゃう
  B_thr=np.where(abs(B)<0.00000000001, 0, B)

  '''
  alm.outを作成
  '''
  f2  = open(ALM_output, "w") # output suggest.in

  # カウンター
  counter=0  #行数をカウント
  counter2=0 #原子数カウント
  #
  f2.write("&general \n")
  f2.write("PREFIX = suggest\n")
  f2.write(" MODE = suggest \n")

  # 最初にNAT/NKD/KDを取得しておく
  KD      = " ".join(symbols_key)      # atomic species
  NKD     = len(symbols_key)           # of species
  NAT     = len(symbols)               # of atoms
  # https://qiita.com/Kodaira_/items/eb5cdef4c4e299794be3
  #
  f2.write(" NAT = "+ str(NAT) + " \n")
  f2.write(" NKD = "+ str(NKD) + " \n")
  f2.write(" KD =  "+ KD       + " \n")
  f2.write("/\n")
  f2.write("&interaction\n")
  f2.write("NORDER = 1  # 1: harmonic, 2: cubic, ..\n")
  f2.write("/\n")
  f2.write("&cell\n")
  f2.write("{}\n".format(ase.units.Bohr))  # convert from bohr to Ang
  for i in range(3): # unit cells
    f2.write("{:.16f} {:.16f} {:.16f} \n".format(cells[i][0], cells[i][1], cells[i][2]))
  f2.write("/\n")
  f2.write("&cutoff\n")
  f2.write("*-* None\n")
  f2.write("/\n")
  f2.write("&position\n")
  # print for alm
  for i in range(len(symbols)):
    f2.write("{:2d} {:.16f} {:.16f} {:.16f} \n".format(symbols_num[i], B_thr[i][0], B_thr[i][1], B_thr[i][2]))

  f2.close()
  # 成功チェック
  print(" ---------------  ")
  print(" convert from pw.in to suggest.in :: SUCCESS")
  #print(" cell       ::                    : %s" % )
  print(" # of atoms ::                    : %s" % len(symbols))
  print("")
  #
  return 0


def main():
  #
  print("*****************************************************************")
  print("           make_alm.py --  Generator of ALM input file           ")
  print("                      Version. 0.0.1                             ")
  print("*****************************************************************")
  print("")
  #
  args       = parse_cml_args(sys.argv[1:])
  INPUT      =args.input
  ALM_output =args.output
  FORMAT     =args.format
  # ====================
  #
  print(" Input File                     : %s" % INPUT)
  print(" Output File                    : %s" % ALM_output)
  print(" Input Format                   : %s" % FORMAT)
  print("")
  #
  if   FORMAT == "QE":
    QE_write(INPUT, ALM_output)
  elif FORMAT == "VASP":
    VASP_write(INPUT, ALM_output)
  elif FORMAT == None:
    if INPUT.endswith("POSCAR"):
      VASP_write(INPUT, ALM_output)
    elif INPUT.endswith("pw.in"):
      QE_write(INPUT, ALM_output)
    elif INPUT.endswith("scf.in"):
      QE_write(INPUT, ALM_output)
    else:
      print(" ERROR :: invalid Input file name.")
  return 0
    
      
    
  


  

if __name__ == '__main__':
  main()
