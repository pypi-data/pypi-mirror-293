from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PepCls:
	"""Pep commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pep", core, parent)

	def set(self, bbout_pep_hs: float, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:CHANnel<ST0>:POWer:PEP \n
		Snippet: driver.source.iq.output.digital.channel.power.pep.set(bbout_pep_hs = 1.0, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param bbout_pep_hs: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
		"""
		param = Conversions.decimal_value_to_str(bbout_pep_hs)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:CHANnel{channelNull_cmd_val}:POWer:PEP {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> float:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:CHANnel<ST0>:POWer:PEP \n
		Snippet: value: float = driver.source.iq.output.digital.channel.power.pep.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: bbout_pep_hs: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:CHANnel{channelNull_cmd_val}:POWer:PEP?')
		return Conversions.str_to_float(response)
