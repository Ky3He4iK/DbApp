from datetime import datetime
import typing

from .DatabaseLowLevel import *



@dataclass
class Worker:
    
    WorkerId: int
    
    
    Name: str
    
    Status: str
    

@dataclass
class ZoneInfo:
    
    ZoneId: int
    
    
    Status: str
    
    Location: str
    
    Description: str
    

@dataclass
class Machine:
    
    MachineId: int
    
    
    Name: str
    
    Status: str
    
    ZoneId: int
    
    WorkerId: typing.Optional[int]
    

@dataclass
class Customer:
    
    CustomerId: int
    
    
    AdditionalInfo: typing.Optional[str]
    
    Mail: str
    
    Phone: int
    

@dataclass
class OrderInfo:
    
    OrderId: int
    
    
    CustomerId: int
    
    DeliveryAddress: str
    
    Price: int
    
    Status: str
    
    PlateCount: int
    
    Notes: typing.Optional[str]
    

@dataclass
class FactManufactoring:
    
    FactId: int
    
    
    OrderId: int
    
    AcceptedPlates: int
    

    StartTime: datetime

    EndTime: datetime
    RejectedPlates: int


@dataclass
class PlateStorage:
    
    OrderId: int
    
    PlateId: int
    
    
    NumberInOrder: int
    

@dataclass
class PlateStatus:
    
    PlateId: int
    
    OrderId: int
    
    

    Status: str
    InstalledComponents: int

    MachineId: typing.Optional[int]
    

@dataclass
class Components:
    
    ComponentId: int
    
    
    Count: int
    
    Name: str
    

@dataclass
class PlateConfiguration:
    
    PlateId: int
    
    OrderId: int
    
    
    Height: int
    
    Width: int
    
    Layers: int
    
    Material: str
    
    Thickness: float
    

@dataclass
class ComponentInfo:
    
    InstalledOrder: int
    
    PlateId: int
    
    OrderId: int
    
    
    posX: float
    
    posY: float
    
    ComponentId: int
    



table_info_data = {

    'worker': TableInfo(
        'Worker',
        ['WorkerId', ],
        ['Name', 'Status', ],
        [int, ],
        [str, str, ],
        Worker
    ),

    'zone_info': TableInfo(
        'ZoneInfo',
        ['ZoneId', ],
        ['Status', 'Location', 'Description', ],
        [int, ],
        [str, str, str, ],
        ZoneInfo
    ),

    'machine': TableInfo(
        'Machine',
        ['MachineId', ],
        ['Name', 'Status', 'ZoneId', 'WorkerId', ],
        [int, ],
        [str, str, int, typing.Optional[int], ],
        Machine
    ),

    'customer': TableInfo(
        'Customer',
        ['CustomerId', ],
        ['AdditionalInfo', 'Mail', 'Phone', ],
        [int, ],
        [typing.Optional[str], str, int, ],
        Customer
    ),

    'order_info': TableInfo(
        'OrderInfo',
        ['OrderId', ],
        ['CustomerId', 'DeliveryAddress', 'Price', 'Status', 'PlateCount', 'Notes', ],
        [int, ],
        [int, str, int, str, int, typing.Optional[str], ],
        OrderInfo
    ),

    'fact_manufactoring': TableInfo(
        'FactManufactoring',
        ['FactId', ],
        ['OrderId', 'AcceptedPlates', 'RejectedPlates', 'StartTime', 'EndTime', ],
        [int, ],
        [int, int, int, datetime, datetime, ],
        FactManufactoring
    ),

    'plate_storage': TableInfo(
        'PlateStorage',
        ['OrderId', 'PlateId', ],
        ['NumberInOrder', ],
        [int, int, ],
        [int, ],
        PlateStorage
    ),

    'plate_status': TableInfo(
        'PlateStatus',
        ['PlateId', 'OrderId', ],
        ['InstalledComponents', 'Status', 'MachineId', ],
        [int, int, ],
        [int, str, typing.Optional[int], ],
        PlateStatus
    ),

    'components': TableInfo(
        'Components',
        ['ComponentId', ],
        ['Count', 'Name', ],
        [int, ],
        [int, str, ],
        Components
    ),

    'plate_configuration': TableInfo(
        'PlateConfiguration',
        ['PlateId', 'OrderId', ],
        ['Height', 'Width', 'Layers', 'Material', 'Thickness', ],
        [int, int, ],
        [int, int, int, str, float, ],
        PlateConfiguration
    ),

    'component_info': TableInfo(
        'ComponentInfo',
        ['InstalledOrder', 'PlateId', 'OrderId', ],
        ['posX', 'posY', 'ComponentId', ],
        [int, int, int, ],
        [float, float, int, ],
        ComponentInfo
    ),

}


