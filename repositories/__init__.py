from .machine_repository import MachineRepository
from .repair_repository import RepairRepository
from .user_repository import UserRepository
from .customer_repository import CustomerRepository
from .technician_repository import TechnicianRepository
from .document_repository import DocumentRepository
from .part_repository import PartRepository
from .manual_repository import ManualRepository
from .machine_instance_repository import MachineInstanceRepository
from .dashboard_repository import DashboardRepository

machine_repository = MachineRepository()
repair_repository = RepairRepository()
user_repository = UserRepository()
customer_repository = CustomerRepository()
technician_repository = TechnicianRepository()
document_repository = DocumentRepository()
part_repository = PartRepository()
manual_repository = ManualRepository()
machine_instance_repository = MachineInstanceRepository()
dashboard_repository = DashboardRepository()