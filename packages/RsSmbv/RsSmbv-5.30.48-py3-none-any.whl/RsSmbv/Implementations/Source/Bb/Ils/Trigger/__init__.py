from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 12 total commands, 4 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	@property
	def arm(self):
		"""arm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arm'):
			from .Arm import ArmCls
			self._arm = ArmCls(self._core, self._cmd_group)
		return self._arm

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	@property
	def external(self):
		"""external commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:TRIGger:RMODe \n
		Snippet: value: enums.TrigRunMode = driver.source.bb.ils.trigger.get_rmode() \n
		Queries the signal generation status. \n
			:return: run_mode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:TRIGger:SLENgth \n
		Snippet: value: int = driver.source.bb.ils.trigger.get_slength() \n
		Defines the length of the signal sequence that is output in the SINGle trigger mode. \n
			:return: seq_length: integer Range: 1 samples to 2^32-1 samples
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, seq_length: int) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:TRIGger:SLENgth \n
		Snippet: driver.source.bb.ils.trigger.set_slength(seq_length = 1) \n
		Defines the length of the signal sequence that is output in the SINGle trigger mode. \n
			:param seq_length: integer Range: 1 samples to 2^32-1 samples
		"""
		param = Conversions.decimal_value_to_str(seq_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TrigSour:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:TRIGger:SOURce \n
		Snippet: value: enums.TrigSour = driver.source.bb.ils.trigger.get_source() \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors EGT1: External global trigger
			- In primary-secondary instrument mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: trigger_source: INTernal| EGT1| EXTernal| BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSour)

	def set_source(self, trigger_source: enums.TrigSour) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:TRIGger:SOURce \n
		Snippet: driver.source.bb.ils.trigger.set_source(trigger_source = enums.TrigSour.BBSY) \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors EGT1: External global trigger
			- In primary-secondary instrument mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param trigger_source: INTernal| EGT1| EXTernal| BBSY
		"""
		param = Conversions.enum_scalar_to_str(trigger_source, enums.TrigSour)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:[TRIGger]:SEQuence \n
		Snippet: value: enums.DmTrigMode = driver.source.bb.ils.trigger.get_sequence() \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single \n
			:return: trigger_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, trigger_mode: enums.DmTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.ils.trigger.set_sequence(trigger_mode = enums.DmTrigMode.AAUTo) \n
			INTRO_CMD_HELP: Selects the trigger mode: \n
			- AUTO = auto
			- RETRigger = retrigger
			- AAUTo = armed auto
			- ARETrigger = armed retrigger
			- SINGle = single \n
			:param trigger_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(trigger_mode, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:TRIGger:SEQuence {param}')

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
