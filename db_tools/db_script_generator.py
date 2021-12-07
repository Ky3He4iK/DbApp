from dataclasses import dataclass
from typing import List, Tuple, Type, Optional, Iterable
import re
from datetime import datetime

'''
sample:
CREATE TABLE PlateStatus
(
    PlateId             INTEGER     NOT NULL,
    InstalledComponents INTEGER     NOT NULL,
    Status              VARCHAR(31) NOT NULL,
    OrderId             INTEGER     NOT NULL,
    MachineId           INTEGER     NULL,
    PRIMARY KEY (OrderId, PlateId),
    FOREIGN KEY R_5 (PlateId, OrderId) REFERENCES PlateStorage (PlateId, OrderId),
    FOREIGN KEY R_17 (MachineId) REFERENCES Machine (MachineId)
);
'''


types_mapping = {
    int: 'int',
    str: 'str',
    float: 'float',
    datetime: 'datetime',
    None: 'None'
}


@dataclass
class NullableType:
    t: Type
    nullable: bool = False

    def __str__(self):
        if self.nullable:
            return str(Optional[self.t])
        return self.t.__name__


@dataclass
class ClassInfoPre:
    classname: str
    primary_keys: List[str]  # name
    foreign_keys: List[Tuple[str, str, str]]  # field name - origin table - origin name
    fields: List[Tuple[str, NullableType]]  # name - type


@dataclass
class FieldInfo:
    name_pc: str
    name_cc: str
    type: str


@dataclass
class ClassInfo:
    name_pc: str
    name_cc: str
    primaries: List[FieldInfo]
    others: List[FieldInfo]


@dataclass
class ProcessContext:
    table: Optional[ClassInfo] = None
    primary: Optional[FieldInfo] = None
    other: Optional[FieldInfo] = None


# create list of ClassInfoPre from `CREATE TABLE ... (...)` command
def parse_create_table(create_query: str) -> ClassInfoPre:
    def parse_type(type_name: str, is_null: Optional[str] = None, is_not_null: Optional[str] = None) \
            -> Optional[NullableType]:
        known_types = {
            'INTEGER': int,
            'NUMERIC': int,
            'VARCHAR': str,
            'FLOAT': float,
            'TIMESTAMP': datetime,
        }
        if type_name.startswith('VARCHAR('):
            type_name = 'VARCHAR'
        if type_name.startswith('NUMERIC('):
            type_name = 'NUMERIC'
        if type_name not in known_types:
            print("Warning: unknown type " + type_name)
            return None
        t = NullableType(known_types[type_name])
        if is_null is not None and is_not_null is None:
            t.nullable = True
        return t

    name = create_query[:create_query.find('(')].strip('\n ').split()[-1]

    field_regex = re.compile(r'^ *(?P<field>\w+) +(?P<type>[\w()]+)'
                             r'( +((?P<null>NULL)|(?P<not_null>NOT NULL)))?( UNIQUE)?,?$')
    primary_regex = re.compile(r'^ *PRIMARY KEY \((?P<fields>(\w+,? ?)+)\),?$')
    foreign_regex = re.compile(r'^ *FOREIGN KEY \w+ \((?P<fields>(\w+,? ?)+)\) REFERENCES '
                               r'(?P<host_table>\w+) \((?P<host_fields>(\w+,? ?)+)\),?$')
    fields = create_query[create_query.find('(') + 1:create_query.rfind(')')].splitlines()
    fields = list(map(lambda x: x.strip(), fields))

    fields_list, primary_list, foreign_list = [], [], []
    for field in filter(lambda f: len(f) > 0, fields):
        match = field_regex.match(field)
        if match:
            groups = match.groupdict()
            fields_list.append((groups['field'], parse_type(groups['type'], groups['null'], groups['not_null'])))
            continue
        match = primary_regex.match(field)
        if match:
            groups = match.groupdict()
            for f in groups['fields'].split(', '):
                primary_list.append(f)
            continue
        match = foreign_regex.match(field)
        if match:
            groups = match.groupdict()
            res = groups['fields'].split(', '), groups['host_table'], groups['host_fields'].split(', ')
            if len(res[0]) != len(res[2]):
                print("Warning: fields count not the same", groups, field, sep='\n      ')
            for f in zip(res[0], res[2]):
                foreign_list.append((f[0], res[1], f[1]))
            continue
        print("Warning: can't parse " + field)
    return ClassInfoPre(name, primary_list, foreign_list, fields_list)


