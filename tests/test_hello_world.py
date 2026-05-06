"""Tests for the hello_world module.

Test 1:
Interface called:
i_hello_world_greet()

Saved name:
None

Expected output:
Hello World

Test 2:
Interface called:
i_hello_world_name_set("Mark")
i_hello_world_greet()

Saved name:
Mark

Expected output:
Hello Mark
"""

from importlib import reload

import ai_hello.hello_world.hello_world as hello_world_module


def test_i_hello_world_greet_outputs_hello_world_when_name_is_not_set(capsys) -> None:
    """Test default greeting when no name was saved."""
    reload(hello_world_module)

    hello_world_module.i_hello_world_greet()

    captured = capsys.readouterr()

    assert captured.out == "Hello World\n"


def test_i_hello_world_greet_outputs_hello_mark_when_name_is_set(capsys) -> None:
    """Test greeting after name was saved."""
    reload(hello_world_module)

    hello_world_module.i_hello_world_name_set("Mark")
    hello_world_module.i_hello_world_greet()

    captured = capsys.readouterr()

    assert captured.out == "Hello Mark\n"
