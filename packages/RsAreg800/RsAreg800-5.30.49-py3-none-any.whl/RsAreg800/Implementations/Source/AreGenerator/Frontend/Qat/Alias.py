from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AliasCls:
	"""Alias commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alias", core, parent)

	def set(self, areg_fe_alias: str, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ALIas \n
		Snippet: driver.source.areGenerator.frontend.qat.alias.set(areg_fe_alias = 'abc', qatFrontent = repcap.QatFrontent.Default) \n
		Sets the alias of the frontend. \n
			:param areg_fe_alias: No help available
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		param = Conversions.value_to_quoted_str(areg_fe_alias)
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ALIas {param}')

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ALIas \n
		Snippet: value: str = driver.source.areGenerator.frontend.qat.alias.get(qatFrontent = repcap.QatFrontent.Default) \n
		Sets the alias of the frontend. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_alias: No help available"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ALIas?')
		return trim_str_response(response)
