"""
LaundryBot V7 Enterprise
Create Upload Folder
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config

folders = [

    Config.UPLOAD_FOLDER,

    Config.MACHINE_IMAGE_FOLDER,

    Config.MANUAL_UPLOAD_FOLDER,

    Config.PART_UPLOAD_FOLDER,

]

for folder in folders:

    folder.mkdir(

        parents=True,

        exist_ok=True,

    )

    print("OK :", folder)

print("=" * 60)
print("Upload folders created.")
print("=" * 60)