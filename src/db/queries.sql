-- 1 Retrieve the total sales revenue for each ice cream flavor:
SELECT F.name AS flavor_name,
    SUM(OD.amount * F.base_price_per_scoop * (1 - OD.discount)) AS total_revenue
FROM Flavors F
    INNER JOIN OrderDetails OD ON F.flavor_id = OD.flavor_id
GROUP BY F.name
ORDER BY total_revenue DESC;


-- 2 Compare total revenue for each payment type:
SELECT o.payment_type, SUM(od.amount * f.base_price_per_scoop * (1 - od.discount)) as total_sales
    FROM Orders o
    INNER JOIN OrderDetails od ON o.order_id = od.order_id
    INNER JOIN Flavors f ON od.flavor_id = f.flavor_id
GROUP BY o.payment_type;

--3 Identify the neighborhoods with the highest average order amount
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

-- 4 total sales per neighborhood and flavor
SELECT f.name as flavor_name, n.name as neighborhood_name, SUM(od.amount) as total_sales
    FROM Flavors f
        INNER JOIN OrderDetails od ON f.flavor_id = od.flavor_id
        INNER JOIN Orders o ON od.order_id = o.order_id
        INNER JOIN Tours t ON o.tours_id = t.tours_id
        INNER JOIN Neighborhoods n ON t.Neighborhood_id = n.Neighborhood_id
GROUP BY flavor_name, neighborhood_name
ORDER BY flavor_name ASC, neighborhood_name ASC

-- 5 Average sales per tour duration
SELECT DATE_PART('hour', t.end_datetime - t.start_datetime) as tour_duration_hours, AVG(od.amount) as average_sales
FROM IceCreamVendors v
INNER JOIN Tours t ON v.vendor_id = t.vendor_id
INNER JOIN Orders o ON t.tours_id = o.tours_id
INNER JOIN OrderDetails od ON o.order_id = od.order_id
GROUP BY tour_duration_hours;

-- 6 Get flavors not sold for each tour
SELECT t.tours_id as tour_id, f.name as flavor_name
	FROM Tours t
	CROSS JOIN Flavors f
EXCEPT
SELECT o.tours_id, f.name
	FROM Flavors f
		INNER JOIN OrderDetails od ON f.flavor_id = od.flavor_id
		INNER JOIN Orders o ON od.order_id = o.order_id
ORDER BY tour_id;

-- 7 get flavors with vegan basis and calories < 230 and the warehouses which store them
SELECT w.address, fs.name, fs.flavor_id, wsf.amt as amount
FROM 
(SELECT warehouse_id, flavor_id, amount amt FROM WarehouseStoresFlavors  WHERE flavor_id IN
	(SELECT f.flavor_id
		FROM Flavors f INNER JOIN Contents c ON f.flavor_id = c.flavor_id 
		WHERE c.isvegan AND c.calories < 230
	) 
 ) as wsf
 INNER JOIN Warehouses w ON wsf.warehouse_id = w.warehouse_id 
	INNER JOIN Flavors fs ON wsf.flavor_id = fs.flavor_id
ORDER BY amount DESC;
 