class DAO(DatabaseLowLevel):
    def __init__(self):
        super().__init__()

    
    def get_worker(self, worker_id: int, ) -> Optional[Worker]:
        return self.get(Worker(worker_id, None, None, ), table_info_data['worker'])

    def filter_worker(self, worker_id: Optional[int] = None, order_by: Optional[str] = None) -> List[Worker]:
        return self.filter(Worker(worker_id, None, None, ), table_info_data['worker'], order_by=order_by)

    def search_worker(self, worker_id: Optional[int] = None, name: Optional[str] = None, status: Optional[str] = None, order_by: Optional[str] = None) -> List[Worker]:
        return self.search(Worker(worker_id, name, status, ), table_info_data['worker'], order_by=order_by)

    def set_worker(self, worker: Worker) -> None:
        return self.set(worker, table_info_data['worker'])

    def get_all_workers(self, order_by: Optional[str] = None) -> List[Worker]:
        return self.get_all(table_info_data['worker'], order_by)

    def remove_worker(self, worker: Worker) -> None:
        return self.remove(worker, table_info_data['worker'])
    
    def get_zone_info(self, zone_id: int, ) -> Optional[ZoneInfo]:
        return self.get(ZoneInfo(zone_id, None, None, None, ), table_info_data['zone_info'])

    def filter_zone_info(self, zone_id: Optional[int] = None, order_by: Optional[str] = None) -> List[ZoneInfo]:
        return self.filter(ZoneInfo(zone_id, None, None, None, ), table_info_data['zone_info'], order_by=order_by)

    def search_zone_info(self, zone_id: Optional[int] = None, status: Optional[str] = None, location: Optional[str] = None, description: Optional[str] = None, order_by: Optional[str] = None) -> List[ZoneInfo]:
        return self.search(ZoneInfo(zone_id, status, location, description, ), table_info_data['zone_info'], order_by=order_by)

    def set_zone_info(self, zone_info: ZoneInfo) -> None:
        return self.set(zone_info, table_info_data['zone_info'])

    def get_all_zone_infos(self, order_by: Optional[str] = None) -> List[ZoneInfo]:
        return self.get_all(table_info_data['zone_info'], order_by)

    def remove_zone_info(self, zone_info: ZoneInfo) -> None:
        return self.remove(zone_info, table_info_data['zone_info'])
    
    def get_machine(self, machine_id: int, ) -> Optional[Machine]:
        return self.get(Machine(machine_id, None, None, None, None, ), table_info_data['machine'])

    def filter_machine(self, machine_id: Optional[int] = None, order_by: Optional[str] = None) -> List[Machine]:
        return self.filter(Machine(machine_id, None, None, None, None, ), table_info_data['machine'], order_by=order_by)

    def search_machine(self, machine_id: Optional[int] = None, name: Optional[str] = None, status: Optional[str] = None, zone_id: Optional[int] = None, worker_id: Optional[typing.Optional[int]] = None, order_by: Optional[str] = None) -> List[Machine]:
        return self.search(Machine(machine_id, name, status, zone_id, worker_id, ), table_info_data['machine'], order_by=order_by)

    def set_machine(self, machine: Machine) -> None:
        return self.set(machine, table_info_data['machine'])

    def get_all_machines(self, order_by: Optional[str] = None) -> List[Machine]:
        return self.get_all(table_info_data['machine'], order_by)

    def remove_machine(self, machine: Machine) -> None:
        return self.remove(machine, table_info_data['machine'])
    
    def get_customer(self, customer_id: int, ) -> Optional[Customer]:
        return self.get(Customer(customer_id, None, None, None, ), table_info_data['customer'])

    def filter_customer(self, customer_id: Optional[int] = None, order_by: Optional[str] = None) -> List[Customer]:
        return self.filter(Customer(customer_id, None, None, None, ), table_info_data['customer'], order_by=order_by)

    def search_customer(self, customer_id: Optional[int] = None, additional_info: Optional[typing.Optional[str]] = None, mail: Optional[str] = None, phone: Optional[int] = None, order_by: Optional[str] = None) -> List[Customer]:
        return self.search(Customer(customer_id, additional_info, mail, phone, ), table_info_data['customer'], order_by=order_by)

    def set_customer(self, customer: Customer) -> None:
        return self.set(customer, table_info_data['customer'])

    def get_all_customers(self, order_by: Optional[str] = None) -> List[Customer]:
        return self.get_all(table_info_data['customer'], order_by)

    def remove_customer(self, customer: Customer) -> None:
        return self.remove(customer, table_info_data['customer'])
    
    def get_order_info(self, order_id: int, ) -> Optional[OrderInfo]:
        return self.get(OrderInfo(order_id, None, None, None, None, None, None, ), table_info_data['order_info'])

    def filter_order_info(self, order_id: Optional[int] = None, order_by: Optional[str] = None) -> List[OrderInfo]:
        return self.filter(OrderInfo(order_id, None, None, None, None, None, None, ), table_info_data['order_info'], order_by=order_by)

    def search_order_info(self, order_id: Optional[int] = None, customer_id: Optional[int] = None, delivery_address: Optional[str] = None, price: Optional[int] = None, status: Optional[str] = None, plate_count: Optional[int] = None, notes: Optional[typing.Optional[str]] = None, order_by: Optional[str] = None) -> List[OrderInfo]:
        return self.search(OrderInfo(order_id, customer_id, delivery_address, price, status, plate_count, notes, ), table_info_data['order_info'], order_by=order_by)

    def set_order_info(self, order_info: OrderInfo) -> None:
        return self.set(order_info, table_info_data['order_info'])

    def get_all_order_infos(self, order_by: Optional[str] = None) -> List[OrderInfo]:
        return self.get_all(table_info_data['order_info'], order_by)

    def remove_order_info(self, order_info: OrderInfo) -> None:
        return self.remove(order_info, table_info_data['order_info'])
    
    def get_fact_manufactoring(self, fact_id: int, ) -> Optional[FactManufactoring]:
        return self.get(FactManufactoring(fact_id, None, None, None, None, None, ), table_info_data['fact_manufactoring'])

    def filter_fact_manufactoring(self, fact_id: Optional[int] = None, order_by: Optional[str] = None) -> List[FactManufactoring]:
        return self.filter(FactManufactoring(fact_id, None, None, None, None, None, ), table_info_data['fact_manufactoring'], order_by=order_by)

    def search_fact_manufactoring(self, fact_id: Optional[int] = None, order_id: Optional[int] = None, accepted_plates: Optional[int] = None, rejected_plates: Optional[int] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, order_by: Optional[str] = None) -> List[FactManufactoring]:
        return self.search(FactManufactoring(fact_id, order_id, accepted_plates, rejected_plates, start_time, end_time, ), table_info_data['fact_manufactoring'], order_by=order_by)

    def set_fact_manufactoring(self, fact_manufactoring: FactManufactoring) -> None:
        return self.set(fact_manufactoring, table_info_data['fact_manufactoring'])

    def get_all_fact_manufactorings(self, order_by: Optional[str] = None) -> List[FactManufactoring]:
        return self.get_all(table_info_data['fact_manufactoring'], order_by)

    def remove_fact_manufactoring(self, fact_manufactoring: FactManufactoring) -> None:
        return self.remove(fact_manufactoring, table_info_data['fact_manufactoring'])
    
    def get_plate_storage(self, order_id: int, plate_id: int, ) -> Optional[PlateStorage]:
        return self.get(PlateStorage(order_id, plate_id, None, ), table_info_data['plate_storage'])

    def filter_plate_storage(self, order_id: Optional[int] = None, plate_id: Optional[int] = None, order_by: Optional[str] = None) -> List[PlateStorage]:
        return self.filter(PlateStorage(order_id, plate_id, None, ), table_info_data['plate_storage'], order_by=order_by)

    def search_plate_storage(self, order_id: Optional[int] = None, plate_id: Optional[int] = None, number_in_order: Optional[int] = None, order_by: Optional[str] = None) -> List[PlateStorage]:
        return self.search(PlateStorage(order_id, plate_id, number_in_order, ), table_info_data['plate_storage'], order_by=order_by)

    def set_plate_storage(self, plate_storage: PlateStorage) -> None:
        return self.set(plate_storage, table_info_data['plate_storage'])

    def get_all_plate_storages(self, order_by: Optional[str] = None) -> List[PlateStorage]:
        return self.get_all(table_info_data['plate_storage'], order_by)

    def remove_plate_storage(self, plate_storage: PlateStorage) -> None:
        return self.remove(plate_storage, table_info_data['plate_storage'])
    
    def get_plate_status(self, plate_id: int, order_id: int, ) -> Optional[PlateStatus]:
        return self.get(PlateStatus(plate_id, order_id, None, None, None, ), table_info_data['plate_status'])

    def filter_plate_status(self, plate_id: Optional[int] = None, order_id: Optional[int] = None, order_by: Optional[str] = None) -> List[PlateStatus]:
        return self.filter(PlateStatus(plate_id, order_id, None, None, None, ), table_info_data['plate_status'], order_by=order_by)

    def search_plate_status(self, plate_id: Optional[int] = None, order_id: Optional[int] = None, installed_components: Optional[int] = None, status: Optional[str] = None, machine_id: Optional[typing.Optional[int]] = None, order_by: Optional[str] = None) -> List[PlateStatus]:
        return self.search(PlateStatus(plate_id, order_id, installed_components, status, machine_id, ), table_info_data['plate_status'], order_by=order_by)

    def set_plate_status(self, plate_status: PlateStatus) -> None:
        return self.set(plate_status, table_info_data['plate_status'])

    def get_all_plate_statuss(self, order_by: Optional[str] = None) -> List[PlateStatus]:
        return self.get_all(table_info_data['plate_status'], order_by)

    def remove_plate_status(self, plate_status: PlateStatus) -> None:
        return self.remove(plate_status, table_info_data['plate_status'])
    
    def get_components(self, component_id: int, ) -> Optional[Components]:
        return self.get(Components(component_id, None, None, ), table_info_data['components'])

    def filter_components(self, component_id: Optional[int] = None, order_by: Optional[str] = None) -> List[Components]:
        return self.filter(Components(component_id, None, None, ), table_info_data['components'], order_by=order_by)

    def search_components(self, component_id: Optional[int] = None, count: Optional[int] = None, name: Optional[str] = None, order_by: Optional[str] = None) -> List[Components]:
        return self.search(Components(component_id, count, name, ), table_info_data['components'], order_by=order_by)

    def set_components(self, components: Components) -> None:
        return self.set(components, table_info_data['components'])

    def get_all_componentss(self, order_by: Optional[str] = None) -> List[Components]:
        return self.get_all(table_info_data['components'], order_by)

    def remove_components(self, components: Components) -> None:
        return self.remove(components, table_info_data['components'])
    
    def get_plate_configuration(self, plate_id: int, order_id: int, ) -> Optional[PlateConfiguration]:
        return self.get(PlateConfiguration(plate_id, order_id, None, None, None, None, None, ), table_info_data['plate_configuration'])

    def filter_plate_configuration(self, plate_id: Optional[int] = None, order_id: Optional[int] = None, order_by: Optional[str] = None) -> List[PlateConfiguration]:
        return self.filter(PlateConfiguration(plate_id, order_id, None, None, None, None, None, ), table_info_data['plate_configuration'], order_by=order_by)

    def search_plate_configuration(self, plate_id: Optional[int] = None, order_id: Optional[int] = None, height: Optional[int] = None, width: Optional[int] = None, layers: Optional[int] = None, material: Optional[str] = None, thickness: Optional[float] = None, order_by: Optional[str] = None) -> List[PlateConfiguration]:
        return self.search(PlateConfiguration(plate_id, order_id, height, width, layers, material, thickness, ), table_info_data['plate_configuration'], order_by=order_by)

    def set_plate_configuration(self, plate_configuration: PlateConfiguration) -> None:
        return self.set(plate_configuration, table_info_data['plate_configuration'])

    def get_all_plate_configurations(self, order_by: Optional[str] = None) -> List[PlateConfiguration]:
        return self.get_all(table_info_data['plate_configuration'], order_by)

    def remove_plate_configuration(self, plate_configuration: PlateConfiguration) -> None:
        return self.remove(plate_configuration, table_info_data['plate_configuration'])
    
    def get_component_info(self, installed_order: int, plate_id: int, order_id: int, ) -> Optional[ComponentInfo]:
        return self.get(ComponentInfo(installed_order, plate_id, order_id, None, None, None, ), table_info_data['component_info'])

    def filter_component_info(self, installed_order: Optional[int] = None, plate_id: Optional[int] = None, order_id: Optional[int] = None, order_by: Optional[str] = None) -> List[ComponentInfo]:
        return self.filter(ComponentInfo(installed_order, plate_id, order_id, None, None, None, ), table_info_data['component_info'], order_by=order_by)

    def search_component_info(self, installed_order: Optional[int] = None, plate_id: Optional[int] = None, order_id: Optional[int] = None, pos_x: Optional[float] = None, pos_y: Optional[float] = None, component_id: Optional[int] = None, order_by: Optional[str] = None) -> List[ComponentInfo]:
        return self.search(ComponentInfo(installed_order, plate_id, order_id, pos_x, pos_y, component_id, ), table_info_data['component_info'], order_by=order_by)

    def set_component_info(self, component_info: ComponentInfo) -> None:
        return self.set(component_info, table_info_data['component_info'])

    def get_all_component_infos(self, order_by: Optional[str] = None) -> List[ComponentInfo]:
        return self.get_all(table_info_data['component_info'], order_by)

    def remove_component_info(self, component_info: ComponentInfo) -> None:
        return self.remove(component_info, table_info_data['component_info'])
    
