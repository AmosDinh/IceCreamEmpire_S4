CREATE TABLE Tour (
    tour_id INT PRIMARY KEY,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    tour_date DATE NOT NULL,
    ice_cream_vendor_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    neighborhood_id INT NOT NULL,
    FOREIGN KEY (ice_cream_vendor_id) REFERENCES IceCreamVendor(vendor_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (neighborhood_id) REFERENCES Neighborhood(neighborhood_id)
);
CREATE TABLE IceCreamVendor (
    vendor_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);
CREATE TABLE Neighborhood (
    neighborhood_id INT PRIMARY KEY,
    neighborhood_name VARCHAR(50) NOT NULL,
    distance_to_headquarter DECIMAL(10, 2) NOT NULL,
    area_covered DECIMAL(10, 2) NOT NULL
);
CREATE TABLE Vehicle (
    vehicle_id INT PRIMARY KEY,
    vehicle_type VARCHAR(50) NOT NULL,
    storage_capacity DECIMAL(10, 2) NOT NULL
);
CREATE TABLE Flavor (
    flavor_id INT PRIMARY KEY,
    flavor_name VARCHAR(50) NOT NULL,
    base_price_per_scoop DECIMAL(10, 2) NOT NULL
);
CREATE TABLE Content (
    content_id INT PRIMARY KEY,
    flavor_id INT NOT NULL,
    calories DECIMAL(10, 2) NOT NULL,
    basis VARCHAR(50) NOT NULL,
    is_vegan BOOLEAN NOT NULL,
    FOREIGN KEY (flavor_id) REFERENCES Flavor(flavor_id)
);
CREATE TABLE Warehouse (
    warehouse_id INT PRIMARY KEY,
    warehouse_address VARCHAR(255) NOT NULL,
    capacity DECIMAL(10, 2) NOT NULL
);
CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY,
    flavor_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (flavor_id) REFERENCES Flavor(flavor_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
);
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    tour_id INT NOT NULL,
    order_time DATETIME NOT NULL,
    payment_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (tour_id) REFERENCES Tour(tour_id)
);
CREATE TABLE OrderDetail (
    order_detail_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    flavor_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Order(order_id),
    FOREIGN KEY (flavor_id) REFERENCES Flavor(flavor_id)
);