from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PeriodCls:
	"""Period commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("period", core, parent)

	def set(self, alloc_rep_period: int, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:ALLoc<AL(DIR0)>:PERiod \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.alloc.period.set(alloc_rep_period = 1, cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the repetition periodicity.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select custom repetition type ([:SOURce<hw>]:BB:NR5G:SCHed:CELL<cc>:SUBF<sf>:USER<us>:BWPart<bwp>:ALLoc<al>:REPetitions) . \n
			:param alloc_rep_period: integer Range: 1 to max* *) Max repetition period is calculated as follows: RepPeriodmax = #SlotsPerFrame * 'SequnceLength', where: #SlotsPerFrame: is the number of available slots and depends on the used subcarrier spacing. 'SequenceLength': is the ARB sequence length as set with the command [:SOURcehw]:BB:NR5G:OUTPut:SEQLen.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(alloc_rep_period)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PERiod {param}')

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:ALLoc<AL(DIR0)>:PERiod \n
		Snippet: value: int = driver.source.bb.nr5G.scheduling.cell.subf.alloc.period.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the repetition periodicity.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select custom repetition type ([:SOURce<hw>]:BB:NR5G:SCHed:CELL<cc>:SUBF<sf>:USER<us>:BWPart<bwp>:ALLoc<al>:REPetitions) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: alloc_rep_period: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PERiod?')
		return Conversions.str_to_int(response)
