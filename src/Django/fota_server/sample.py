import pyodbc

print(pyodbc.drivers())
connectionQuery = "DRIVER={SQL Server}; SERVER=localhost\\TEW_SQLEXPRESS; DATABASE=FOTA;Trusted_Connection=yes;TrustServerCertificate=yes;"

conn = pyodbc.connect(connectionQuery)