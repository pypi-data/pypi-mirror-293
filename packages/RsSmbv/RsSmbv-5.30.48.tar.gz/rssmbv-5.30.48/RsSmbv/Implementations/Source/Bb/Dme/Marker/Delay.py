from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def set(self, delay: int, marker=repcap.Marker.Default) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:MARKer<CH>:DELay \n
		Snippet: driver.source.bb.dme.marker.delay.set(delay = 1, marker = repcap.Marker.Default) \n
		Sets the delay between the marker signal at the marker outputs relative to the signal generation start. \n
			:param delay: integer Range: 0 to 127
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
		"""
		param = Conversions.decimal_value_to_str(delay)
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:MARKer{marker_cmd_val}:DELay {param}')

	def get(self, marker=repcap.Marker.Default) -> int:
		"""SCPI: [SOURce<HW>]:[BB]:DME:MARKer<CH>:DELay \n
		Snippet: value: int = driver.source.bb.dme.marker.delay.get(marker = repcap.Marker.Default) \n
		Sets the delay between the marker signal at the marker outputs relative to the signal generation start. \n
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
			:return: delay: integer Range: 0 to 127"""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DME:MARKer{marker_cmd_val}:DELay?')
		return Conversions.str_to_int(response)
