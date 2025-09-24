#SELECT * FROM sakila.customer;
#select * from customer where store_id=2


SELECT 
    c.customer_id      AS CustomerID,
    CONCAT(c.first_name, ' ', c.last_name) AS Name,
    COUNT(r.rental_id) AS NumberOfRental
FROM customer c
JOIN rental r 
  ON r.customer_id = c.customer_id
GROUP BY c.customer_id, Name
ORDER BY NumberOfRental DESC;