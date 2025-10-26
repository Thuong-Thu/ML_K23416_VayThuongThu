from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.model.employee import Employee
ec =EmployeeConnector()
ec.connect()
emp = Employee()
emp.EmployeeCode = 'EMP888'
emp.Name = 'Doremon'
emp.Phone = '113'
emp.Email = 'doremon@yahoo.com'
emp.Password = '456'
emp.IsDeleted = 0

result = ec.insert_one_employee(emp)
if result>0:
    print("chuc mung ba nha, da them thanh cong")
else:
    print("that dang thuong")