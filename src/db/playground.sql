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