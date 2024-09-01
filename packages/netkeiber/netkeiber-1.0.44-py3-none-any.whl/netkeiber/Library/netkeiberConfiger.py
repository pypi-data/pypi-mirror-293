from LibHanger.Library.uwGlobals import configer
from LibHanger.Library.uwGlobals import *
from netkeiber.Library.netkeiberGlobals import *

class netkeiberConfiger(configer):
    
    """
    netkeiber共通設定クラス
    """
    
    def __init__(self, _tgv:netkeiberGlobal, _file, _configFolderName):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__(_tgv, _file, _configFolderName)
        
        # netkeibar.ini
        da = netkeiberConfig()
        da.getConfig(_file, _configFolderName)

        # gvセット
        _tgv.netkeiberConfig = da
        