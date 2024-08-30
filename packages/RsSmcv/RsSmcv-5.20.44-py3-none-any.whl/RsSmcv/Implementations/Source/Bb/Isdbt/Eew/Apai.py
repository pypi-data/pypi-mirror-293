from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApaiCls:
	"""Apai commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apai", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ISDBt:EEW:APAI \n
		Snippet: driver.source.bb.isdbt.eew.apai.set() \n
		Issues a seismic motion warning based on the information of 'Area Information Hex'. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ISDBt:EEW:APAI')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:ISDBt:EEW:APAI \n
		Snippet: driver.source.bb.isdbt.eew.apai.set_with_opc() \n
		Issues a seismic motion warning based on the information of 'Area Information Hex'. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmcv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ISDBt:EEW:APAI', opc_timeout_ms)
