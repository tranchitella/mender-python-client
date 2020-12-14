# Copyright 2020 Northern.tech AS
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
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
