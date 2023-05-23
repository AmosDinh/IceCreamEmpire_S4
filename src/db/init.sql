-- currently used version under construction
DROP TABLE IF EXISTS IceCreamVendors CASCADE;
DROP TABLE IF EXISTS Neighborhoods CASCADE;
DROP TABLE IF EXISTS Vehicles CASCADE;
DROP TABLE IF EXISTS Tours CASCADE;
DROP TABLE IF EXISTS Flavors CASCADE;
DROP TABLE IF EXISTS Contents CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS OrderDetails CASCADE;
DROP TABLE IF EXISTS Warehouses CASCADE;
DROP TABLE IF EXISTS WarehouseStoresFlavors CASCADE;
DROP TABLE IF EXISTS VehicleStoresFlavors CASCADE;

-- Schema
CREATE TABLE IceCreamVendors (
    vendor_id SERIAL,
    forename VARCHAR(32) NOT NULL,
    lastname VARCHAR(32) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (vendor_id)
);
CREATE TABLE Neighborhoods (
    Neighborhood_id SERIAL,
    name VARCHAR(32) NOT NULL,
    distance_to_headquarter_km DECIMAL(10, 3) NOT NULL,
    area_sqkm DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (Neighborhood_id)
);
CREATE TABLE Vehicles (
    vehicle_id SERIAL,
    type VARCHAR(32) NOT NULL,
    storage_capacity INT NOT NULL,
    -- measured in scoops
    PRIMARY KEY (vehicle_id)
);
CREATE TABLE Tours (
    tours_id SERIAL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    -- it is possible to keep a Tours even when the operating vendor, Vehicles or Neighborhoods is deleted
    vendor_id INT,
    vehicle_id INT,
    Neighborhood_id INT,
    PRIMARY KEY (tours_id),
    FOREIGN KEY (vendor_id) REFERENCES IceCreamVendors (vendor_id) ON DELETE
    SET NULL,
        FOREIGN KEY (vehicle_id) REFERENCES Vehicles (vehicle_id) ON DELETE
    SET NULL,
        FOREIGN KEY (Neighborhood_id) REFERENCES Neighborhoods (Neighborhood_id) ON DELETE
    SET NULL
);
-- TODO
CREATE TABLE Flavors (
    flavor_id SERIAL,
    name VARCHAR(32) NOT NULL,
    base_price_per_scoop DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (flavor_id)
);
CREATE TABLE Contents (
    flavor_id SERIAL,
    calories INT NOT NULL,
    basis VARCHAR(32) NOT NULL,
    isvegan BOOLEAN GENERATED ALWAYS AS (
        CASE
            WHEN basis = 'milk' THEN false
            ELSE true
        END
    ) STORED,
    FOREIGN KEY (flavor_id) REFERENCES Flavors (flavor_id) ON DELETE CASCADE,
    PRIMARY KEY (flavor_id)
);
CREATE TABLE Orders (
    order_id SERIAL,
    tours_id INT NOT NULL,
    order_datetime TIMESTAMP NOT NULL,
    payment_type VARCHAR(32) NOT NULL,
    FOREIGN KEY (tours_id) REFERENCES Tours (tours_id),
    PRIMARY KEY (order_id)
);
CREATE TABLE OrderDetails (
    order_id SERIAL,
    flavor_id SERIAL,
    amount SERIAL,
    --scoops
    discount SERIAL,
    -- in %
    FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    FOREIGN KEY (flavor_id) REFERENCES Flavors (flavor_id),
     PRIMARY KEY (order_id, flavor_id)
);
CREATE TABLE Warehouses (
   warehouse_id SERIAL,
   address VARCHAR(30),
   capacity DECIMAL(10, 2),
   PRIMARY KEY (warehouse_id)
);
CREATE TABLE WarehouseStoresFlavors (
   warehouse_id SERIAL ,
   flavor_id SERIAL ,
   amount INT NOT NULL ,
   FOREIGN KEY (warehouse_id) REFERENCES Warehouses (warehouse_id) ON DELETE CASCADE ,
   FOREIGN KEY (flavor_id) REFERENCES Flavors(flavor_id) ON DELETE CASCADE ,
   PRIMARY KEY (warehouse_id, flavor_id)
);
CREATE TABLE VehicleStoresFlavors (
   vehicle_id SERIAL ,
   flavor_id SERIAL ,
   amount INT NOT NULL ,
   -- scoops
   FOREIGN KEY(vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE CASCADE ,
   FOREIGN KEY(flavor_id) REFERENCES Flavors(flavor_id) ON DELETE CASCADE ,
   PRIMARY KEY(vehicle_id, flavor_id)
);

-- views
-- normal view
-- lists all flavors and their current stock (combination of stock in vehicles and in warehouses)
CREATE VIEW Stock(id, name, amount)
AS
WITH warehouse_stock AS (
	SELECT SUM(amount) as amt, flavor_id FROM WarehouseStoresFlavors GROUP BY flavor_id
),
vehicle_stock AS (
	SELECT SUM(amount) as amt, flavor_id FROM VehicleStoresFlavors GROUP BY flavor_id
)
SELECT f.flavor_id, f.name, (w.amt+v.amt) as flavor_stock  
    FROM vehicle_stock v 
    INNER JOIN warehouse_stock w 
        ON v.flavor_id = w.flavor_id 
    INNER JOIN flavors f 
        on v.flavor_id = f.flavor_id;

-- materialized view
-- show how many ice cream each vendor has sold in total (sum of all orderdetails)
CREATE MATERIALIZED VIEW VendorPerformance
AS
SELECT v.vendor_id, v.forename, v.lastname, SUM(od.amount) as total_sales
    FROM IceCreamVendors v
    INNER JOIN Tours t ON v.vendor_id = t.vendor_id
    INNER JOIN Orders o ON t.tours_id = o.tours_id
    INNER JOIN OrderDetails od ON o.order_id = od.order_id
    GROUP BY v.vendor_id, v.forename, v.lastname
ORDER BY total_sales DESC;

-- populate
INSERT INTO IceCreamVendors (forename, lastname, salary)
VALUES ('John', 'Doe', 3000.00),
    ('Jane', 'Doe', 3500.00),
    ('Bob', 'Smith', 3200.00);
INSERT INTO Neighborhoods (
        name,
        distance_to_headquarter_km,
        area_sqkm
    )
VALUES ('Downtown', 5.0, 10.0),
    ('Uptown', 10.0, 15.0),
    ('Midtown', 7.5, 12.5);
INSERT INTO Vehicles (type, storage_capacity)
VALUES ('Truck', 1000),
    ('Van', 800),
    ('Car', 600);

INSERT INTO Tours (
        start_datetime,
        end_datetime,
        vendor_id,
        vehicle_id,
        Neighborhood_id
    )
VALUES 
    ('2023-05-11 13:00:00', '2023-05-11 17:00:00', 3, 2, 2), 
    ('2023-05-13 15:00:00', '2023-05-13 21:00:00', 1, 2, 1), 
    ('2023-06-11 16:00:00', '2023-06-11 23:00:00', 2, 3, 3), 
    ('2023-07-11 17:00:00', '2023-07-11 21:00:00', 1, 1, 2);
    

INSERT INTO Flavors (name, base_price_per_scoop)
VALUES ('Vanilla', 1.00),
    ('Chocolate', 1.50),
    ('Strawberry', 1.25);
INSERT INTO Contents (calories, basis)
VALUES (200, 'milk'),
    (250, 'milk'),
    (225, 'water');
INSERT INTO Orders (tours_id, order_datetime, payment_type)
VALUES (1, '2023-05-10 12:30:00', 'cash'),
    (2, '2023-05-10 13:00:00', 'credit'),
    (3, '2023-05-11 13:30:00', 'cash'),
    (4, '2023-05-11 13:30:00', 'cash');
   

INSERT INTO OrderDetails (order_id, flavor_id, amount, discount)
VALUES (1, 1, 2, 0.00),
    (1, 2, 1, 0.30),
    (2, 3, 3, 0.00),
     (2, 1, 4, 0.00),
    (2, 2, 3, 0.15),
     (3, 2, 1, 0.00),
    (3, 3, 3, 0.00),
     (1, 3, 1, 0.1),
    (3, 1, 3, 0.00),
    (4, 1, 3, 0.00);


INSERT INTO Warehouses (warehouse_id, address,capacity)
VALUES (1, '123 Main St,Palo Alto',1000),
       (2, '456 Elm St,Palo Alto',1500),
       (3, '789 Oak St,Palo Alto',1200);
       
INSERT INTO WarehouseStoresFlavors(warehouse_id ,flavor_id ,amount)
VALUES(1 ,1 ,100),
      (1 ,2 ,200),
      (2 ,3 ,300),
      (3 ,1 ,150),
      (3 ,2 ,250);
      
INSERT INTO VehicleStoresFlavors(vehicle_id ,flavor_id ,amount)
VALUES(2 ,1 ,100),
      (2 ,2 ,200),
      (3 ,3 ,300),
      (1 ,1 ,150),
      (1 ,2 ,250);
