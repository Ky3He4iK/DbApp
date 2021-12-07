from datetime import datetime
import typing

from DatabaseLowLevel import *



@dataclass
class Worker:
    
    worker_id: int
    
    
    name: str
    
    status: str
    

@dataclass
class ZoneInfo:
    
    zone_id: int
    
    
    status: str
    
    location: str
    
    description: str
    

@dataclass
class Machine:
    
    machine_id: int
    
    
    name: str
    
    status: str
    
    zone_id: int
    
    worker_id: typing.Optional[int]
    

@dataclass
class Customer:
    
    customer_id: int
    
    
    additional_info: typing.Optional[str]
    
    mail: str
    
    phone: int
    

@dataclass
class OrderInfo:
    
    order_id: int
    
    
    customer_id: int
    
    delivery_address: str
    
    price: int
    
    status: str
    
    plate_count: int
    
    notes: typing.Optional[str]
    

@dataclass
class FactManufactoring:
    
    fact_id: int
    
    
    order_id: int
    
    accepted_plates: int
    
    rejected_plates: int
    
    start_time: datetime
    
    end_time: datetime
    

@dataclass
class PlateStorage:
    
    order_id: int
    
    plate_id: int
    
    
    number_in_order: int
    

@dataclass
class PlateStatus:
    
    plate_id: int
    
    order_id: int
    
    
    installed_components: int
    
    status: str
    
    machine_id: typing.Optional[int]
    

@dataclass
class Components:
    
    component_id: int
    
    
    count: int
    
    name: str
    

@dataclass
class PlateConfiguration:
    
    plate_id: int
    
    order_id: int
    
    
    height: int
    
    width: int
    
    layers: int
    
    material: str
    
    thickness: float
    

@dataclass
class ComponentInfo:
    
    installed_order: int
    
    plate_id: int
    
    order_id: int
    
    
    pos_x: float
    
    pos_y: float
    
    component_id: int
    



table_info_data = {

    'worker': TableInfo(
        'worker',
        ['WorkerId', ],
        ['Name', 'Status', ],
        Worker
    ),

    'zone_info': TableInfo(
        'zone_info',
        ['ZoneId', ],
        ['Status', 'Location', 'Description', ],
        ZoneInfo
    ),

    'machine': TableInfo(
        'machine',
        ['MachineId', ],
        ['Name', 'Status', 'ZoneId', 'WorkerId', ],
        Machine
    ),

    'customer': TableInfo(
        'customer',
        ['CustomerId', ],
        ['AdditionalInfo', 'Mail', 'Phone', ],
        Customer
    ),

    'order_info': TableInfo(
        'order_info',
        ['OrderId', ],
        ['CustomerId', 'DeliveryAddress', 'Price', 'Status', 'PlateCount', 'Notes', ],
        OrderInfo
    ),

    'fact_manufactoring': TableInfo(
        'fact_manufactoring',
        ['FactId', ],
        ['OrderId', 'AcceptedPlates', 'RejectedPlates', 'StartTime', 'EndTime', ],
        FactManufactoring
    ),

    'plate_storage': TableInfo(
        'plate_storage',
        ['OrderId', 'PlateId', ],
        ['NumberInOrder', ],
        PlateStorage
    ),

    'plate_status': TableInfo(
        'plate_status',
        ['PlateId', 'OrderId', ],
        ['InstalledComponents', 'Status', 'MachineId', ],
        PlateStatus
    ),

    'components': TableInfo(
        'components',
        ['ComponentId', ],
        ['Count', 'Name', ],
        Components
    ),

    'plate_configuration': TableInfo(
        'plate_configuration',
        ['PlateId', 'OrderId', ],
        ['Height', 'Width', 'Layers', 'Material', 'Thickness', ],
        PlateConfiguration
    ),

    'component_info': TableInfo(
        'component_info',
        ['InstalledOrder', 'PlateId', 'OrderId', ],
        ['posX', 'posY', 'ComponentId', ],
        ComponentInfo
    ),

}


