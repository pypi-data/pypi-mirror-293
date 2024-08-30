from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValueCls:
	"""Value commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("value", core, parent)

	def get(self, xvalue: float, xunit: enums.Unknown) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:AMAM:VALue \n
		Snippet: value: float = driver.source.iq.doherty.amam.value.get(xvalue = 1.0, xunit = enums.Unknown.DBM) \n
		No command help available \n
			:param xvalue: No help available
			:param xunit: No help available
			:return: delta_power: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('xvalue', xvalue, DataType.Float), ArgSingle('xunit', xunit, DataType.Enum, enums.Unknown))
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty:AMAM:VALue? {param}'.rstrip())
		return Conversions.str_to_float(response)

	def get_level(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:AMAM:VALue:LEVel \n
		Snippet: value: float = driver.source.iq.doherty.amam.value.get_level() \n
		No command help available \n
			:return: delta_power: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DOHerty:AMAM:VALue:LEVel?')
		return Conversions.str_to_float(response)

	def get_pep(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:AMAM:VALue:PEP \n
		Snippet: value: float = driver.source.iq.doherty.amam.value.get_pep() \n
		No command help available \n
			:return: delta_power: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DOHerty:AMAM:VALue:PEP?')
		return Conversions.str_to_float(response)
