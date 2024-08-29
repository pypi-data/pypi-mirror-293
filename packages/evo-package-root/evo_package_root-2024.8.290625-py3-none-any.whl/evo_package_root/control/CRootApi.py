#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_root.entity import *
from evo_package_root.utility import *
from evo_framework.core.evo_core_api.entity.EApiConfig import EApiConfig

# ---------------------------------------------------------------------------------------------------------------------------------------
# CRootApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CRootApi
"""
class CRootApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CRootApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CRootApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CRootApi instance
	"""
	@staticmethod
	def getInstance():
		if CRootApi.__instance is None:
			cObject = CRootApi()  
			cObject.doInit()  
		return CRootApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			URootApi.getInstance().doInit()
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("root-set", callback=self.onSet, input=EApiConfig, output=EApiText )
			api0.description="root-set _DESCRIPTION_"
			api0.required="*"

			api1 = self.newApi("root-get", callback=self.onGet, input=EApiQuery, output=EApiConfig )
			api1.description="root-get _DESCRIPTION_"
			api1.required="*"

			api2 = self.newApi("root-query", callback=self.onQuery, input=EApiQuery, output=EEApiConfigMap )
			api2.description="root-query _DESCRIPTION_"
			api2.required="*"

			api3 = self.newApi("root-get-package", callback=self.onGetPackage, input=EApiQuery, output=EEApiPackage )
			api3.description="root-set_eapiconfig _DESCRIPTION_"
			api3.required="*"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onSet api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onSet(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onSet: {eAction} ")

					
			async for eActionOutput in URootApi.getInstance().doOnSet(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGet api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGet(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGet: {eAction} ")

					
			async for eActionOutput in URootApi.getInstance().doOnGet(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onQuery api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onQuery(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onQuery: {eAction} ")

					
			async for eActionOutput in URootApi.getInstance().doOnQuery(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetPackage api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetPackage(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetPackage: {eAction} ")

					
			async for eActionOutput in URootApi.getInstance().doOnGetPackage(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
