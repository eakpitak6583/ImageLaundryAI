"""
LaundryBot V7 Enterprise
Routes Package
"""

from .dashboard import dashboard_bp
from .machine import machine_bp
from .repair import repair_bp
from .manual import manual_bp
from .auth import auth_bp
from .customer import customer_bp
from .technician import technician_bp
from .part import part_bp
from .api import api_bp
from .ai import ai_bp
from .documents import documents_bp


__all__ = [

    "dashboard_bp",
    "machine_bp",
    "repair_bp",
    "manual_bp",
    "auth_bp",
    "customer_bp",
    "technician_bp",
    "part_bp",
    "api_bp",
    "ai_bp",
    "documents_bp",

]