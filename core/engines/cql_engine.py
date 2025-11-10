"""
Common Query Language (CQL) Engine
Translates CQL queries to platform-specific query languages
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class CQLEngine:
    """Universal query language engine for security platforms"""

    def __init__(self):
        self.supported_platforms = [
            'splunk', 'elastic', 'sentinel', 'qradar', 'chronicle',
            'crowdstrike', 'sentinelone', 'defender', 'carbonblack',
            'paloalto', 'cisco', 'fortinet', 'zscaler',
            'aws_security_hub', 'azure_security', 'gcp_scc',
            'okta', 'entraid', 'ping',
            'misp', 'threatconnect', 'anomali'
        ]

    def parse(self, cql_query: str) -> Dict[str, Any]:
        """Parse CQL query into AST"""
        ast = {
            'filters': [],
            'groupby': None,
            'aggregations': [],
            'conditions': [],
            'timerange': None,
            'sort': None,
            'limit': None
        }

        lines = [line.strip() for line in cql_query.strip().split('\n') if line.strip()]

        for line in lines:
            if line.startswith('#'):
                # Repository or metadata
                if '=' in line:
                    key, value = line[1:].split('=', 1)
                    ast['filters'].append({
                        'field': key.strip(),
                        'operator': '=',
                        'value': value.strip()
                    })
            elif 'groupBy' in line:
                # Group by clause
                ast['groupby'] = self._parse_groupby(line)
            elif line.startswith('sort('):
                # Sort clause
                ast['sort'] = self._parse_sort(line)
            elif '>=' in line or '<=' in line or '=' in line or '!=' in line:
                # Filter or condition
                if any(agg in line for agg in ['count', 'sum', 'avg', 'min', 'max']):
                    ast['conditions'].append(self._parse_condition(line))
                else:
                    ast['filters'].append(self._parse_filter(line))

        return ast

    def _parse_groupby(self, line: str) -> Dict[str, Any]:
        """Parse groupBy clause"""
        # Extract fields and function
        match = re.search(r'groupBy\(\[([^\]]+)\],\s*function=([^,\)]+)', line)
        if match:
            fields = [f.strip() for f in match.group(1).split(',')]
            function = match.group(2).strip()

            # Extract alias
            alias_match = re.search(r'as="([^"]+)"', line)
            alias = alias_match.group(1) if alias_match else 'result'

            return {
                'fields': fields,
                'function': function,
                'alias': alias
            }
        return None

    def _parse_filter(self, line: str) -> Dict[str, Any]:
        """Parse filter expression"""
        operators = ['>=', '<=', '!=', '=']
        for op in operators:
            if op in line:
                parts = line.split(op, 1)
                return {
                    'field': parts[0].strip(),
                    'operator': op,
                    'value': parts[1].strip()
                }
        return None

    def _parse_condition(self, line: str) -> Dict[str, Any]:
        """Parse condition expression"""
        operators = ['>=', '<=', '!=', '=']
        for op in operators:
            if op in line:
                parts = line.split(op, 1)
                return {
                    'field': parts[0].strip(),
                    'operator': op,
                    'value': parts[1].strip()
                }
        return None

    def _parse_sort(self, line: str) -> Dict[str, Any]:
        """Parse sort clause"""
        field_match = re.search(r'field=([^,\)]+)', line)
        order_match = re.search(r'order=([^,\)]+)', line)
        limit_match = re.search(r'limit=(\d+)', line)

        return {
            'field': field_match.group(1).strip() if field_match else None,
            'order': order_match.group(1).strip() if order_match else 'asc',
            'limit': int(limit_match.group(1)) if limit_match else None
        }

    def translate(self, cql_query: str, platform: str) -> str:
        """Translate CQL to platform-specific query"""
        if platform not in self.supported_platforms:
            raise ValueError(f"Unsupported platform: {platform}")

        ast = self.parse(cql_query)

        translators = {
            'splunk': self._translate_splunk,
            'elastic': self._translate_elastic,
            'sentinel': self._translate_sentinel,
            'qradar': self._translate_qradar,
            'crowdstrike': self._translate_crowdstrike,
        }

        translator = translators.get(platform, self._translate_generic)
        return translator(ast)

    def _translate_splunk(self, ast: Dict[str, Any]) -> str:
        """Translate to Splunk SPL"""
        query_parts = []

        # Base search
        filters = []
        for f in ast['filters']:
            if f['operator'] == '=':
                filters.append(f'{f["field"]}={f["value"]}')
            else:
                filters.append(f'{f["field"]}{f["operator"]}{f["value"]}')

        if filters:
            query_parts.append('search ' + ' '.join(filters))

        # Group by and stats
        if ast['groupby']:
            gb = ast['groupby']
            fields_str = ', '.join(gb['fields'])
            func = gb['function'].replace('count', 'count').replace('(as=', ' AS ')
            query_parts.append(f'| stats {func} by {fields_str}')

        # Conditions (where clause after stats)
        for cond in ast['conditions']:
            query_parts.append(f'| where {cond["field"]} {cond["operator"]} {cond["value"]}')

        # Sort
        if ast['sort']:
            sort_order = '-' if ast['sort']['order'] == 'desc' else '+'
            query_parts.append(f'| sort {sort_order}{ast["sort"]["field"]}')
            if ast['sort']['limit']:
                query_parts.append(f'| head {ast["sort"]["limit"]}')

        return ' '.join(query_parts)

    def _translate_elastic(self, ast: Dict[str, Any]) -> Dict[str, Any]:
        """Translate to Elasticsearch DSL"""
        query = {
            'query': {
                'bool': {
                    'must': []
                }
            }
        }

        # Filters
        for f in ast['filters']:
            if f['operator'] == '=':
                query['query']['bool']['must'].append({
                    'term': {f['field']: f['value']}
                })
            elif f['operator'] == '>=':
                query['query']['bool']['must'].append({
                    'range': {f['field']: {'gte': f['value']}}
                })

        # Aggregations
        if ast['groupby']:
            gb = ast['groupby']
            query['aggs'] = {
                'grouped': {
                    'terms': {
                        'field': gb['fields'][0],
                        'size': 10000
                    }
                }
            }

        return query

    def _translate_sentinel(self, ast: Dict[str, Any]) -> str:
        """Translate to Azure Sentinel KQL"""
        query_parts = []

        # Table/source
        table = 'SecurityEvent'
        for f in ast['filters']:
            if f['field'] in ['event.module', 'event.dataset']:
                table = f['value'].title() + 'Events'
                break

        query_parts.append(table)

        # Filters
        filters = []
        for f in ast['filters']:
            if f['field'] not in ['event.module', 'event.dataset']:
                filters.append(f'{f["field"]} {f["operator"]} "{f["value"]}"')

        if filters:
            query_parts.append('| where ' + ' and '.join(filters))

        # Summarize (group by)
        if ast['groupby']:
            gb = ast['groupby']
            fields_str = ', '.join(gb['fields'])
            func = gb['function'].replace('count', 'count()').replace('(as=', ' ')
            query_parts.append(f'| summarize {gb["alias"]}={func} by {fields_str}')

        # Conditions
        for cond in ast['conditions']:
            query_parts.append(f'| where {cond["field"]} {cond["operator"]} {cond["value"]}')

        # Sort
        if ast['sort']:
            order = 'desc' if ast['sort']['order'] == 'desc' else 'asc'
            query_parts.append(f'| sort by {ast["sort"]["field"]} {order}')
            if ast['sort']['limit']:
                query_parts.append(f'| take {ast["sort"]["limit"]}')

        return '\n'.join(query_parts)

    def _translate_qradar(self, ast: Dict[str, Any]) -> str:
        """Translate to QRadar AQL"""
        query_parts = ['SELECT']

        # Fields
        if ast['groupby']:
            fields = ast['groupby']['fields'] + [ast['groupby']['alias']]
            query_parts.append(', '.join(fields))
        else:
            query_parts.append('*')

        query_parts.append('FROM events')

        # Where clause
        filters = []
        for f in ast['filters']:
            filters.append(f'{f["field"]} {f["operator"]} \'{f["value"]}\'')

        if filters:
            query_parts.append('WHERE ' + ' AND '.join(filters))

        # Group by
        if ast['groupby']:
            fields_str = ', '.join(ast['groupby']['fields'])
            query_parts.append(f'GROUP BY {fields_str}')

        # Having (conditions)
        if ast['conditions']:
            having = []
            for cond in ast['conditions']:
                having.append(f'{cond["field"]} {cond["operator"]} {cond["value"]}')
            query_parts.append('HAVING ' + ' AND '.join(having))

        # Order by
        if ast['sort']:
            order = 'DESC' if ast['sort']['order'] == 'desc' else 'ASC'
            query_parts.append(f'ORDER BY {ast["sort"]["field"]} {order}')

        # Limit
        if ast['sort'] and ast['sort']['limit']:
            query_parts.append(f'LIMIT {ast["sort"]["limit"]}')

        return ' '.join(query_parts)

    def _translate_crowdstrike(self, ast: Dict[str, Any]) -> str:
        """Translate to CrowdStrike query syntax"""
        filters = []
        for f in ast['filters']:
            if f['operator'] == '=':
                filters.append(f'{f["field"]}:\'{f["value"]}\'')
            else:
                filters.append(f'{f["field"]}{f["operator"]}\'{f["value"]}\'')

        return ' '.join(filters)

    def _translate_generic(self, ast: Dict[str, Any]) -> str:
        """Generic translation fallback"""
        return str(ast)

    def execute(self, cql_query: str, platform: str, connector=None) -> List[Dict[str, Any]]:
        """Execute CQL query on target platform"""
        translated_query = self.translate(cql_query, platform)

        if connector:
            return connector.execute_query(translated_query)

        # Return mock results for demo
        return [
            {'field1': 'value1', 'count': 10},
            {'field1': 'value2', 'count': 5}
        ]
