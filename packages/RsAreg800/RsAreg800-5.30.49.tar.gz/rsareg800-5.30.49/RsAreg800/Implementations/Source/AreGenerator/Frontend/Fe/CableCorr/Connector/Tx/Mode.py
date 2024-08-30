from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, areg_cabel_cor_mod: enums.AregCableCorrSour, channel=repcap.Channel.Default, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:CABLecorr:CONNector<DI>:TX<ST0>:MODE \n
		Snippet: driver.source.areGenerator.frontend.fe.cableCorr.connector.tx.mode.set(areg_cabel_cor_mod = enums.AregCableCorrSour.FACTory, channel = repcap.Channel.Default, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Selects the source for cable correction data. \n
			:param areg_cabel_cor_mod:
				- USER: Selects user-defined cable correction data, i.e. fixed values for delay and attenuation.
				- S2P: Selects cable correction data from a file with file extension *.s2p.
				- FACTory: For TRX-type frontends only.Selects cable correction data for the TRX frontend from factory specification.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')"""
		param = Conversions.enum_scalar_to_str(areg_cabel_cor_mod, enums.AregCableCorrSour)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> enums.AregCableCorrSour:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:CABLecorr:CONNector<DI>:TX<ST0>:MODE \n
		Snippet: value: enums.AregCableCorrSour = driver.source.areGenerator.frontend.fe.cableCorr.connector.tx.mode.get(channel = repcap.Channel.Default, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Selects the source for cable correction data. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: areg_cabel_cor_mod:
				- USER: Selects user-defined cable correction data, i.e. fixed values for delay and attenuation.
				- S2P: Selects cable correction data from a file with file extension *.s2p.
				- FACTory: For TRX-type frontends only.Selects cable correction data for the TRX frontend from factory specification."""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AregCableCorrSour)
