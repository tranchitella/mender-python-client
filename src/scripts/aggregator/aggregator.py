import logging as log
import os
import subprocess

class ScriptKeyValueAggregator(object):
    """Handles the parsing of the output from any Mender identity of inventory scripts.

    These scripts support key=value pairs, with one output per line maximum.
    Multiple lines with a matching key are aggregated into an array."""

    def __init__(self, script_path):
        self.script_path = script_path
        self.vals = {}

    def run(self):
        output = subprocess.run(self.script_path, stdout=subprocess.PIPE, timeout=100)
        ss = output.stdout.decode()
        for line in ss.split("\n"):
            if line == "":
                continue
            arr = line.strip().split("=")
            if len(arr) < 2:
                log.debug(f"Skipping line without output")
                continue
            if len(arr) > 2:
                log.error(f"script: {script_path} output line: {line} is improperly formatted with more than one '=' sign. Skipping.")
                continue
            key, val = arr[0], arr[1]
            l = self.vals.get(key, [])
            l.append(val)
            self.vals[key] = l
        return self.vals
