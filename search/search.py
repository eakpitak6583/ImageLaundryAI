from search.search_engine import (
    search_parts,
    search_manual,
    search_repair,
)


def search_everything(model, keyword):
    return {
        "parts": search_parts(model, keyword),
        "manual": search_manual(model, keyword),
        "repair": search_repair(model, keyword),
    }