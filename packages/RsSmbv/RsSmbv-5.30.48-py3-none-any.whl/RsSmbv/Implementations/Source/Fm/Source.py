from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source: enums.AmFmSource, generatorIx=repcap.GeneratorIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:FM<CH>:SOURce \n
		Snippet: driver.source.fm.source.set(source = enums.AmFmSource.EXT1, generatorIx = repcap.GeneratorIx.Default) \n
		Selects the modulation source for frequency modulation. \n
			:param source: EXT1| NOISe| LF2| LF1| INTernal| EXTernal LF1|LF2 Uses an internally generated LF signal. INTernal Uses the internally generated signal of LF1. EXTernal Uses an external LF signal (EXT1) . NOISe Uses the internally generated noise signal.
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fm')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.AmFmSource)
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		self._core.io.write(f'SOURce<HwInstance>:FM{generatorIx_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, generatorIx=repcap.GeneratorIx.Default) -> enums.AmFmSource:
		"""SCPI: [SOURce<HW>]:FM<CH>:SOURce \n
		Snippet: value: enums.AmFmSource = driver.source.fm.source.get(generatorIx = repcap.GeneratorIx.Default) \n
		Selects the modulation source for frequency modulation. \n
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fm')
			:return: source: EXT1| NOISe| LF2| LF1| INTernal| EXTernal LF1|LF2 Uses an internally generated LF signal. INTernal Uses the internally generated signal of LF1. EXTernal Uses an external LF signal (EXT1) . NOISe Uses the internally generated noise signal."""
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FM{generatorIx_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AmFmSource)
