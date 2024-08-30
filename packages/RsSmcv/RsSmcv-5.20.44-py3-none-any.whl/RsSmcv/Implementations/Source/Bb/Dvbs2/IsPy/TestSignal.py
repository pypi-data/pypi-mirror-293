from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TestSignalCls:
	"""TestSignal commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("testSignal", core, parent)

	def set(self, test_signal: enums.Dvbs2InputSignalTestSignal, inputStream=repcap.InputStream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBS2:[IS<CH>]:TESTsignal \n
		Snippet: driver.source.bb.dvbs2.isPy.testSignal.set(test_signal = enums.Dvbs2InputSignalTestSignal.TGSP, inputStream = repcap.InputStream.Default) \n
		Defines the test signal data. \n
			:param test_signal: TTSP| TGSP TTSP Test TS packet with standardized packet data used as modulation data in the transport stream. TGSP Test GS packet with predefined packet data used as modulation data in the generic stream.
			:param inputStream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IsPy')
		"""
		param = Conversions.enum_scalar_to_str(test_signal, enums.Dvbs2InputSignalTestSignal)
		inputStream_cmd_val = self._cmd_group.get_repcap_cmd_value(inputStream, repcap.InputStream)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBS2:IS{inputStream_cmd_val}:TESTsignal {param}')

	# noinspection PyTypeChecker
	def get(self, inputStream=repcap.InputStream.Default) -> enums.Dvbs2InputSignalTestSignal:
		"""SCPI: [SOURce<HW>]:BB:DVBS2:[IS<CH>]:TESTsignal \n
		Snippet: value: enums.Dvbs2InputSignalTestSignal = driver.source.bb.dvbs2.isPy.testSignal.get(inputStream = repcap.InputStream.Default) \n
		Defines the test signal data. \n
			:param inputStream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IsPy')
			:return: test_signal: TTSP| TGSP TTSP Test TS packet with standardized packet data used as modulation data in the transport stream. TGSP Test GS packet with predefined packet data used as modulation data in the generic stream."""
		inputStream_cmd_val = self._cmd_group.get_repcap_cmd_value(inputStream, repcap.InputStream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVBS2:IS{inputStream_cmd_val}:TESTsignal?')
		return Conversions.str_to_scalar_enum(response, enums.Dvbs2InputSignalTestSignal)
