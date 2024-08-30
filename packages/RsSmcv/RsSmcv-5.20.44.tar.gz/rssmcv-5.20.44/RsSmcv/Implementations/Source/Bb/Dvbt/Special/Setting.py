from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVBT:[SPECial]:SETTing:[STATe] \n
		Snippet: value: bool = driver.source.bb.dvbt.special.setting.get_state() \n
		Enables/disables special settings. The setting allows you to switch between standard-compliant and user-defined channel
		coding. \n
			:return: settings: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:SPECial:SETTing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, settings: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:[SPECial]:SETTing:[STATe] \n
		Snippet: driver.source.bb.dvbt.special.setting.set_state(settings = False) \n
		Enables/disables special settings. The setting allows you to switch between standard-compliant and user-defined channel
		coding. \n
			:param settings: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(settings)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:SPECial:SETTing:STATe {param}')
