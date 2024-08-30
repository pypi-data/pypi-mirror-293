from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, power_offset: float, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:POWer:OFFSet \n
		Snippet: driver.source.bb.gnss.svid.galileo.power.offset.set(power_offset = 1.0, satelliteSvid = repcap.SatelliteSvid.Default) \n
		Reduces the signal of the selected SV ID by the defined value. \n
			:param power_offset: float Range: -21 to 0
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
		"""
		param = Conversions.decimal_value_to_str(power_offset)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:POWer:OFFSet {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GALileo:POWer:OFFSet \n
		Snippet: value: float = driver.source.bb.gnss.svid.galileo.power.offset.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Reduces the signal of the selected SV ID by the defined value. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: power_offset: float Range: -21 to 0"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GALileo:POWer:OFFSet?')
		return Conversions.str_to_float(response)
