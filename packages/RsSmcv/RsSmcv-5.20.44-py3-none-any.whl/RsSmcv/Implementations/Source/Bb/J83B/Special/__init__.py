from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpecialCls:
	"""Special commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("special", core, parent)

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	def get_reed_solomon(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:J83B:[SPECial]:REEDsolomon \n
		Snippet: value: bool = driver.source.bb.j83B.special.get_reed_solomon() \n
		Enables/disables the Reed-Solomon encoder. \n
			:return: reed_solomon: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:J83B:SPECial:REEDsolomon?')
		return Conversions.str_to_bool(response)

	def set_reed_solomon(self, reed_solomon: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:J83B:[SPECial]:REEDsolomon \n
		Snippet: driver.source.bb.j83B.special.set_reed_solomon(reed_solomon = False) \n
		Enables/disables the Reed-Solomon encoder. \n
			:param reed_solomon: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(reed_solomon)
		self._core.io.write(f'SOURce<HwInstance>:BB:J83B:SPECial:REEDsolomon {param}')

	def clone(self) -> 'SpecialCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpecialCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
