# vim:set noet ts=4:
#
# ibus - The Input Bus
#
# Copyright (c) 2007-2008 Huang Peng <shawn.p.huang@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import dbus.lowlevel
import ibus
import gobject

class Connection (ibus.Object):
	__gsignals__ = {
		"dbus-signal" : (
			gobject.SIGNAL_RUN_FIRST,
			gobject.TYPE_NONE,
			(gobject.TYPE_PYOBJECT, )
		)
	}
	def __init__ (self, dbusconn):
		ibus.Object.__init__ (self)
		self._dbusconn = dbusconn

	def get_object (self, path):
		return self._dbusconn.get_object ("no.name", path)

	def emit_dbus_signal (self, name, *args):
		message = dbus.lowlevel.SignalMessage (ibus.IBUS_PATH, ibus.IBUS_IFACE, name)
		message.append (*args)
		self._dbusconn.send_message (message)
		self._dbusconn.flush ()

	def do_destroy (self):
		self._dbusconn = None

	def dispatch_dbus_signal (self, message):
		self.emit ("dbus-signal", message)

gobject.type_register (Connection)