class Base:
    CREATE='''
    CREATE TABLE asistencia(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMBRES TEXT,
        APELLIDO_PATERNO TEXT,
        APELLIDO_MATERNO TEXT,
        DNI NUMBER,
        GENERO TEXT,
        ESTADO_CIVIL TEXT,
        FECHA_HORA PRIMARY KEY AUTOINCREMENT)
        '''
        
    
    DELETE_TABLE="DROP TABLE asistencia"
    
    INSERT="INSERT INTO  asistencia VALUES(NULL,?,?,?,?,?,?,?)"
    
    SELECT="SELECT * FROM asistencia"
    
    UPDATE="UPDATE asistencia SET NOMBRES=?, APELLIDO_PATERNO=?, APELLIDO_MATERNO=?, DNI=?, GENERO=?, ESTADO_CIVIL=?, FECHA_HORA=? WHERE ID="
    
    DELETE="DELETE FROM asistencia WHERE ID="
    
    BUSCAR="SELECT *FROM asistencia WHERE DNI LIKE '%' || ? || '%'"
    