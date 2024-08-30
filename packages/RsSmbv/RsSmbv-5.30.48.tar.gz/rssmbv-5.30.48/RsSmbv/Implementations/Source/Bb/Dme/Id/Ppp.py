from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PppCls:
	"""Ppp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ppp", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PPP:[STATe] \n
		Snippet: value: bool = driver.source.bb.dme.id.ppp.get_state() \n
		Sets the state of the pair of pulse pairs for the ID signal generation. When enabled a pair of pulse pairs is transmitted
		during the set [:SOURce<hw>][:BB]:DME:ID:RATE. \n
			:return: pair_of_pulse_pair: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:PPP:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, pair_of_pulse_pair: bool) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PPP:[STATe] \n
		Snippet: driver.source.bb.dme.id.ppp.set_state(pair_of_pulse_pair = False) \n
		Sets the state of the pair of pulse pairs for the ID signal generation. When enabled a pair of pulse pairs is transmitted
		during the set [:SOURce<hw>][:BB]:DME:ID:RATE. \n
			:param pair_of_pulse_pair: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(pair_of_pulse_pair)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:PPP:STATe {param}')
