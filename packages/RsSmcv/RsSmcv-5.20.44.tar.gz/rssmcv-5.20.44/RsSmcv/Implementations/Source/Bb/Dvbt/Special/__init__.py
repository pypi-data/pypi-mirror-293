from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpecialCls:
	"""Special commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("special", core, parent)

	@property
	def reedSolomon(self):
		"""reedSolomon commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_reedSolomon'):
			from .ReedSolomon import ReedSolomonCls
			self._reedSolomon = ReedSolomonCls(self._core, self._cmd_group)
		return self._reedSolomon

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	def clone(self) -> 'SpecialCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpecialCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
