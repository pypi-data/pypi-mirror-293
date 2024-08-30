from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TsGenCls:
	"""TsGen commands group definition. 21 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsGen", core, parent)

	@property
	def configure(self):
		"""configure commands group. 3 Sub-classes, 10 commands."""
		if not hasattr(self, '_configure'):
			from .Configure import ConfigureCls
			self._configure = ConfigureCls(self._core, self._cmd_group)
		return self._configure

	@property
	def read(self):
		"""read commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_read'):
			from .Read import ReadCls
			self._read = ReadCls(self._core, self._cmd_group)
		return self._read

	def clone(self) -> 'TsGenCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TsGenCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
