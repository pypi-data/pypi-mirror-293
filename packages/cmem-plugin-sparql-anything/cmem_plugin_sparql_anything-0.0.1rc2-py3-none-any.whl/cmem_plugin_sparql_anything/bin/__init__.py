"""Path to the sparql-anything-0.9.0.jar file."""

from pathlib import Path

from . import __path__

sparql_anything_jar_path = Path(__path__[0]) / "sparql-anything-0.9.0.jar"
