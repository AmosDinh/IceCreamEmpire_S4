def init(Session): # get session from icecream_model.py
    session = Session()

    # Insert data into IceCreamVendors table
    vendors = [
        IceCreamVendors(vendor_id=1, forename='John', lastname='Doe', salary=3000.00),
        IceCreamVendors(vendor_id=2, forename='Jane', lastname='Doe', salary=3500.00),
        IceCreamVendors(vendor_id=3, forename='Bob', lastname='Smith', salary=3200.00)
    ]
    session.add_all(vendors)

    neighborhoods = [
        Neighborhoods(Neighborhoods_id=1, name='Downtown', distance_to_headquarter_km=5.0, area_sqkm=10.0),
        Neighborhoods(Neighborhoods_id=2, name='Uptown', distance_to_headquarter_km=10.0, area_sqkm=15.0),
        Neighborhoods(Neighborhoods_id=3, name='Midtown', distance_to_headquarter_km=7.5, area_sqkm=12.5)
    ]
    session.add_all(neighborhoods)

    vehicles = [
        Vehicles(Vehicles_id=1, type='Truck', storage_capacity=1000),
        Vehicles(Vehicles_id=2, type='Van', storage_capacity=800),
        Vehicles(Vehicles_id=3, type='Car', storage_capacity=600)
    ]
    session.add_all(vehicles)

    tours = [
        Tours(Tours_id=1, start_datetime='2023-05-10 12:00:00', end_datetime='2023-05-10 16:00:00', vendor_id=1, Vehicles_id=1, Neighborhoods_id=1),
        Tours(Tours_id=2, start_datetime='2023-05-11 13:00:00', end_datetime='2023-05-11 17:00:00', vendor_id=2, Vehicles_id=2, Neighborhoods_id=2)
    ]
    session.add_all(tours)

    flavors = [
        Flavors(flavors_id=1, name='Vanilla', base_price_per_scoop=1.00),
        Flavors(flavors_id=2, name='Chocolate', base_price_per_scoop=1.50),
        Flavors(flavors_id=3, name='Strawberry', base_price_per_scoop=1.25)
    ]
    session.add_all(flavors)

    contents = [
        Contents(flavors_id=1, calories=200, basis='milk'),
        Contents(flavors_id=2, calories=250, basis='milk'),
        Contents(flavors_id=3, calories=225, basis='almond milk')
    ]

    session.add_all(contents)


    orders = [
        Orders(order_id=1, Tours_id=1, order_datetime='2023-05-10 12:30:00', payment_type='cash'),
        Orders(order_id=2, Tours_id=1, order_datetime='2023-05-10 13:00:00', payment_type='credit'),
        Orders(order_id=3, Tours_id=2, order_datetime='2023-05-11 13:30:00', payment_type='cash')
    ]
    session.add_all(orders)

    order_details = [
        OrderDetails(order_id=1, flavors_id=1, amount=2, price=2.00, discount=0.00),
        OrderDetails(order_id=1, flavors_id=2, amount=1, price=1.50, discount=0.00),
        OrderDetails(order_id=2, flavors_id=3, amount=3, price=3.75, discount=0.00)
    ]
    session.add_all(order_details)

    warehouses = [
        Warehouses(warehouse_id=1, address='123 Main St', capacity=1000.00),
        Warehouses(warehouse_id=2, address='456 Elm St', capacity=1500.00),
        Warehouses(warehouse_id=3, address='789 Oak St', capacity=1200.00)
    ]
    session.add_all(warehouses)

    warehouse_stores_flavors = [
        WarehouseStoresFlavors(warehouse_id=1, flavors_id=1, amount=100),
        WarehouseStoresFlavors(warehouse_id=1, flavors_id=2, amount=200),
        WarehouseStoresFlavors(warehouse_id=2, flavors_id=3, amount=300),
        WarehouseStoresFlavors(warehouse_id=3, flavors_id=1, amount=150),
        WarehouseStoresFlavors(warehouse_id=3, flavors_id=2, amount=250)
    ]
    session.add_all(warehouse_stores_flavors)

    session.commit()