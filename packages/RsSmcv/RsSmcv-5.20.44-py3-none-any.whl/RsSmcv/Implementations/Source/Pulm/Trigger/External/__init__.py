from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	@property
	def gate(self):
		"""gate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gate'):
			from .Gate import GateCls
			self._gate = GateCls(self._core, self._cmd_group)
		return self._gate

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InputImpRf:
		"""SCPI: [SOURce<HW>]:PULM:TRIGger:EXTernal:IMPedance \n
		Snippet: value: enums.InputImpRf = driver.source.pulm.trigger.external.get_impedance() \n
		No command help available \n
			:return: impedance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRIGger:EXTernal:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InputImpRf)

	def set_impedance(self, impedance: enums.InputImpRf) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRIGger:EXTernal:IMPedance \n
		Snippet: driver.source.pulm.trigger.external.set_impedance(impedance = enums.InputImpRf.G10K) \n
		No command help available \n
			:param impedance: No help available
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.InputImpRf)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRIGger:EXTernal:IMPedance {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SlopeType:
		"""SCPI: [SOURce<HW>]:PULM:TRIGger:EXTernal:SLOPe \n
		Snippet: value: enums.SlopeType = driver.source.pulm.trigger.external.get_slope() \n
		No command help available \n
			:return: slope: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRIGger:EXTernal:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)

	def set_slope(self, slope: enums.SlopeType) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRIGger:EXTernal:SLOPe \n
		Snippet: driver.source.pulm.trigger.external.set_slope(slope = enums.SlopeType.NEGative) \n
		No command help available \n
			:param slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SlopeType)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRIGger:EXTernal:SLOPe {param}')

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
