from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfeCls:
	"""Cfe commands group definition. 10 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfe", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Add import AddCls
			self._add = AddCls(self._core, self._cmd_group)
		return self._add

	@property
	def alias(self):
		"""alias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alias'):
			from .Alias import AliasCls
			self._alias = AliasCls(self._core, self._cmd_group)
		return self._alias

	@property
	def ats(self):
		"""ats commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ats'):
			from .Ats import AtsCls
			self._ats = AtsCls(self._core, self._cmd_group)
		return self._ats

	@property
	def rmv(self):
		"""rmv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmv'):
			from .Rmv import RmvCls
			self._rmv = RmvCls(self._core, self._cmd_group)
		return self._rmv

	@property
	def rts(self):
		"""rts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rts'):
			from .Rts import RtsCls
			self._rts = RtsCls(self._core, self._cmd_group)
		return self._rts

	@property
	def rx(self):
		"""rx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rx'):
			from .Rx import RxCls
			self._rx = RxCls(self._core, self._cmd_group)
		return self._rx

	@property
	def tx(self):
		"""tx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tx'):
			from .Tx import TxCls
			self._tx = TxCls(self._core, self._cmd_group)
		return self._tx

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'CfeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CfeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
