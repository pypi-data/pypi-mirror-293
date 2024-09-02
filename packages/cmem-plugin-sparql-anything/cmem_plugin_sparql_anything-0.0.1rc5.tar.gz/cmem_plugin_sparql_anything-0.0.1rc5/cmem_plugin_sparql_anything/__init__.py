"""sparql-anything - main package"""

import logging

import cmem_plugin_sparql_anything.bin

try:
    if not cmem_plugin_sparql_anything.bin.has_jar():
        cmem_plugin_sparql_anything.bin.download_sparql_anything()
except Exception:  # noqa: BLE001
    logging.info("Failed to download sparql anything zip file")
