"""
LaundryBot V5

Part Service
"""

from repositories.part_repository import search_parts
from database.db import connect


# ==========================================================
# Get All Parts
# ==========================================================

def get_all_parts(limit=1000):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        model,
        part_no,
        description,
        page
    FROM parts
    ORDER BY model, part_no
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# Get Part Detail
# ==========================================================

def get_part(part_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM parts
    WHERE id=?
    """, (part_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ==========================================================
# Search Part
# ==========================================================

def search_part(keyword, model=""):

    return search_parts(
        keyword=keyword,
        model=model,
    )