from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PilotCls:
	"""Pilot commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pilot", core, parent)

	@property
	def boost(self):
		"""boost commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boost'):
			from .Boost import BoostCls
			self._boost = BoostCls(self._core, self._cmd_group)
		return self._boost

	@property
	def siso(self):
		"""siso commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_siso'):
			from .Siso import SisoCls
			self._siso = SisoCls(self._core, self._cmd_group)
		return self._siso

	def clone(self) -> 'PilotCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PilotCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
