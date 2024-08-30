from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmeCls:
	"""Dme commands group definition. 6 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dme", core, parent)

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def gaussian(self):
		"""gaussian commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gaussian'):
			from .Gaussian import GaussianCls
			self._gaussian = GaussianCls(self._core, self._cmd_group)
		return self._gaussian

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:PRESet \n
		Snippet: driver.source.bb.dme.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:PRESet \n
		Snippet: driver.source.bb.dme.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DME:STATe \n
		Snippet: value: bool = driver.source.bb.dme.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:STATe \n
		Snippet: driver.source.bb.dme.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:STATe {param}')

	def clone(self) -> 'DmeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