# List[ClassInfoPre] -> List[ClassInfo]
def process_class_info(pre_classes: Iterable[ClassInfoPre]) -> List[ClassInfo]:
    def camel_to_snake(name):
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def process_single(pre_class: ClassInfoPre) -> ClassInfo:
        primaries, others = [], []
        for field in pre_class.fields:
            name_pc, name_cc = camel_to_snake(field[0]), field[0]
            if field[0] in pre_class.primary_keys:
                primaries.append(FieldInfo(name_pc, name_cc, str(field[1])))
            else:
                others.append(FieldInfo(name_pc, name_cc, str(field[1])))
        return ClassInfo(camel_to_snake(pre_class.classname), pre_class.classname, primaries, others)

    return list(map(process_single, pre_classes))


def process_template_fragment(template: str, classes: List[ClassInfo], context: ProcessContext) -> str:
    while True:
        temp_pos = template.find('{{')
        temp_pos_end = template.find('}}')
        if temp_pos == -1:
            return template
        temp_info = template[temp_pos:temp_pos_end + 2]
        template_pre = template[:temp_pos]
        if temp_info == '{{tables.begin}}':
            temp_end = template.find('{{tables.end}}')
            for table in classes:
                context_rec = ProcessContext(table)
                template_pre += process_template_fragment(template[temp_pos_end + 2:temp_end], classes, context_rec)
            template = template_pre + template[temp_end + len('{{tables.end}}'):]
            continue
        if temp_info == '{{primaries.begin}}':
            temp_end = template.find('{{primaries.end}}')
            for primary in context.table.primaries:
                context_rec = ProcessContext(context.table, primary, context.other)
                template_pre += process_template_fragment(template[temp_pos_end + 2:temp_end], classes, context_rec)
            template = template_pre + template[temp_end + len('{{primaries.end}}'):]
            continue
        if temp_info == '{{others.begin}}':
            temp_end = template.find('{{others.end}}')
            for other in context.table.others:
                context_rec = ProcessContext(context.table, context.primary, other)
                template_pre += process_template_fragment(template[temp_pos_end + 2:temp_end], classes, context_rec)
            template = template_pre + template[temp_end + len('{{others.end}}'):]
            continue
        fields = {
            '{{name_pc}}': lambda: context.table.name_pc,
            '{{name_cc}}': lambda: context.table.name_cc,
            '{{primary.type}}': lambda: context.primary.type,
            '{{primary.name_pc}}': lambda: context.primary.name_pc,
            '{{primary.name_cc}}': lambda: context.primary.name_cc,
            '{{other.type}}': lambda: context.other.type,
            '{{other.name_pc}}': lambda: context.other.name_pc,
            '{{other.name_cc}}': lambda: context.other.name_cc,
        }
        if temp_info in fields:
            template = template_pre + fields[temp_info]() + template[temp_pos_end + 2:]
            continue
        print("Unknown token " + temp_info)


def main():
    commands = map(lambda x: x.strip('\n '), open('db_tools/create_db.sql').read().split(';'))
    # for cmd in filter(lambda cmd: cmd.startswith('CREATE'), commands):
    #     print(parse_create_table(cmd))
    class_info_pre = map(parse_create_table, filter(lambda cmd: cmd.startswith('CREATE'), commands))
    class_info = process_class_info(class_info_pre)
    print('\n'.join(map(str, class_info)))
    dao_text = process_template_fragment(open('db_tools/DAO_Template.py').read(), class_info, ProcessContext())
    # print(dao_text)
    with open('db_tools/DAO.py', 'w') as file:
        file.write(dao_text)


if __name__ == '__main__':
    main()
