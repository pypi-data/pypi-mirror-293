from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePyCls:
	"""TypePy commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	@property
	def nsubSlices(self):
		"""nsubSlices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsubSlices'):
			from .NsubSlices import NsubSlicesCls
			self._nsubSlices = NsubSlicesCls(self._core, self._cmd_group)
		return self._nsubSlices

	@property
	def subslice(self):
		"""subslice commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_subslice'):
			from .Subslice import SubsliceCls
			self._subslice = SubsliceCls(self._core, self._cmd_group)
		return self._subslice

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'TypePyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TypePyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
