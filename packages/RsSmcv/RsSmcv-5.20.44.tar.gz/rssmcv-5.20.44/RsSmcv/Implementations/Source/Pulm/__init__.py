from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PulmCls:
	"""Pulm commands group definition. 10 total commands, 2 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pulm", core, parent)

	@property
	def double(self):
		"""double commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_double'):
			from .Double import DoubleCls
			self._double = DoubleCls(self._core, self._cmd_group)
		return self._double

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:DELay \n
		Snippet: value: float = driver.source.pulm.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:DELay \n
		Snippet: driver.source.pulm.set_delay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:PULM:DELay {param}')

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.NormalInverted:
		"""SCPI: [SOURce<HW>]:PULM:POLarity \n
		Snippet: value: enums.NormalInverted = driver.source.pulm.get_polarity() \n
		No command help available \n
			:return: polarity: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormalInverted)

	def set_polarity(self, polarity: enums.NormalInverted) -> None:
		"""SCPI: [SOURce<HW>]:PULM:POLarity \n
		Snippet: driver.source.pulm.set_polarity(polarity = enums.NormalInverted.INVerted) \n
		No command help available \n
			:param polarity: No help available
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormalInverted)
		self._core.io.write(f'SOURce<HwInstance>:PULM:POLarity {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.PulseSoure:
		"""SCPI: [SOURce<HW>]:PULM:SOURce \n
		Snippet: value: enums.PulseSoure = driver.source.pulm.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.PulseSoure)

	def set_source(self, source: enums.PulseSoure) -> None:
		"""SCPI: [SOURce<HW>]:PULM:SOURce \n
		Snippet: driver.source.pulm.set_source(source = enums.PulseSoure.CODer) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.PulseSoure)
		self._core.io.write(f'SOURce<HwInstance>:PULM:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:PULM:STATe \n
		Snippet: value: bool = driver.source.pulm.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:PULM:STATe \n
		Snippet: driver.source.pulm.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:PULM:STATe {param}')

	def clone(self) -> 'PulmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PulmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
