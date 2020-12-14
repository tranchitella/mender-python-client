import logging as log
from src.scripts.aggregator.aggregator import ScriptKeyValueAggregator

def get(path="/etc/mender/artifact_info"):
    try:
        with open(path) as fh:
            artifact_info = ScriptKeyValueAggregator(path).collect()
            return artifact_info
    except FileNotFoundError:
        log.error(f"No artifact_info file found in {path}")
        return None
    except Exception as e:
        log.error(f"Error: {e}")
