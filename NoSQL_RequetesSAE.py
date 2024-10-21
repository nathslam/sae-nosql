# Importation des modules utilisés
import sqlite3
import pandas as pd

# Création de la connexion
conn = sqlite3.connect("ClassicModel.sqlite")

# 1. Lister les clients n'ayant jamais effectué de commande
query_1 = """
SELECT customerName
FROM Customers c
LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
WHERE o.customerNumber IS NULL;
"""
result_1 = pd.read_sql_query(query_1, conn)
print("Clients n'ayant jamais effectué de commande:")
print(result_1)

# 2. Lister chaque employé avec le nombre de clients et le montant total de leurs commandes
query_2 = """
SELECT e.employeeNumber, e.firstName || ' ' || e.lastName AS employeeName, 
       COUNT(DISTINCT c.customerNumber) AS totalClients, 
       SUM(od.priceEach * od.quantityOrdered) AS totalAmount
FROM Employees e
JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN Orders o ON c.customerNumber = o.customerNumber
JOIN OrderDetails od ON o.orderNumber = od.orderNumber
GROUP BY e.employeeNumber;
"""
result_2 = pd.read_sql_query(query_2, conn)
print("Nombre de clients et montant total des commandes par employé:")
print(result_2)

# 3. Lister chaque bureau avec le nombre de clients et total de leurs commandes par pays
query_3 = """
SELECT o.officeCode, o.city, COUNT(DISTINCT c.customerNumber) AS totalClients, 
       SUM(od.priceEach * od.quantityOrdered) AS totalAmount, 
       COUNT(DISTINCT c.country) AS differentCountries
FROM Offices o
JOIN Employees e ON o.officeCode = e.officeCode
JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN Orders o2 ON c.customerNumber = o2.customerNumber
JOIN OrderDetails od ON o2.orderNumber = od.orderNumber
GROUP BY o.officeCode;
"""
result_3 = pd.read_sql_query(query_3, conn)
print("Nombre de clients et total des commandes par bureau:")
print(result_3)

# 4. Lister chaque produit avec le nombre de commandes, le total commandé et le nombre de clients différents
query_4 = """
SELECT p.productCode, p.productName, COUNT(DISTINCT od.orderNumber) AS totalOrders, 
       SUM(od.quantityOrdered) AS totalQuantity, COUNT(DISTINCT o.customerNumber) AS totalClients
FROM Products p
JOIN OrderDetails od ON p.productCode = od.productCode
JOIN Orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode;
"""
result_4 = pd.read_sql_query(query_4, conn)
print("Nombre de commandes, total commandé et clients différents par produit:")
print(result_4)

# 5. Tableau de commande par pays, nombre de clients et montant total
query_5 = """
SELECT c.country, COUNT(DISTINCT c.customerNumber) AS totalClients, 
       SUM(od.priceEach * od.quantityOrdered) AS totalAmount
FROM Customers c
JOIN Orders o ON c.customerNumber = o.customerNumber
JOIN OrderDetails od ON o.orderNumber = od.orderNumber
GROUP BY c.country;
"""
result_5 = pd.read_sql_query(query_5, conn)
print("Commande par pays:")
print(result_5)

# 6. Tableau croisé des produits et pays avec le montant total payé par client
query_6 = """
SELECT c.country, p.productName, SUM(od.priceEach * od.quantityOrdered) AS totalAmount
FROM Customers c
JOIN Orders o ON c.customerNumber = o.customerNumber
JOIN OrderDetails od ON o.orderNumber = od.orderNumber
JOIN Products p ON od.productCode = p.productCode
GROUP BY c.country, p.productName;
"""
result_6 = pd.read_sql_query(query_6, conn)
print("Tableau croisé dynamique: produits et pays")
print(result_6)

# 7. Donner les 10 produits pour lesquels la marge est la plus importante (buyPrice vs priceEach)
query_7 = """
SELECT p.productName, p.buyPrice, AVG(od.priceEach) AS avgPriceSold, 
       (AVG(od.priceEach) - p.buyPrice) AS margin
FROM Products p
JOIN OrderDetails od ON p.productCode = od.productCode
GROUP BY p.productCode
ORDER BY margin DESC
LIMIT 10;
"""
result_7 = pd.read_sql_query(query_7, conn)
print("Top 10 produits avec la marge la plus importante:")
print(result_7)

# 8. Lister les produits (avec nom et code du client) qui n'ont jamais été vendus
query_8 = """
SELECT p.productCode, p.productName
FROM Products p
LEFT JOIN OrderDetails od ON p.productCode = od.productCode
WHERE od.productCode IS NULL;
"""
result_8 = pd.read_sql_query(query_8, conn)
print("Produits non vendus:")
print(result_8)

# 9. Comparer le prix de vente et d'achat pour les articles vendus à perte
query_9 = """
SELECT p.productName, p.buyPrice, od.priceEach
FROM Products p
JOIN OrderDetails od ON p.productCode = od.productCode
WHERE od.priceEach < p.buyPrice;
"""
result_9 = pd.read_sql_query(query_9, conn)
print("Produits vendus à perte:")
print(result_9)

# 10. Lister les clients avec le montant total de leurs achats
query_10 = """
SELECT c.customerName, SUM(od.priceEach * od.quantityOrdered) AS totalSpent
FROM Customers c
JOIN Orders o ON c.customerNumber = o.customerNumber
JOIN OrderDetails od ON o.orderNumber = od.orderNumber
GROUP BY c.customerNumber;
"""
result_10 = pd.read_sql_query(query_10, conn)
print("Clients et montant total de leurs achats:")
print(result_10)
# Fermeture de la connexion : IMPORTANT à faire dans un cadre professionnel
conn.close()
