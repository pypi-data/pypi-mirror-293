from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LastCls:
	"""Last commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("last", core, parent)

	def get_fe(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:LAST:FE \n
		Snippet: value: int = driver.source.areGenerator.frontend.last.get_fe() \n
		Queries the last added QAT-type, FE-type or custom frontend. Displays the number included in the frontend ID, e.g.
		'3' for QAT-type frontend ID Q3. \n
			:return: last_added_fe: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:FRONtend:LAST:FE?')
		return Conversions.str_to_int(response)

	def get_qat(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:LAST:QAT \n
		Snippet: value: int = driver.source.areGenerator.frontend.last.get_qat() \n
		Queries the last added QAT-type, FE-type or custom frontend. Displays the number included in the frontend ID, e.g.
		'3' for QAT-type frontend ID Q3. \n
			:return: areg_fe_last_add_qa: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:FRONtend:LAST:QAT?')
		return Conversions.str_to_int(response)
