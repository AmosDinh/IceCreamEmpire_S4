INSERT INTO IceCreamVendor (vendor_id, forename, lastname, salary) VALUES
(1, 'John', 'Doe', 3000.00),
(2, 'Jane', 'Doe', 3500.00),
(3, 'Bob', 'Smith', 3200.00);

INSERT INTO Neighborhood (neighborhood_id, name, distance_to_headquarter_km, area_sqkm) VALUES
(1, 'Downtown', 5.0, 10.0),
(2, 'Uptown', 10.0, 15.0),
(3, 'Midtown', 7.5, 12.5);

INSERT INTO Vehicle (vehicle_id, type, storage_capacity) VALUES
(1, 'Truck', 1000),
(2, 'Van', 800),
(3, 'Car', 600);

INSERT INTO Tour (tour_id, start_datetime, end_datetime, vendor_id, vehicle_id, neighborhood_id) VALUES
(1, '2023-05-10 09:00:00', '2023-05-10 17:00:00', 1, 1, 1),
(2, '2023-05-11 09:00:00', '2023-05-11 17:00:00', 2, 2, 2),
(3,'2023-05-12 09:00:00','2023-05-12 17:00:00',3 ,3 ,3);

INSERT INTO Flavor (flavor_id,name ,base_price_per_scoop ) VALUES
(1,'Vanilla' ,1.50 ),
(2,'Chocolate' ,1.75 ),
(3,'Strawberry' ,1.60 );

INSERT INTO Content (flavor_id ,calories ,basis ) VALUES
(1 ,200 ,'milk' ),
(2 ,250 ,'milk' ),
(3 ,225 ,'milk' );

INSERT INTO Order (order_id, tour_id, order_datetime, payment_type) VALUES
(1, 1, '2023-05-10 10:30:00', 'Cash'),
(2, 2, '2023-05-11 11:45:00', 'Credit Card'),
(3, 3, '2023-05-12 13:15:00', 'Debit Card');

INSERT INTO OrderDetails (order_id, flavor_id, amount, price, discount) VALUES
(1, 1, 2, 3.00, 0.50),
(2, 2, 3, 5.25, 0.75),
(3, 3, 4, 6.40, 1.00);

INSERT INTO Warehouses (warehouse_id,address,capacity) VALUES
(1,'123 Main St.',1000),
(2,'456 Elm St.',1500),
(3,'789 Oak St.',1200);

INSERT INTO WarehouseFlavorStock (warehouse_id,flavor_id,amount) VALUES
(1,1,550),
(1,2,1450),
(2,2,780),
(2,3,805),
(3,1,775),