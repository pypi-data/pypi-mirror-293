from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SensorCls:
	"""Sensor commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensor", core, parent)

	@property
	def offset(self):
		"""offset commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def sfrequency(self):
		"""sfrequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfrequency'):
			from .Sfrequency import SfrequencyCls
			self._sfrequency = SfrequencyCls(self._core, self._cmd_group)
		return self._sfrequency

	def clone(self) -> 'SensorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SensorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
