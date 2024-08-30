from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DetectorCls:
	"""Detector commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("detector", core, parent)

	@property
	def rfLevel(self):
		"""rfLevel commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfLevel'):
			from .RfLevel import RfLevelCls
			self._rfLevel = RfLevelCls(self._core, self._cmd_group)
		return self._rfLevel

	def clone(self) -> 'DetectorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DetectorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
