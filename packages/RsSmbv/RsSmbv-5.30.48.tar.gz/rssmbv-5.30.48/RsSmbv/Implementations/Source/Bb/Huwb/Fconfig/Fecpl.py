from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FecplCls:
	"""Fecpl commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fecpl", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:FECPl:STATe \n
		Snippet: value: bool = driver.source.bb.huwb.fconfig.fecpl.get_state() \n
		No command help available \n
			:return: fecp_l: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:FECPl:STATe?')
		return Conversions.str_to_bool(response)
