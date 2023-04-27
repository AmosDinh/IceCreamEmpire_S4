CREATE TABLE IF NOT EXISTS IceCreamVendor (
    vendor_id INT PRIMARY KEY NOT NULL,
    forename VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS Neighborhood (
    neighborhood_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    distance_to_headquarter_km DECIMAL(10, 3) NOT NULL,
    area_sqkm DECIMAL(10, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS Vehicle (
    vehicle_id INT PRIMARY KEY NOT NULL,
    type VARCHAR(255) NOT NULL,
    storage_capacity INT NOT NULL -- measured in scoops
);
CREATE TABLE IF NOT EXISTS tour (
    tour_id INT PRIMARY KEY NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    date DATE NOT NULL,
    -- it is possible to keep a tour even when the operating vendor, vehicle or neighborhood is deleted
    vendor_id INT,
    vehicle_id INT,
    neighborhood_id INT,
    FOREIGN KEY (vendor_id) REFERENCES IceCreamVendor (vendor_id) ON DELETE
    SET NULL,
        FOREIGN KEY (vehicle_id) REFERENCES Vehicle (vehicle_id) ON DELETE
    SET NULL,
        FOREIGN KEY (neighborhood_id) REFERENCES Neighborhood (neighborhood_id) ON DELETE
    SET NULL
);
-- TODO
CREATE TABLE IF NOT EXISTS Flavor (
    flavor_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    base_price_per_scoop DECIMAL(10, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS Content (
    content_id INT PRIMARY KEY NOT NULL,
    flavor_id INT NOT NULL,
    calories INT NOT NULL,
    basis VARCHAR(255) NOT NULL,
    isvegan BOOLEAN AS (
        CASE
            WHEN content = 'milk' THEN false
            ELSE true
        END
    ) FOREIGN KEY (flavor_id) REFERENCES Flavor (flavor_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Order (
    order_id INT PRIMARY KEY NOT NULL,
    tour_id INT NOT NULL,
    time TIME NOT NULL,
    payment_type VARCHAR(255) NOT NULL,
    FOREIGN KEY (tour_id) REFERENCES Tours (tour_id)
);
CREATE TABLE IF NOT EXISTS OrderDetails (
    id INT PRIMARY KEY,
    order_id INT,
    flavor_id INT,
    amount INT,
    price DECIMAL(10, 2),
    discount DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders (id),
    FOREIGN KEY (flavor_id) REFERENCES Flavors (id)
);
CREATE TABLE IF NOT EXISTS Warehouses (
    id INT PRIMARY KEY,
    address VARCHAR(255),
    capacity DECIMAL(10, 2)
);
CREATE TABLE IF NOT EXISTS WarehouseFlavorStock (
    warehouse_id INT,
    flavor_id INT,
    amount INT,
    PRIMARY KEY (warehouse_id, flavor_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id),
    FOREIGN KEY (flavor_id) REFERENCES Flavors (id)
);