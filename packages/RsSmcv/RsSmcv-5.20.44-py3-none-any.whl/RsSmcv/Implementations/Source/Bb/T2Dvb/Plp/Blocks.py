from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BlocksCls:
	"""Blocks commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("blocks", core, parent)

	def get(self, physicalLayerPipe=repcap.PhysicalLayerPipe.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:T2DVb:PLP<CH>:BLOCks \n
		Snippet: value: int = driver.source.bb.t2Dvb.plp.blocks.get(physicalLayerPipe = repcap.PhysicalLayerPipe.Default) \n
		Queries the number of FEC blocks per interleaving frame. \n
			:param physicalLayerPipe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Plp')
			:return: fec_blocks: integer Range: 0 to 1023"""
		physicalLayerPipe_cmd_val = self._cmd_group.get_repcap_cmd_value(physicalLayerPipe, repcap.PhysicalLayerPipe)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:T2DVb:PLP{physicalLayerPipe_cmd_val}:BLOCks?')
		return Conversions.str_to_int(response)
