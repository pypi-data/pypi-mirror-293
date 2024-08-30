from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	# noinspection PyTypeChecker
	def get_coupling(self) -> enums.AcDc:
		"""SCPI: [SOURce<HW>]:FM:EXTernal:COUPling \n
		Snippet: value: enums.AcDc = driver.source.fm.external.get_coupling() \n
		No command help available \n
			:return: coupling: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:EXTernal:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.AcDc)

	def set_coupling(self, coupling: enums.AcDc) -> None:
		"""SCPI: [SOURce<HW>]:FM:EXTernal:COUPling \n
		Snippet: driver.source.fm.external.set_coupling(coupling = enums.AcDc.AC) \n
		No command help available \n
			:param coupling: No help available
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.AcDc)
		self._core.io.write(f'SOURce<HwInstance>:FM:EXTernal:COUPling {param}')

	def get_deviation(self) -> float:
		"""SCPI: [SOURce<HW>]:FM:EXTernal:DEViation \n
		Snippet: value: float = driver.source.fm.external.get_deviation() \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:EXTernal:DEViation?')
		return Conversions.str_to_float(response)

	def set_deviation(self, deviation: float) -> None:
		"""SCPI: [SOURce<HW>]:FM:EXTernal:DEViation \n
		Snippet: driver.source.fm.external.set_deviation(deviation = 1.0) \n
		No command help available \n
			:param deviation: No help available
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:FM:EXTernal:DEViation {param}')
