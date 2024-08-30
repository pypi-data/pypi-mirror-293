from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AmplifierCls:
	"""Amplifier commands group definition. 4 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("amplifier", core, parent)

	@property
	def stage(self):
		"""stage commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_stage'):
			from .Stage import StageCls
			self._stage = StageCls(self._core, self._cmd_group)
		return self._stage

	def clone(self) -> 'AmplifierCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AmplifierCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
