# import psycopg2 as sql
# from recursos.constantes import *

from typing import overload


class RunQuery():
    def __init__(self):
        self._query = ""

    def select(self, table:str, columns:list=[]):
        """
        Genera una consulta SELECT en la tabla seleccionada. Si no se indican columnas, se seleccionan todas (SELECT *)
        """
        if len(columns) == 0:
            cols = "*"
        else:
            cols = ""
            for column in columns:
                cols += f"{column}, "
            cols = cols[:-2]
        self._query = f"SELECT {cols} FROM {table}"

    def insert(self):
        raise PermissionError

    def update(self):
        raise PermissionError

    def delete(self):
        raise PermissionError

    def inner_join(self):
        raise PermissionError

    def left_join(self):
        raise PermissionError
    
    def right_join(self):
        raise PermissionError
    
    def full_join(self):
        raise PermissionError
    
    def where(self, columns:list, values:list):
        """
        Filtra los resultados de la consulta.

        columns -> Lista con los nombres de las columnas a filtrar

        values  -> Lista con los valores a buscar en cada columna

        Agrega a la consulta la siguiente sintaxis: WHERE columns[n] = values[n]
        """
        if type(columns) != list:
            raise SyntaxError('columns debe ser tipo list')
        if type(values) != list:
            raise SyntaxError('values debe ser tipo list')
        if len(columns) != len(values):
            raise SyntaxError('columns y values deben contener la misma cantidad de elementos')
        if len(columns) == 0 or len(values) == 0:
            raise SyntaxError('columns y values deben contener al menos un elemento')
        if len(columns) == 1:
            if type(values[0]) == int:
                self._query += f" WHERE {columns[0]} = {values[0]}"
            elif type(values[0]) == str:
                self._query += f" WHERE {columns[0]} = '{values[0]}'"
        else:
            if type(values[0]) == int:
                self._query += f" WHERE {columns[0]} = {values[0]}"
            elif type(values[0]) == str:
                self._query += f" WHERE {columns[0]} = '{values[0]}'"
            for n in range(1, len(columns)):
                if type(values[n]) == int:
                    self._query += f" AND {columns[n]} = {values[n]}"
                elif type(values[0]) == str:
                    self._query += f" AND {columns[n]} = '{values[n]}'"

    def order_by(self, column:str):
        """
        Ordena la consulta

        column -> Cadena con el nombre de la columna por la cual se ordenará la consulta

        Agrega a la consulta la siguiente sintaxis: ORDER BY column
        """
        self._query += f" ORDER BY {column}"

    def run_query(self):
        return self._query
    




if __name__ == '__main__':
    columnas = ['pass', 'privilegios', 'activo']
    valores = ['1234', '2', 1]
    consulta = RunQuery()
    consulta.select('usuarios', ['nombre', 'apellido'])
    consulta.where(columnas, valores)
    consulta.order_by('id')
    print(consulta.run_query())
