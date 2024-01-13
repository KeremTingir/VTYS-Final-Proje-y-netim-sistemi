import pyodbc

server = 'TINGIR\\SQLEXPRESS'
database = 'FinalOdev'
username = ''
password = ''

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# veri tabanı bağlantı ve bağlantı kesme 
def connect_to_database():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f'Hata: {e}')
        return None, None # Bağlantı başarısız olduğunda None değerleri döndür

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

# Proje tablosuna veri ekleme 
def add_project(conn, cursor, name, start_date, end_date):
    try:
        insert_query = f"INSERT INTO Projects (ProjeAdi, BaslangicTarihi, BitisTarihi) VALUES ('{name}', '{start_date}', '{end_date}')"
        cursor.execute(insert_query)
        conn.commit()
        print(f"{name} projesi eklendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# Employees tablosuna veri ekleme
def add_employee(name, surname, position):
    conn, cursor = connect_to_database()

    try:
        insert_query = f"INSERT INTO Employees (Name, Surname, Position) VALUES ('{name}', '{surname}', '{position}')"
        cursor.execute(insert_query)
        conn.commit()
        print(f"{name} {surname} eklenen çalışan.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# Task tablosuna veri ekleme
def add_task(conn, cursor, description, start_date, end_date, project_id, employee_id, status):
    try:
        insert_query = f"INSERT INTO Tasks (Description, StartDate, EndDate, ProjectID, EmployeeID, Status) " \
                       f"VALUES ('{description}', '{start_date}', '{end_date}', {project_id}, {employee_id}, '{status}')"
        cursor.execute(insert_query)
        conn.commit()
        print(f"{description} görevi eklendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)
    
# Proje tablosundan veri silme
def delete_project(conn, cursor, project_name):
    try:
        delete_query = f"DELETE FROM Projects WHERE ProjeAdi = '{project_name}'"
        cursor.execute(delete_query)
        conn.commit()
        print(f"{project_name} projesi silindi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# Employees tablosundan veri silme
def delete_employee(employee_id):
    conn, cursor = connect_to_database()

    try:
        delete_query = f"DELETE FROM Employees WHERE ID = {employee_id}"
        cursor.execute(delete_query)
        conn.commit()
        print(f"Çalışan ID {employee_id} silindi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# Task tablosundan veri silme
def delete_task(task_id):
    conn, cursor = connect_to_database()

    try:
        delete_query = f"DELETE FROM Tasks WHERE ID = {task_id}"
        cursor.execute(delete_query)
        conn.commit()
        print(f"Görev ID {task_id} silindi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# Task status tablosundan veri silme
def delete_task_status(status_id):
    conn, cursor = connect_to_database()

    try:
        delete_query = f"DELETE FROM TaskStatus WHERE ID = {status_id}"
        cursor.execute(delete_query)
        conn.commit()
        print(f"Görev Durumu ID {status_id} silindi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)
               
# Proje tablosunu güncelleme
def update_project(conn, cursor, old_name, new_name, start_date, end_date):
    try:
        update_query = f"UPDATE Projects SET ProjeAdi = '{new_name}', BaslangicTarihi = '{start_date}', BitisTarihi = '{end_date}' WHERE ProjeAdi = '{old_name}'"
        cursor.execute(update_query)
        conn.commit()
        print(f"{old_name} projesi güncellendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# employee tablosunu güncelleme
def update_employee(employee_id, name, surname, position):
    conn, cursor = connect_to_database()

    try:
        update_query = f"UPDATE Employees SET Name = '{name}', Surname = '{surname}', Position = '{position}' WHERE ID = {employee_id}"
        cursor.execute(update_query)
        conn.commit()
        print(f"Çalışan ID {employee_id} güncellendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# task tablosunu güncelleme
def update_task(task_id, description, start_date, end_date, project_id, employee_id, status):
    conn, cursor = connect_to_database()

    try:
        update_query = f"UPDATE Tasks SET Description = '{description}', StartDate = '{start_date}', EndDate = '{end_date}', " \
                       f"ProjectID = {project_id}, EmployeeID = {employee_id}, Status = '{status}' WHERE ID = {task_id}"
        cursor.execute(update_query)
        conn.commit()
        print(f"Görev ID {task_id} güncellendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)

# task status tablosunu güncelleme
def update_task_status(status_id, status):
    conn, cursor = connect_to_database()

    try:
        update_query = f"UPDATE TaskStatus SET Status = '{status}' WHERE ID = {status_id}"
        cursor.execute(update_query)
        conn.commit()
        print(f"Görev Durumu ID {status_id} güncellendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)
           
# Proje tablosunda arama yapma
def search_project(conn, cursor, project_name):
    try:
        select_query = f"SELECT * FROM Projects WHERE ProjeAdi LIKE '%{project_name}%'"
        cursor.execute(select_query)
        projects = cursor.fetchall()

        return projects
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)
        
# Projeyi ismine göre veritabanından alıp ID'sini döndüren fonksiyon
def get_project_id(conn, cursor, project_name):
    try:
        select_query = f"SELECT ID FROM Projects WHERE ProjeAdi = '{project_name}'"
        cursor.execute(select_query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f'Hata: {e}')
        return None

# Çalışanı ismine göre veritabanından alıp ID'sini döndüren fonksiyon
def get_employee_id(conn, cursor, employee_name):
    try:
        select_query = f"SELECT ID FROM Employees WHERE Name = '{employee_name}'"
        cursor.execute(select_query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f'Hata: {e}')
        return None      
           
# Çalışanın görevlerini veritabanından alarak listeleyen fonksiyon
def get_employee_tasks(conn, cursor, employee_name):
    try:
        select_query = f"SELECT Projects.ProjeAdi, Tasks.Description AS task_name, Employees.Name AS assigned_person, Tasks.Status " \
                       f"FROM Tasks " \
                       f"JOIN Employees ON Tasks.EmployeeID = Employees.ID " \
                       f"JOIN Projects ON Tasks.ProjectID = Projects.ID " \
                       f"WHERE Employees.Name = '{employee_name}'"

        cursor.execute(select_query)
        tasks = cursor.fetchall()

        return tasks
    except Exception as e:
        print(f'Hata: {e}')
        return []
    finally:
        close_connection(conn, cursor)    
    
# Görev durumunu güncelleyen fonksiyon
def update_task_status(conn, cursor, task_id, status):
    try:
        update_query = f"UPDATE Tasks SET Status = '{status}' WHERE ID = {task_id}"
        cursor.execute(update_query)
        conn.commit()
        print(f"Görev ID {task_id} durumu güncellendi.")
    except Exception as e:
        print(f'Hata: {e}')
    finally:
        close_connection(conn, cursor)   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        