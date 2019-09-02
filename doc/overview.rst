==========
 Overview
==========

Labgridhelper is separated into different submodules. These submodules are
created for different stages of a device boot, i.e. the barebox submodules is
used for the barebox bootloader and the linux submodule is used for a fully
booted linux system.

Writing new helper functions
============================
Helper functions usually use one of the protocols from labgrid to retrive data
from the device, reformat the data and return it to be consumed in the test
case.
These functions should not perform test asserts, this should be done in the
individual test cases, to separate data reformating from testing.
Asserts however are needed to verify that the correct protocol is passed to the
helper function. This is usually done by importing the protocol from labgrid and
performing the assert in the beginning of the helper, i.e.:

::

  def get_systemd_status(command):
      assert isinstance(command, CommandProtocol), "command must be a CommandProtocol"

This should ensure that the correct protocol is used and the helper function is
used correctly in the test suite.

Helper functions should also contain a docstring to document its function for
the user, i.e.:

::

  def get_commands(command, directories=None):
      """Returns the commands of a running linux system

      Args:
          command (CommandProtocol): An instance of a Driver implementing the CommandProtocol
          directories (list): An optional list of directories to include

      Returns:
          list: list of commands available under linux
      """
