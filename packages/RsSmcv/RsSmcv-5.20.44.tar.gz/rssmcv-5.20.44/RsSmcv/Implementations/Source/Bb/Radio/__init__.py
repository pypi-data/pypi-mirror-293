from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RadioCls:
	"""Radio commands group definition. 183 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("radio", core, parent)

	@property
	def am(self):
		"""am commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_am'):
			from .Am import AmCls
			self._am = AmCls(self._core, self._cmd_group)
		return self._am

	@property
	def fm(self):
		"""fm commands group. 8 Sub-classes, 4 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import FmCls
			self._fm = FmCls(self._core, self._cmd_group)
		return self._fm

	def clone(self) -> 'RadioCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RadioCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
