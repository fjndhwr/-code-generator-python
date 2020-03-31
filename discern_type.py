map = {"varchar": "String", "char": "String", "text": "String", "longtext": "String", "tinytext": "String",
       "int": "Integer", "integer": "Integer", "bigint": "Long", "smallint": "Integer", "tinyint": "Integer",
       "bit": "Integer", "decimal": "java.math.BigDecimal", "date": "Date", "datetime": "Date",
       "timestamp": "Date", "float": "Float", "double": "Double"}


def discern_type(type):
    return map[type]

