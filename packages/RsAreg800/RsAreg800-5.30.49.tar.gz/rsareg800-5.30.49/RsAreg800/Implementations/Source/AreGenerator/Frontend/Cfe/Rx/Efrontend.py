from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EfrontendCls:
	"""Efrontend commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("efrontend", core, parent)

	def set(self, instr_name: str, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:RX<ST>:EFRontend \n
		Snippet: driver.source.areGenerator.frontend.cfe.rx.efrontend.set(instr_name = 'abc', channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default) \n
		No command help available \n
			:param instr_name: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.value_to_quoted_str(instr_name)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:RX{rxIndex_cmd_val}:EFRontend {param}')

	def get(self, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:RX<ST>:EFRontend \n
		Snippet: value: str = driver.source.areGenerator.frontend.cfe.rx.efrontend.get(channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: instr_name: No help available"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:RX{rxIndex_cmd_val}:EFRontend?')
		return trim_str_response(response)
