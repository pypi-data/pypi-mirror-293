from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PzCls:
	"""Pz commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pz", core, parent)

	def set(self, longitude: float, latitude: float, altitude: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:BEIDou:LOCation:COORdinates:DECimal:PZ \n
		Snippet: driver.source.bb.gnss.adGeneration.beidou.location.coordinates.decimal.pz.set(longitude = 1.0, latitude = 1.0, altitude = 1.0) \n
		Sets the geographic reference location in decimal format. \n
			:param longitude: float Range: -180 to 180
			:param latitude: float Range: -90 to 90
			:param altitude: float Range: -10E3 to 50E6
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('longitude', longitude, DataType.Float), ArgSingle('latitude', latitude, DataType.Float), ArgSingle('altitude', altitude, DataType.Float))
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:BEIDou:LOCation:COORdinates:DECimal:PZ {param}'.rstrip())

	# noinspection PyTypeChecker
	class PzStruct(StructBase):
		"""Response structure. Fields: \n
			- Longitude: float: float Range: -180 to 180
			- Latitude: float: float Range: -90 to 90
			- Altitude: float: float Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def get(self) -> PzStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:BEIDou:LOCation:COORdinates:DECimal:PZ \n
		Snippet: value: PzStruct = driver.source.bb.gnss.adGeneration.beidou.location.coordinates.decimal.pz.get() \n
		Sets the geographic reference location in decimal format. \n
			:return: structure: for return value, see the help for PzStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:BEIDou:LOCation:COORdinates:DECimal:PZ?', self.__class__.PzStruct())
