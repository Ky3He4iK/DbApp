from datetime import datetime
import typing

from DatabaseLowLevel import *


{{tables.begin}}
@dataclass
class {{name_cc}}:
    {{primaries.begin}}
    {{primary.name_pc}}: {{primary.type}}
    {{primaries.end}}
    {{others.begin}}
    {{other.name_pc}}: {{other.type}}
    {{others.end}}
{{tables.end}}


table_info_data = {
{{tables.begin}}
    '{{name_pc}}': TableInfo(
        '{{name_pc}}',
        [{{primaries.begin}}'{{primary.name_cc}}', {{primaries.end}}],
        [{{others.begin}}'{{other.name_cc}}', {{others.end}}],
        {{name_cc}}
    ),
{{tables.end}}
}


class DAO(DatabaseLowLevel):
    def __init__(self):
        super().__init__()

    {{tables.begin}}
    def get_{{name_pc}}(self, {{primaries.begin}}{{primary.name_pc}}: {{primary.type}}, {{primaries.end}}) -> Optional[{{name_cc}}]:
        return self.get({{name_cc}}({{primaries.begin}}{{primary.name_pc}}, {{primaries.end}}{{others.begin}}None, {{others.end}}), table_info_data['{{name_pc}}'])

    def filter_{{name_pc}}(self, {{primaries.begin}}{{primary.name_pc}}: Optional[{{primary.type}}] = None, {{primaries.end}}order_by: Optional[str] = None) -> List[{{name_cc}}]:
        return self.filter({{name_cc}}({{primaries.begin}}{{primary.name_pc}}, {{primaries.end}}{{others.begin}}None, {{others.end}}), table_info_data['{{name_pc}}'], order_by=order_by)

    def search_{{name_pc}}(self, {{primaries.begin}}{{primary.name_pc}}: Optional[{{primary.type}}] = None, {{primaries.end}}{{others.begin}}{{other.name_pc}}: Optional[{{other.type}}] = None, {{others.end}}order_by: Optional[str] = None) -> List[{{name_cc}}]:
        return self.search({{name_cc}}({{primaries.begin}}{{primary.name_pc}}, {{primaries.end}}{{others.begin}}{{other.name_pc}}, {{others.end}}), table_info_data['{{name_pc}}'], order_by=order_by)

    def set_{{name_pc}}(self, {{name_pc}}: {{name_cc}}) -> None:
        return self.set({{name_pc}}, table_info_data['{{name_pc}}'])

    def get_all_{{name_pc}}s(self, order_by: Optional[str] = None) -> List[{{name_cc}}]:
        return self.get_all(table_info_data['{{name_pc}}'], order_by)

    def remove_{{name_pc}}(self, {{name_pc}}: {{name_cc}}) -> None:
        return self.remove({{name_pc}}, table_info_data['{{name_pc}}'])
    {{tables.end}}
