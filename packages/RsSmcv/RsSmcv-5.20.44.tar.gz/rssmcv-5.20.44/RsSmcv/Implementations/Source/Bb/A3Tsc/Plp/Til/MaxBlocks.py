from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaxBlocksCls:
	"""MaxBlocks commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maxBlocks", core, parent)

	def get(self, physicalLayerPipe=repcap.PhysicalLayerPipe.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:A3TSc:PLP<CH>:TIL:MAXBlocks \n
		Snippet: value: int = driver.source.bb.a3Tsc.plp.til.maxBlocks.get(physicalLayerPipe = repcap.PhysicalLayerPipe.Default) \n
		Queries the maximum number of blocks per interleaving frame. \n
			:param physicalLayerPipe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Plp')
			:return: fec_blocks_max: integer Range: 1 to 4096"""
		physicalLayerPipe_cmd_val = self._cmd_group.get_repcap_cmd_value(physicalLayerPipe, repcap.PhysicalLayerPipe)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:A3TSc:PLP{physicalLayerPipe_cmd_val}:TIL:MAXBlocks?')
		return Conversions.str_to_int(response)
