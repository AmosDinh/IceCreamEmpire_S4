-- Retrieve the total sales revenue for each ice cream flavor:
SELECT F.name AS flavor_name,
    SUM(OD.amount * F.base_price_per_scoop * (1 - OD.discount)) AS total_revenue
FROM Flavors F
    INNER JOIN OrderDetails OD ON F.flavor_id = OD.flavor_id
GROUP BY F.name
ORDER BY total_revenue DESC;

--Find the best-selling ice cream flavors based on the total quantity sold:
SELECT F.name AS flavor_name,
    SUM(OD.amount) AS total_quantity_sold
FROM Flavors F
    INNER JOIN OrderDetails OD ON F.flavor_id = OD.flavor_id
GROUP BY F.name
ORDER BY total_quantity_sold DESC
LIMIT 5;

--Identify the neighborhoods with the highest average order amount
SELECT N.name AS neighborhood_name,
    AVG(OD.amount * FL.base_price_per_scoop * (1 - OD.discount)) AS average_order_amount_discounted
FROM Neighborhoods N
    INNER JOIN Tours T ON N.Neighborhood_id = T.Neighborhood_id
    INNER JOIN Orders O ON T.tours_id = O.tours_id
    INNER JOIN OrderDetails OD ON O.order_id = OD.order_id
    INNER JOIN Flavors FL ON OD.flavor_id = FL.flavor_id
GROUP BY N.name
ORDER BY average_order_amount_discounted DESC
LIMIT 3;

-- Get current stored inventory per vehicle as a percentage of its capacity:
-- see if current warehouse inventory is sufficient to fill all vehicles
