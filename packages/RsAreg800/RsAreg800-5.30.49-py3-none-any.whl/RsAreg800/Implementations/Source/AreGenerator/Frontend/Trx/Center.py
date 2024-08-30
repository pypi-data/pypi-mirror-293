from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CenterCls:
	"""Center commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("center", core, parent)

	def set(self, areg_fe_center_fre: float, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:CENTer \n
		Snippet: driver.source.areGenerator.frontend.trx.center.set(areg_fe_center_fre = 1.0, trxFrontent = repcap.TrxFrontent.Default) \n
		Sets the RF center frequency of the output signal of the connected frontend. The frontend center frequency and frequency
		range depend on the configuration of the R&S AREG800A and the configuration of the frontend included in the test setup.
		For more information, see the data sheet. When using custom frontends, the IF center frequency instead of the RF center
		frequency is configurable in the frontend configuration. The IF center frequency with the sensor bandwidth is used for
		the cable correction, whereas the sensor frequency and bandwidth is used for the antenna correction. \n
			:param areg_fe_center_fre: No help available
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_center_fre)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:CENTer {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:CENTer \n
		Snippet: value: float = driver.source.areGenerator.frontend.trx.center.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Sets the RF center frequency of the output signal of the connected frontend. The frontend center frequency and frequency
		range depend on the configuration of the R&S AREG800A and the configuration of the frontend included in the test setup.
		For more information, see the data sheet. When using custom frontends, the IF center frequency instead of the RF center
		frequency is configurable in the frontend configuration. The IF center frequency with the sensor bandwidth is used for
		the cable correction, whereas the sensor frequency and bandwidth is used for the antenna correction. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_center_fre: No help available"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:CENTer?')
		return Conversions.str_to_float(response)
