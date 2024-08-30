from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RateCls:
	"""Rate commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rate", core, parent)

	def get_max(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DTMB:USEFul:[RATE]:MAX \n
		Snippet: value: int = driver.source.bb.dtmb.useful.rate.get_max() \n
		Queries the maximum data rate, that is derived from the current modulation parameter settings. The value is the optimal
		value at the TS input interface, that is necessary for the modulator. \n
			:return: dtmb_max_use: integer Range: 0 to 999999999
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DTMB:USEFul:RATE:MAX?')
		return Conversions.str_to_int(response)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:DTMB:USEFul:[RATE] \n
		Snippet: value: float = driver.source.bb.dtmb.useful.rate.get_value() \n
		Queries the data rate of useful data ruseful of the external transport stream. The data rate is measured at the input of
		the installed input interface. \n
			:return: dtmb_useful: float Range: 0 to 999999999
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DTMB:USEFul:RATE?')
		return Conversions.str_to_float(response)
