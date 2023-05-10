INSERT INTO IceCreamVendors (vendor_id, forename, lastname, salary) VALUES
(1, 'John', 'Doe', 3000.00),
(2, 'Jane', 'Doe', 3500.00),
(3, 'Bob', 'Smith', 3200.00);

INSERT INTO Neighborhoods (Neighborhoods_id, name, distance_to_headquarter_km, area_sqkm) VALUES
(1, 'Downtown', 5.0, 10.0),
(2, 'Uptown', 10.0, 15.0),
(3, 'Midtown', 7.5, 12.5);

INSERT INTO Vehicles (Vehicles_id, type, storage_capacity) VALUES
(1, 'Truck', 1000),
(2, 'Van', 800),
(3, 'Car', 600);

INSERT INTO Tours (Tours_id, start_datetime, end_datetime, vendor_id, Vehicles_id, Neighborhoods_id) VALUES
(1, '2023-05-10 12:00:00', '2023-05-10 16:00:00', 1, 1, 1),
(2, '2023-05-11 13:00:00', '2023-05-11 17:00:00', 2, 2, 2);

INSERT INTO Flavors (flavors_id, name, base_price_per_scoop) VALUES
(1, 'Vanilla', 1.00),
(2, 'Chocolate', 1.50),
(3, 'Strawberry', 1.25);

INSERT INTO Contents (flavors_id, calories, basis) VALUES
(1, 200, 'milk'),
(2, 250, 'milk'),
(3, 225, 'water');

INSERT INTO Orders (order_id, Tours_id, order_datetime, payment_type) VALUES
(1, 1, '2023-05-10 12:30:00', 'cash'),
(2, 1, '2023-05-10 13:00:00', 'credit'),
(3, 2, '2023-05-11 13:30:00', 'cash');

INSERT INTO OrderDetails (order_id, flavors_id, amount, price, discount) VALUES
(1, 1, 2, 2.00, 0.00),
(1, 2, 1, 1.50, 0.00),
(2, 3, 3, 3.75,0.00);


INSERT INTO Warehouses (warehouse_id, address, capacity) VALUES
(1, '123 Main St', 1000.00),
(2, '456 Elm St', 1500.00),
(3, '789 Oak St', 1200.00);

INSERT INTO WarehouseStoresFlavors (warehouse_id, flavors_id, amount) VALUES
(1, 1, 100),
(1, 2, 200),
(2, 3, 300),
(3, 1, 150),
(3, 2, 250);