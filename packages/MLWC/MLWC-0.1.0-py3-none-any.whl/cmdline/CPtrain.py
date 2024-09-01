#!/usr/bin/env python
# coding: utf-8
from __future__ import annotations # fugaku上のpython3.8で型指定をする方法（https://future-architect.github.io/articles/20201223/）

import argparse
import sys
import numpy as np
import argparse
import sys
import os
# import matplotlib.pyplot as plt


# python version check
from include.small import python_version_check
python_version_check()


try:
    import ase.io
except ImportError:
    sys.exit("Error: ase.io not installed")
try:
    import ase
except ImportError:
    sys.exit("Error: ase not installed")


import torch       # ライブラリ「PyTorch」のtorchパッケージをインポート
import torch.nn as nn  # 「ニューラルネットワーク」モジュールの別名定義

import argparse
from ase.io.trajectory import Trajectory
import ml.parse # my package
# import home-made package
# import importlib
# import cpmd

# 物理定数
from include.constants import constant
# Debye   = 3.33564e-30
# charge  = 1.602176634e-019
# ang      = 1.0e-10
coef    = constant.Ang*constant.Charge/constant.Debye


## our packages
import cmdline.cptrain_train  as cptrain_train
import cmdline.cptrain_test   as cptrain_test
import cmdline.cptrain_sample as cptrain_sample

def command_help(args):
    print(parser.parse_args([args.command, "--help"]))
    

def parse_cml_args(cml):
    parser = argparse.ArgumentParser(description="CPtrain.py")
    subparsers = parser.add_subparsers()
    
    # * ------------
    # cptrain train
    parser_train = subparsers.add_parser("train", help="train models")
    # parser_cpmd.set_defaults(handler=command_cpmd)
    # create sub-parser for sub-command cool
    # cpmd_sub_parsers = parser_train.add_subparsers(help='sub-command help')
    # 
    parser_train.add_argument("-i", "--input", \
                        help='input file name. .\n', \
                        # default="train.yaml"
                        )
    
    parser_train.set_defaults(handler=cptrain_train.command_cptrain_train)
    
    # * ------------
    # cptrain test
    parser_test = subparsers.add_parser("test", help="test models")
    # parser_cpmd.set_defaults(handler=command_cpmd)
    # create sub-parser for sub-command cool
    # cpmd_sub_parsers = parser_train.add_subparsers(help='sub-command help')
    # args.model,args.xyz,args.itp
    parser_test.add_argument("-m", "--model", required=True,\
                        help='input model file name. The format should be torchscript.\n', \
                        # default="test.yaml"
                        )
    
    parser_test.add_argument("-x", "--xyz", required=True,\
                        help='input xyz file name with WCs.\n', \
                        # default="IONS+CENTERS.xyz"
                        )

    parser_test.add_argument("-i", "--mol", required=True,\
                        help='input mol file name. The format should be mol.\n', \
                        # default="input_GMX.mol"
                        )
    
    parser_test.add_argument("-b", "--bond", required=True,\
                        help='bond type to calculate. \n', \
                        choices=['CH', 'CC', 'CO', 'OH', 'O', 'COC', 'COH'],\
                        # default="input_GMX.mol"
                        )
    # 
    parser_test.set_defaults(handler=cptrain_test.command_cptrain_test)
    
        # * ------------
    # cpmake sample 
    parser_sample = subparsers.add_parser("sample", \
                                         help="print sample input files for CPtrain.py and dieltools.")
    parser_sample.set_defaults(handler=cptrain_sample.command_sample)
    return parser, parser.parse_args(cml)



def main():
    '''
         Simple script for plotting CP.x output
        Usage:
        $ python CPextract.py file

        For details of available options, please type
        $ python CPextract.py -h
    '''
    print(" ")
    print(" *****************************************************************")
    print("                       CPtrain.py                                 ")
    print("                       Version. 0.0.1                             ")
    print(" *****************************************************************")
    print(" ")

    parser, args = parse_cml_args(sys.argv[1:])

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()

# 
if __name__ == '__main__':
    main()
