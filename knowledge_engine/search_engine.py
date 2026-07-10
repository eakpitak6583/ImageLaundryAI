"""
LaundryBot V5

Knowledge Search Engine

หน้าที่
--------

รวบรวมข้อมูลจาก Search Layer
เพื่อส่งต่อเข้า AI Pipeline
"""

from search.search_engine import (
    search_parts,
    search_manual,
    search_repair,
)


def search_knowledge(
    model: str,
    keyword: str,
):

    knowledge = {

        "parts": [],

        "manual": [],

        "repair": [],

    }

    # ----------------------------------------
    # Parts
    # ----------------------------------------

    try:

        knowledge["parts"] = search_parts(

            model=model,

            question=keyword,

        )

    except Exception as e:

        print()

        print("=" * 60)

        print("SEARCH PART ERROR")

        print(e)

        print("=" * 60)

    # ----------------------------------------
    # Manual
    # ----------------------------------------

    try:

        knowledge["manual"] = search_manual(

            model=model,

            question=keyword,

        )

    except Exception as e:

        print()

        print("=" * 60)

        print("SEARCH MANUAL ERROR")

        print(e)

        print("=" * 60)

    # ----------------------------------------
    # Repair
    # ----------------------------------------

    try:

        knowledge["repair"] = search_repair(

            model=model,

            question=keyword,

        )

    except Exception as e:

        print()

        print("=" * 60)

        print("SEARCH REPAIR ERROR")

        print(e)

        print("=" * 60)

    print()

    print("=" * 60)

    print("KNOWLEDGE SEARCH")

    print("MODEL :", model)

    print("KEYWORD :", keyword)

    print("PARTS :", len(knowledge["parts"]))

    print("MANUAL :", len(knowledge["manual"]))

    print("REPAIR :", len(knowledge["repair"]))

    print("=" * 60)

    return knowledge