class DAO(DatabaseLowLevel):
    def __init__(self):
        super().__init__()

    
    def get_worker(self, worker_id: int, ) -> Optional[Worker]:
        return self.get(Worker(worker_id, None, None, ), table_info_data['worker'])

    def filter_worker(self, worker_id: Optional[int] = None, ) -> List[Worker]:
        return self.filter(Worker(worker_id, None, None, ), table_info_data['worker'])

    def set_worker(self, worker: Worker) -> None:
        return self.set(worker, table_info_data['worker'])

    def get_all_workers(self) -> List[Worker]:
        return self.get_all(table_info_data['worker'])

    def remove_worker(self, worker: Worker) -> None:
        return self.remove(worker, table_info_data['worker'])
    
    def get_zone_info(self, zone_id: int, ) -> Optional[ZoneInfo]:
        return self.get(ZoneInfo(zone_id, None, None, None, ), table_info_data['zone_info'])

    def filter_zone_info(self, zone_id: Optional[int] = None, ) -> List[ZoneInfo]:
        return self.filter(ZoneInfo(zone_id, None, None, None, ), table_info_data['zone_info'])

    def set_zone_info(self, zone_info: ZoneInfo) -> None:
        return self.set(zone_info, table_info_data['zone_info'])

    def get_all_zone_infos(self) -> List[ZoneInfo]:
        return self.get_all(table_info_data['zone_info'])

    def remove_zone_info(self, zone_info: ZoneInfo) -> None:
        return self.remove(zone_info, table_info_data['zone_info'])
    
    def get_machine(self, machine_id: int, ) -> Optional[Machine]:
        return self.get(Machine(machine_id, None, None, None, None, ), table_info_data['machine'])

    def filter_machine(self, machine_id: Optional[int] = None, ) -> List[Machine]:
        return self.filter(Machine(machine_id, None, None, None, None, ), table_info_data['machine'])

    def set_machine(self, machine: Machine) -> None:
        return self.set(machine, table_info_data['machine'])

    def get_all_machines(self) -> List[Machine]:
        return self.get_all(table_info_data['machine'])

    def remove_machine(self, machine: Machine) -> None:
        return self.remove(machine, table_info_data['machine'])
    
    def get_customer(self, customer_id: int, ) -> Optional[Customer]:
        return self.get(Customer(customer_id, None, None, None, ), table_info_data['customer'])

    def filter_customer(self, customer_id: Optional[int] = None, ) -> List[Customer]:
        return self.filter(Customer(customer_id, None, None, None, ), table_info_data['customer'])

    def set_customer(self, customer: Customer) -> None:
        return self.set(customer, table_info_data['customer'])

    def get_all_customers(self) -> List[Customer]:
        return self.get_all(table_info_data['customer'])

    def remove_customer(self, customer: Customer) -> None:
        return self.remove(customer, table_info_data['customer'])
    
    def get_order_info(self, order_id: int, ) -> Optional[OrderInfo]:
        return self.get(OrderInfo(order_id, None, None, None, None, None, None, ), table_info_data['order_info'])

    def filter_order_info(self, order_id: Optional[int] = None, ) -> List[OrderInfo]:
        return self.filter(OrderInfo(order_id, None, None, None, None, None, None, ), table_info_data['order_info'])

    def set_order_info(self, order_info: OrderInfo) -> None:
        return self.set(order_info, table_info_data['order_info'])

    def get_all_order_infos(self) -> List[OrderInfo]:
        return self.get_all(table_info_data['order_info'])

    def remove_order_info(self, order_info: OrderInfo) -> None:
        return self.remove(order_info, table_info_data['order_info'])
    
    def get_fact_manufactoring(self, fact_id: int, ) -> Optional[FactManufactoring]:
        return self.get(FactManufactoring(fact_id, None, None, None, None, None, ), table_info_data['fact_manufactoring'])

    def filter_fact_manufactoring(self, fact_id: Optional[int] = None, ) -> List[FactManufactoring]:
        return self.filter(FactManufactoring(fact_id, None, None, None, None, None, ), table_info_data['fact_manufactoring'])

    def set_fact_manufactoring(self, fact_manufactoring: FactManufactoring) -> None:
        return self.set(fact_manufactoring, table_info_data['fact_manufactoring'])

    def get_all_fact_manufactorings(self) -> List[FactManufactoring]:
        return self.get_all(table_info_data['fact_manufactoring'])

    def remove_fact_manufactoring(self, fact_manufactoring: FactManufactoring) -> None:
        return self.remove(fact_manufactoring, table_info_data['fact_manufactoring'])
    
    def get_plate_storage(self, order_id: int, plate_id: int, ) -> Optional[PlateStorage]:
        return self.get(PlateStorage(order_id, plate_id, None, ), table_info_data['plate_storage'])

    def filter_plate_storage(self, order_id: Optional[int] = None, plate_id: Optional[int] = None, ) -> List[PlateStorage]:
        return self.filter(PlateStorage(order_id, plate_id, None, ), table_info_data['plate_storage'])

    def set_plate_storage(self, plate_storage: PlateStorage) -> None:
        return self.set(plate_storage, table_info_data['plate_storage'])

    def get_all_plate_storages(self) -> List[PlateStorage]:
        return self.get_all(table_info_data['plate_storage'])

    def remove_plate_storage(self, plate_storage: PlateStorage) -> None:
        return self.remove(plate_storage, table_info_data['plate_storage'])
    
    def get_plate_status(self, plate_id: int, order_id: int, ) -> Optional[PlateStatus]:
        return self.get(PlateStatus(plate_id, order_id, None, None, None, ), table_info_data['plate_status'])

    def filter_plate_status(self, plate_id: Optional[int] = None, order_id: Optional[int] = None, ) -> List[PlateStatus]:
        return self.filter(PlateStatus(plate_id, order_id, None, None, None, ), table_info_data['plate_status'])

    def set_plate_status(self, plate_status: PlateStatus) -> None:
        return self.set(plate_status, table_info_data['plate_status'])

    def get_all_plate_statuss(self) -> List[PlateStatus]:
        return self.get_all(table_info_data['plate_status'])

    def remove_plate_status(self, plate_status: PlateStatus) -> None:
        return self.remove(plate_status, table_info_data['plate_status'])
    
    def get_components(self, component_id: int, ) -> Optional[Components]:
        return self.get(Components(component_id, None, None, ), table_info_data['components'])

    def filter_components(self, component_id: Optional[int] = None, ) -> List[Components]:
        return self.filter(Components(component_id, None, None, ), table_info_data['components'])

    def set_components(self, components: Components) -> None:
        return self.set(components, table_info_data['components'])

    def get_all_componentss(self) -> List[Components]:
        return self.get_all(table_info_data['components'])

    def remove_components(self, components: Components) -> None:
        return self.remove(components, table_info_data['components'])
    
    def get_plate_configuration(self, plate_id: int, order_id: int, ) -> Optional[PlateConfiguration]:
        return self.get(PlateConfiguration(plate_id, order_id, None, None, None, None, None, ), table_info_data['plate_configuration'])

    def filter_plate_configuration(self, plate_id: Optional[int] = None, order_id: Optional[int] = None, ) -> List[PlateConfiguration]:
        return self.filter(PlateConfiguration(plate_id, order_id, None, None, None, None, None, ), table_info_data['plate_configuration'])

    def set_plate_configuration(self, plate_configuration: PlateConfiguration) -> None:
        return self.set(plate_configuration, table_info_data['plate_configuration'])

    def get_all_plate_configurations(self) -> List[PlateConfiguration]:
        return self.get_all(table_info_data['plate_configuration'])

    def remove_plate_configuration(self, plate_configuration: PlateConfiguration) -> None:
        return self.remove(plate_configuration, table_info_data['plate_configuration'])
    
    def get_component_info(self, installed_order: int, plate_id: int, order_id: int, ) -> Optional[ComponentInfo]:
        return self.get(ComponentInfo(installed_order, plate_id, order_id, None, None, None, ), table_info_data['component_info'])

    def filter_component_info(self, installed_order: Optional[int] = None, plate_id: Optional[int] = None, order_id: Optional[int] = None, ) -> List[ComponentInfo]:
        return self.filter(ComponentInfo(installed_order, plate_id, order_id, None, None, None, ), table_info_data['component_info'])

    def set_component_info(self, component_info: ComponentInfo) -> None:
        return self.set(component_info, table_info_data['component_info'])

    def get_all_component_infos(self) -> List[ComponentInfo]:
        return self.get_all(table_info_data['component_info'])

    def remove_component_info(self, component_info: ComponentInfo) -> None:
        return self.remove(component_info, table_info_data['component_info'])
    
