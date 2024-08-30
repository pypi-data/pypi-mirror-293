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

	def set(self, areg_cabel_cor_mod: enums.AregCableCorrSour, trxFrontent=repcap.TrxFrontent.Default, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:CABLecorr:CONNector<DI>:RX<ST>:MODE \n
		Snippet: driver.source.areGenerator.frontend.trx.cableCorr.connector.rx.mode.set(areg_cabel_cor_mod = enums.AregCableCorrSour.FACTory, trxFrontent = repcap.TrxFrontent.Default, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Selects the source for cable correction data. \n
			:param areg_cabel_cor_mod:
				- USER: Selects user-defined cable correction data, i.e. fixed values for delay and attenuation.
				- S2P: Selects cable correction data from a file with file extension *.s2p.
				- FACTory: For TRX-type frontends only.Selects cable correction data for the TRX frontend from factory specification.
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')"""
		param = Conversions.enum_scalar_to_str(areg_cabel_cor_mod, enums.AregCableCorrSour)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, trxFrontent=repcap.TrxFrontent.Default, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> enums.AregCableCorrSour:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:CABLecorr:CONNector<DI>:RX<ST>:MODE \n
		Snippet: value: enums.AregCableCorrSour = driver.source.areGenerator.frontend.trx.cableCorr.connector.rx.mode.get(trxFrontent = repcap.TrxFrontent.Default, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Selects the source for cable correction data. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_cabel_cor_mod:
				- USER: Selects user-defined cable correction data, i.e. fixed values for delay and attenuation.
				- S2P: Selects cable correction data from a file with file extension *.s2p.
				- FACTory: For TRX-type frontends only.Selects cable correction data for the TRX frontend from factory specification."""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AregCableCorrSour)
