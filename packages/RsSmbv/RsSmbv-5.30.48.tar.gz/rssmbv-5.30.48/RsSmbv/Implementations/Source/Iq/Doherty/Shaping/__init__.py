from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ShapingCls:
	"""Shaping commands group definition. 18 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("shaping", core, parent)

	@property
	def normalized(self):
		"""normalized commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_normalized'):
			from .Normalized import NormalizedCls
			self._normalized = NormalizedCls(self._core, self._cmd_group)
		return self._normalized

	@property
	def polynomial(self):
		"""polynomial commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_polynomial'):
			from .Polynomial import PolynomialCls
			self._polynomial = PolynomialCls(self._core, self._cmd_group)
		return self._polynomial

	@property
	def table(self):
		"""table commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_table'):
			from .Table import TableCls
			self._table = TableCls(self._core, self._cmd_group)
		return self._table

	def clone(self) -> 'ShapingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ShapingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
