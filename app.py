"""Run the bundled BizPilot source on Streamlit Community Cloud."""
from pathlib import Path
import runpy
import sys
from tempfile import mkdtemp
from zipfile import ZipFile

import streamlit as st


@st.cache_resource(show_spinner=False)
def unpack_source(archive_path):
    root = Path(mkdtemp(prefix="bizpilot-"))
    with ZipFile(archive_path) as archive:
        archive.extractall(root)
    sys.path.insert(0, str(root))
    return root


bundle = Path(__file__).with_name("bizpilot_source.zip")
source = unpack_source(bundle)
runpy.run_path(str(source / "app.py"), run_name="__main__")
