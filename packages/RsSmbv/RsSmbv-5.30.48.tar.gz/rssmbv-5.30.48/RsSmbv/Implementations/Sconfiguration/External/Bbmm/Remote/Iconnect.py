from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IconnectCls:
	"""Iconnect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iconnect", core, parent)

	def set(self, instr_name: str, rf_path: str, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:REMote:ICONnect \n
		Snippet: driver.sconfiguration.external.bbmm.remote.iconnect.set(instr_name = 'abc', rf_path = 'abc', iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param instr_name: No help available
			:param rf_path: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('instr_name', instr_name, DataType.String), ArgSingle('rf_path', rf_path, DataType.String))
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:REMote:ICONnect {param}'.rstrip())
