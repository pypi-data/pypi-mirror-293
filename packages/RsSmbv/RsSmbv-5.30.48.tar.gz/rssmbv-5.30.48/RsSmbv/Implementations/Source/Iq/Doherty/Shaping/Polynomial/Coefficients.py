from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoefficientsCls:
	"""Coefficients commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coefficients", core, parent)

	def set(self, ipart_0: float, j_0: float, i_1: float, j_1: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients \n
		Snippet: driver.source.iq.doherty.shaping.polynomial.coefficients.set(ipart_0 = 1.0, j_0 = 1.0, i_1 = 1.0, j_1 = 1.0) \n
		No command help available \n
			:param ipart_0: No help available
			:param j_0: No help available
			:param i_1: No help available
			:param j_1: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ipart_0', ipart_0, DataType.Float), ArgSingle('j_0', j_0, DataType.Float), ArgSingle('i_1', i_1, DataType.Float), ArgSingle('j_1', j_1, DataType.Float))
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients {param}'.rstrip())

	# noinspection PyTypeChecker
	class CoefficientsStruct(StructBase):
		"""Response structure. Fields: \n
			- Ipart_0: float: No parameter help available
			- J_0: float: No parameter help available
			- I_1: float: No parameter help available
			- J_1: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ipart_0'),
			ArgStruct.scalar_float('J_0'),
			ArgStruct.scalar_float('I_1'),
			ArgStruct.scalar_float('J_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ipart_0: float = None
			self.J_0: float = None
			self.I_1: float = None
			self.J_1: float = None

	def get(self) -> CoefficientsStruct:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients \n
		Snippet: value: CoefficientsStruct = driver.source.iq.doherty.shaping.polynomial.coefficients.get() \n
		No command help available \n
			:return: structure: for return value, see the help for CoefficientsStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients?', self.__class__.CoefficientsStruct())

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:CATalog \n
		Snippet: value: List[str] = driver.source.iq.doherty.shaping.polynomial.coefficients.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:LOAD \n
		Snippet: driver.source.iq.doherty.shaping.polynomial.coefficients.load(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:STORe \n
		Snippet: driver.source.iq.doherty.shaping.polynomial.coefficients.set_store(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:STORe {param}')
