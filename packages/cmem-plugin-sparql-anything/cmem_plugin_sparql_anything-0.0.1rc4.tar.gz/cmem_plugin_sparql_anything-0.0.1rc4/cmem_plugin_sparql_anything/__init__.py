"""sparql-anything - main package"""

import cmem_plugin_sparql_anything.bin

# Checks if SPARQL Anything is not installed. Installs it if so.
if not cmem_plugin_sparql_anything.bin.has_jar():  # SPARQL Anything not installed.
    cmem_plugin_sparql_anything.bin.download_sparql_anything()
