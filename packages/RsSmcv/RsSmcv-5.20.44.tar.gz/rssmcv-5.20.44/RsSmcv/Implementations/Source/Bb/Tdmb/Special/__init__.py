from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpecialCls:
	"""Special commands group definition. 5 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("special", core, parent)

	@property
	def settings(self):
		"""settings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_settings'):
			from .Settings import SettingsCls
			self._settings = SettingsCls(self._core, self._cmd_group)
		return self._settings

	@property
	def testSignal(self):
		"""testSignal commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_testSignal'):
			from .TestSignal import TestSignalCls
			self._testSignal = TestSignalCls(self._core, self._cmd_group)
		return self._testSignal

	@property
	def transmission(self):
		"""transmission commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_transmission'):
			from .Transmission import TransmissionCls
			self._transmission = TransmissionCls(self._core, self._cmd_group)
		return self._transmission

	def clone(self) -> 'SpecialCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpecialCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
