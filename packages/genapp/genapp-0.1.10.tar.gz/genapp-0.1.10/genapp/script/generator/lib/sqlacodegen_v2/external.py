from __future__ import annotations

import os
import sys
from contextlib import ExitStack
from typing import List, Optional, TextIO

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from genapp.script.generator.lib.sqlacodegen_v2.generators import DeclarativeGenerator

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points, version
else:
    from importlib.metadata import entry_points, version


def generate_models(
    engine,
    options: Optional[dict] = None,
    path: Optional[str] = None,
    file_name: Optional[str] = None,
):

    metadata = MetaData()

    generator = DeclarativeGenerator(
        metadata, engine, options if options else {})
    tables = None
    schemas = [None]
    for schema in schemas:
        metadata.reflect(engine, schema, False, tables)

    # Open the target file (if given)
    with ExitStack() as stack:
        outfile: TextIO
        if path:
            outfile = open(path + "\\" + file_name +
                           ".py", "w", encoding="utf-8")
            stack.enter_context(outfile)
        else:
            outfile = sys.stdout
        # Write the generated model code to the specified file or standard output
        outfile.write(generator.generate())
