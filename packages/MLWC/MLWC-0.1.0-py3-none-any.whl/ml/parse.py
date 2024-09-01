'''
inputファイルのparse専用のクラスと関数
'''


def read_inputfile(inputfilename:str):
    '''
    入力ファイルを読み込み，行ごとのリストにする
    '''
    # * read input file
    fp=open(inputfilename,mode="r")
    inputs = []
    
    for line in fp.readlines():
        # print(line.strip()) # !! debug
        inputs.append(line.strip()) # space/改行などを削除
    fp.close()
    return inputs



def locate_tag(inputs:list):
    '''
    入力ファイル（lines）から&で始まるタグをサーチする．
     &general
     &descripter
     &predict

    サーチして，タグごとに出力を分解する．
    '''
    # エラー処理のため-1で初期化しておく
    num_general = -1
    num_descripter = -1
    num_predict = -1
    # タグの位置を読み込み
    for num,i in enumerate(inputs):
        if i == "&general":
            num_general = num            
        if i == "&descriptor":
            num_descripter = num
        if i == "&predict":
            num_predict = num
    assert num_general != -1, "ERROR :: &general is not found"
    assert num_descripter != -1, "ERROR :: &descripter is not found"
    assert num_predict != -1, "ERROR :: &predict is not found"

    input_general    = []
    input_descripter = []
    input_predict    = []
    if num_descripter <= num_predict:
        for num,line in enumerate(inputs):
            if num_general<num<num_descripter:
                input_general.append(line.split("="))
            if num_descripter<num<num_predict:
                input_descripter.append(line.split("="))
            if num_predict<num:
                input_predict.append(line.split("="))
    else:
        print("ERROR :: num_descripter > num_predict ")
        return 1
    return input_general, input_descripter, input_predict



def find_input(inputs, str):
    '''
    入力ファイルから特定のキーワードをサーチする．

    input
    -------------
      inputs :: [keyword, value]がappendされた2次元配列．keywordを検索し，valueを返す

    output
    -------------
      output  :: keywordに対応するvalue.

    note
    -------------
     TODO :: キーワードが複数出てきた時は？
     TODO :: optional keywordがこのままだと扱えない．
    '''
    output = None # 見つからなかった場合はNoneになるようにしている．
    for i in inputs:
        if i[0] == str:
            output=i[1]
            print(" {0} :: {1}".format(str,output))
    if output == None:
        print("not found key :: ", str)
    return output

def decide_if_use_default(output, default_val):
    '''
    find_inputの出力を入力とする．
    もしoutput=Noneの場合は，default値を入れる．
    それ以外の場合はそのまま出力する．
    '''
    if output == None:
        return default_val
    else:
        return output

class var_general:
    '''
    descripter用の変数を一括管理する
    '''
    def __init__(self,input_general):
        import yaml
        import os
        import pkgutil
        # test=pkgutil.get_data('dieltools', 'data/inputparameter.yaml')
        # print(test)
        path = os.path.dirname(os.path.abspath(__file__)) + "/../data/inputparameter.yaml"
        print(path)
        # https://qiita.com/studio_haneya/items/9aad8f9ede11e58b41a8#7-%E3%83%87%E3%83%BC%E3%82%BF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8%E3%81%AB%E5%90%AB%E3%82%81%E3%82%8B
        # print(os.path.isfile(path))    
        with open(path, 'r') as yml:
            config = yaml.safe_load(yml)
        print(config["general"])
        self.itpfilename = find_input(input_general,"itpfilename") # itpファイル
        # yamlデータを使う方法
        self.input={}
        for key, value in config["general"].items():
            print(key,value)
            self.input[key] = find_input(input_general, key)
        print("finish reading self.input :: ", self.input)
            
    

    
class var_descripter:
    '''
    descripter用の変数を一括管理する
    bool値はここでintに変換しておく
    '''
    def __init__(self,input_descriptor):
        import yaml
        import os
        path = os.path.dirname(os.path.abspath(__file__)) + "/../data/inputparameter.yaml"
        print(path)
        with open(path, 'r') as yml:
            config = yaml.safe_load(yml)
        print(config["descriptor"])
        self.calc        =int(decide_if_use_default(find_input(input_descriptor,"calc"), 0)) # 計算するかどうかのフラグ（1がTrue，0がFalse）
        self.directory   =find_input(input_descriptor,"directory")
        # stdoutfile=find_input(inputs,"stdoutfile")
        self.xyzfilename =find_input(input_descriptor,"xyzfilename") #
        self.savedir     =find_input(input_descriptor,"savedir") # 記述子の保存dir
        self.descmode    =find_input(input_descriptor, "descmode") # wannier計算をしない（1）かする（2）か
        self.desctype    =decide_if_use_default(find_input(input_descriptor, "desctype"), "old") # 記述子の種類
        self.step        =find_input(input_descriptor, "step") # 計算するステップ数(optional)
        self.haswannier  =int(decide_if_use_default(find_input(input_descriptor,"haswannier"), 0)) # 1がTrue，0がFalse
        self.interval    =int(decide_if_use_default(find_input(input_descriptor,"interval"), 1)) # trajectoryを何ステップごとに処理するか．デフォルトは毎ステップ．
        self.desc_coh    =int(decide_if_use_default(find_input(input_descriptor, "desc_coh"),0)) # # 1がTrue，0がFalse
        self.Rcs         =float(decide_if_use_default(find_input(input_descriptor, "Rcs"), 4.0))
        self.Rc          =float(decide_if_use_default(find_input(input_descriptor, "Rc"),  6.0))
        self.MaxAt       =int(decide_if_use_default(find_input(input_descriptor, "MaxAt"), 24))
        self.trueonly    =int(decide_if_use_default(find_input(input_descriptor,"trueonly"), 0)) # trueyだけ計算する場合は1（1がtrue，0がfalse）
        
        # yamlデータを使う方法（yamlにキーとなるタグと，そのデフォルト値を保持している）
        self.input={}
        for key, value in config["descriptor"].items():
            print(key,value)
            self.input[key] = find_input(input_descriptor, key)
        print("finish reading self.input :: ", self.input)
class var_predict:
    '''
    predict用の変数を一括管理する
    '''
    def __init__(self,input_predict):
        import yaml
        import os
        path = os.path.dirname(os.path.abspath(__file__)) + "/../data/inputparameter.yaml"
        print(path)
        with open(path, 'r') as yml:
            config = yaml.safe_load(yml)
        print(config["predict"])
        # read input parameters
        self.calc        =int(decide_if_use_default(find_input(input_predict,"calc"),0)) # 計算するかどうかのフラグ（1がTrue，0がFalse）
        self.model_dir   =find_input(input_predict,"model_dir")
        # stdoutfile=find_input(inputs,"stdoutfile")
        self.desc_dir    =find_input(input_predict,"desc_dir") # 記述子のロードdir
        self.modelmode   =find_input(input_predict,"modelmode") # normal or rotate (2023/4/16)
        self.bondspecies =int(decide_if_use_default(find_input(input_predict,"bondspecies"), 4)) # デフォルトの4はメタノールに対応
        self.save_truey  =int(decide_if_use_default(find_input(input_predict,"save_truey"), 0)) # 1がTrue，0がFalse（true_yを保存するかどうか．）
        # yamlデータを使う方法
        self.input={}
        for key, value in config["predict"].items():
            print(key,value)
            self.input[key] = find_input(input_predict, key)
        print("finish reading self.input :: ", self.input)
