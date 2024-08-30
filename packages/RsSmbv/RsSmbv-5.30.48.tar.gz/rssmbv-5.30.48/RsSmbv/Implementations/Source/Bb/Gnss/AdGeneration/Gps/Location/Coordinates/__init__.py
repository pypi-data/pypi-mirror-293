from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoordinatesCls:
	"""Coordinates commands group definition. 5 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coordinates", core, parent)

	@property
	def decimal(self):
		"""decimal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_decimal'):
			from .Decimal import DecimalCls
			self._decimal = DecimalCls(self._core, self._cmd_group)
		return self._decimal

	@property
	def dms(self):
		"""dms commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dms'):
			from .Dms import DmsCls
			self._dms = DmsCls(self._core, self._cmd_group)
		return self._dms

	# noinspection PyTypeChecker
	def get_rframe(self) -> enums.RefFrame:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:RFRame \n
		Snippet: value: enums.RefFrame = driver.source.bb.gnss.adGeneration.gps.location.coordinates.get_rframe() \n
		Sets the reference frame. \n
			:return: reference_frame: PZ90| WGS84
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:RFRame?')
		return Conversions.str_to_scalar_enum(response, enums.RefFrame)

	def set_rframe(self, reference_frame: enums.RefFrame) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:RFRame \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.location.coordinates.set_rframe(reference_frame = enums.RefFrame.PZ90) \n
		Sets the reference frame. \n
			:param reference_frame: PZ90| WGS84
		"""
		param = Conversions.enum_scalar_to_str(reference_frame, enums.RefFrame)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:RFRame {param}')

	def clone(self) -> 'CoordinatesCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CoordinatesCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
