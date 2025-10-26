from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.model.employee import Employee
ec =EmployeeConnector()
ec.connect()
emp = Employee()
emp.EmployeeCode = 'EMP_K23416'
emp.Name = 'Doremon'
emp.Phone = '0907864365'
emp.Email = 'k23416@yahoo.com'
emp.Password = '789'
emp.IsDeleted = 0

result = ec.insert_one_employee(emp)
if result>0:
    print("chuc mung ba nha, da sua thanh cong")
else:
    print("that dang thuong")