from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CpvpCls:
	"""Cpvp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cpvp", core, parent)

	def set(self, cs_pv_p: str, bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CPVP \n
		Snippet: driver.source.bb.btooth.cs.cpvp.set(cs_pv_p = rawAbc, bitcount = 1) \n
		No command help available \n
			:param cs_pv_p: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cs_pv_p', cs_pv_p, DataType.RawString), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CPVP {param}'.rstrip())

	# noinspection PyTypeChecker
	class CpvpStruct(StructBase):
		"""Response structure. Fields: \n
			- Cs_Pv_P: str: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Cs_Pv_P'),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_Pv_P: str = None
			self.Bitcount: int = None

	def get(self) -> CpvpStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CPVP \n
		Snippet: value: CpvpStruct = driver.source.bb.btooth.cs.cpvp.get() \n
		No command help available \n
			:return: structure: for return value, see the help for CpvpStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CPVP?', self.__class__.CpvpStruct())
