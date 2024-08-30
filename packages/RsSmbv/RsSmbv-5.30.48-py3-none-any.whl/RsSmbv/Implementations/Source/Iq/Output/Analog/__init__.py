from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnalogCls:
	"""Analog commands group definition. 62 total commands, 6 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("analog", core, parent)

	@property
	def bias(self):
		"""bias commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_bias'):
			from .Bias import BiasCls
			self._bias = BiasCls(self._core, self._cmd_group)
		return self._bias

	@property
	def envelope(self):
		"""envelope commands group. 7 Sub-classes, 12 commands."""
		if not hasattr(self, '_envelope'):
			from .Envelope import EnvelopeCls
			self._envelope = EnvelopeCls(self._core, self._cmd_group)
		return self._envelope

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def ppsMarker(self):
		"""ppsMarker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ppsMarker'):
			from .PpsMarker import PpsMarkerCls
			self._ppsMarker = PpsMarkerCls(self._core, self._cmd_group)
		return self._ppsMarker

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:ANALog:STATe \n
		Snippet: value: bool = driver.source.iq.output.analog.get_state() \n
		Activates the specified analog I/Q output. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + OUTPut<hw>:STATe or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:ANALog:STATe \n
		Snippet: driver.source.iq.output.analog.set_state(state = False) \n
		Activates the specified analog I/Q output. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + OUTPut<hw>:STATe or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:STATe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.IqOutMode:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Snippet: value: enums.IqOutMode = driver.source.iq.output.analog.get_mode() \n
		Determines the mode for setting the output parameters. \n
			:return: mode: FIXed| VARiable | VATTenuated FIXed Locks the I/Q output settings VARiable Unlocks the settings VATTenuated Attenuates the signal with the value set with the command [:SOURcehw]:IQ:OUTPut:[ANALog]:POWer:ATTDigital.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutMode)

	def set_mode(self, mode: enums.IqOutMode) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Snippet: driver.source.iq.output.analog.set_mode(mode = enums.IqOutMode.FIXed) \n
		Determines the mode for setting the output parameters. \n
			:param mode: FIXed| VARiable | VATTenuated FIXed Locks the I/Q output settings VARiable Unlocks the settings VATTenuated Attenuates the signal with the value set with the command [:SOURcehw]:IQ:OUTPut:[ANALog]:POWer:ATTDigital.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.IqOutMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Snippet: driver.source.iq.output.analog.preset() \n
		Sets the default settings (*RST values specified for the commands) .
			INTRO_CMD_HELP: Not affected are: \n
			- The state set with the command [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe.
			- If SCONfiguration:EXTernal:PBEHaviour 1, the I/Q ouptput type set with the command [:SOURce<hw>]:IQ:OUTPut[:ANALog]:TYPE. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Snippet: driver.source.iq.output.analog.preset_with_opc() \n
		Sets the default settings (*RST values specified for the commands) .
			INTRO_CMD_HELP: Not affected are: \n
			- The state set with the command [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe.
			- If SCONfiguration:EXTernal:PBEHaviour 1, the I/Q ouptput type set with the command [:SOURce<hw>]:IQ:OUTPut[:ANALog]:TYPE. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.IqOutType:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Snippet: value: enums.IqOutType = driver.source.iq.output.analog.get_type_py() \n
		Sets the type of the analog signal. \n
			:return: type_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutType)

	def set_type_py(self, type_py: enums.IqOutType) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Snippet: driver.source.iq.output.analog.set_type_py(type_py = enums.IqOutType.DAC) \n
		Sets the type of the analog signal. \n
			:param type_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.IqOutType)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE {param}')

	def clone(self) -> 'AnalogCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AnalogCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
