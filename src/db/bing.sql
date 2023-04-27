CREATE TABLE Tour (
    id INTEGER PRIMARY KEY,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    date DATE NOT NULL,
    vendor_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    neighborhood_id INTEGER NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES Vendor(id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id),
    FOREIGN KEY (neighborhood_id) REFERENCES Neighborhood(id)
);
CREATE TABLE Vendor (
    id INTEGER PRIMARY KEY,
    forename TEXT NOT NULL,
    lastname TEXT NOT NULL,
    salary REAL NOT NULL
);
CREATE TABLE Neighborhood (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    distance REAL NOT NULL,
    area REAL NOT NULL
);
CREATE TABLE Vehicle (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    storage_capacity REAL NOT NULL
);
CREATE TABLE Flavor (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    base_price REAL NOT NULL
);
CREATE TABLE Content (
    id INTEGER PRIMARY KEY,
    flavor_id INTEGER NOT NULL,
    calories INTEGER NOT NULL,
    basis TEXT NOT NULL,
    vegan BOOLEAN NOT NULL,
    FOREIGN KEY (flavor_id) REFERENCES Flavor(id)
);
CREATE TABLE Order (
    id INTEGER PRIMARY KEY,
    tour_id INTEGER NOT NULL,
    time TIME NOT NULL,
    payment_type TEXT NOT NULL,
    FOREIGN KEY (tour_id) REFERENCES Tour(id)
);
CREATE TABLE OrderDetail (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    flavor_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    price REAL NOT NULL,
    discount REAL DEFAULT 0.0,
    FOREIGN KEY (order_id) REFERENCES `Order`(id),
    FOREIGN KEY (flavor_id) REFERENCES Flavor(id)
);
CREATE TABLE Warehouse (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    capacity REAL NOT NULL
);
CREATE TABLE WarehouseFlavor (
    warehouse_id INTEGER NOT NULL,
    flavor_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    PRIMARY KEY (warehouse_id, flavor_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(id),
    FOREIGN KEY (flavor_id) REFERENCES Flavor(id)
);