import pytest
import os
import stat
import os.path as path
import shutil

from . import inventory


@pytest.fixture(scope="function")
def inventory_scripts_path(tmpdir):
    print(tmpdir)
    d = tmpdir.mkdir("inventory")
    f = d.join("script")
    f.write("#!/bin/sh\necho key=val")
    os.chmod(f, stat.S_IRWXU | stat.S_IRWXO | stat.S_IRWXG)
    return str(d)

@pytest.fixture
def inventory_script(inventory_scripts_path):
    # For now
    return inventory_scripts_path + "/script"


class TestInventory:
    def test_aggregator(self):
        pass

    def test_inventory_scripts(self, inventory_scripts_path):
        assert len(inventory.inventory_scripts(inventory_scripts_path)) == 1

    def test_InventoryScript(self, inventory_script):
        i = inventory.InventoryScript(inventory_script)
        i.run()
