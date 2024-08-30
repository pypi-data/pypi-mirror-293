from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LayerCls:
	"""Layer commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("layer", core, parent)

	# noinspection PyTypeChecker
	def get(self, physicalLayerPipe=repcap.PhysicalLayerPipe.Default) -> enums.Atsc30Layer:
		"""SCPI: [SOURce<HW>]:BB:A3TSc:PLP<CH>:LAYer:LAYer \n
		Snippet: value: enums.Atsc30Layer = driver.source.bb.a3Tsc.plp.layer.layer.get(physicalLayerPipe = repcap.PhysicalLayerPipe.Default) \n
		Queries the layer, that is used in . \n
			:param physicalLayerPipe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Plp')
			:return: layer: ENHanced| CORE"""
		physicalLayerPipe_cmd_val = self._cmd_group.get_repcap_cmd_value(physicalLayerPipe, repcap.PhysicalLayerPipe)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:A3TSc:PLP{physicalLayerPipe_cmd_val}:LAYer:LAYer?')
		return Conversions.str_to_scalar_enum(response, enums.Atsc30Layer)
