#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiConfig import EApiConfig
#========================================================================================================================================
"""EEApiConfigMap

    EEApiConfigMap _DOC_
    
"""
class EEApiConfigMap(EObject):

    VERSION:str="0ec01a6baa3514d7aa6b84080e01be289953f585ff940fcdf13808dc2694d9ab"

    def __init__(self):
        super().__init__()
        
        self.mapEApiConfig:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteMap(self.mapEApiConfig, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.mapEApiConfig = self._doReadMap(EApiConfig, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmapEApiConfig:{self.mapEApiConfig}",
                            ]) 
        return strReturn
    