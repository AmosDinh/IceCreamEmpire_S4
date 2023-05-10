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


CREATE TABLE IceCreamVendors (
    vendor_id INT NOT NULL, 
    forename VARCHAR(32)NOT NULL,
    lastname VARCHAR(32)NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (vendor_id)
);
CREATE TABLE Neighborhoods (
    Neighborhoods_id INT NOT NULL,
    name VARCHAR(32)NOT NULL,
    distance_to_headquarter_km DECIMAL(10, 3) NOT NULL,
    area_sqkm DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (Neighborhoods_id)
);
CREATE TABLE Vehicles (
    Vehicles_id INT NOT NULL,
    type VARCHAR(32)NOT NULL,
    storage_capacity INT NOT NULL, -- measured in scoops
    PRIMARY KEY (Vehicles_id)
);
CREATE TABLE  Tours (
    Tours_id INT NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    -- it is possible to keep a Tours even when the operating vendor, Vehicles or Neighborhoods is deleted
    vendor_id INT,
    Vehicles_id INT,
    Neighborhoods_id INT,
    PRIMARY KEY (Tours_id),
    FOREIGN KEY (vendor_id) REFERENCES IceCreamVendors (vendor_id) ON DELETE
    SET NULL,
        FOREIGN KEY (Vehicles_id) REFERENCES Vehicles (Vehicles_id) ON DELETE
    SET NULL,
        FOREIGN KEY (Neighborhoods_id) REFERENCES Neighborhoods (Neighborhoods_id) ON DELETE
    SET NULL
);
-- TODO
CREATE TABLE  Flavors (
    flavors_id INT NOT NULL,
    name VARCHAR(32) NOT NULL,
    base_price_per_scoop DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (flavors_id)
);
CREATE TABLE Contents (
    flavors_id INT,
    calories INT NOT NULL,
    basis VARCHAR(32) NOT NULL,
    isvegan BOOLEAN GENERATED ALWAYS AS (
        CASE
            WHEN basis = 'milk' THEN false
            ELSE true
        END
    ) STORED,
    FOREIGN KEY (flavors_id) REFERENCES Flavors (flavors_id) ON DELETE CASCADE,
    PRIMARY KEY (flavors_id)
);

CREATE TABLE  Orders (
    order_id INT NOT NULL,
    Tours_id INT NOT NULL,
    order_datetime TIMESTAMP NOT NULL,
    payment_type VARCHAR(32) NOT NULL,
    FOREIGN KEY (Tours_id) REFERENCES Tours (Tours_id),
    PRIMARY KEY (order_id)
);

CREATE TABLE  OrderDetails (
    order_id INT,
    flavors_id INT,
    amount INT,
    price DECIMAL(10, 2),
    discount DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    FOREIGN KEY (flavors_id) REFERENCES Flavors (flavors_id),
    PRIMARY KEY (order_id, flavors_id)
);
CREATE TABLE  Warehouses (
    warehouse_id INT PRIMARY KEY,
    address VARCHAR(30),
    capacity DECIMAL(10, 2)
);
CREATE TABLE  WarehouseStoresFlavors (
    warehouse_id INT,
    flavors_id INT,
    amount INT NOT NULL,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses (warehouse_id),
    FOREIGN KEY (flavors_id) REFERENCES Flavors (flavors_id),
    PRIMARY KEY (warehouse_id, flavors_id)
   
);


-- populate

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