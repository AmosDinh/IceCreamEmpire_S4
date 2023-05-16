from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, DECIMAL, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased
Base = declarative_base()

class IceCreamVendors(Base):
    __tablename__ = 'IceCreamVendors'
    vendor_id = Column(Integer, primary_key=True)
    forename = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    salary = Column(DECIMAL(10, 2), nullable=False)

class Neighborhoods(Base):
    __tablename__ = 'Neighborhoods'
    Neighborhoods_id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    distance_to_headquarter_km = Column(DECIMAL(10, 3), nullable=False)
    area_sqkm = Column(DECIMAL(10, 2), nullable=False)

class Vehicles(Base):
    __tablename__ = 'Vehicles'
    Vehicles_id = Column(Integer, primary_key=True)
    type = Column(String(32), nullable=False)
    storage_capacity = Column(Integer, nullable=False)

class Tours(Base):
    __tablename__ = 'Tours'
    Tours_id = Column(Integer, primary_key=True)
    start_datetime = Column(TIMESTAMP, nullable=False)
    end_datetime = Column(TIMESTAMP, nullable=False)
    vendor_id = Column(Integer, ForeignKey('IceCreamVendors.vendor_id', ondelete='SET NULL'))
    Vehicles_id = Column(Integer, ForeignKey('Vehicles.Vehicles_id', ondelete='SET NULL'))
    Neighborhoods_id = Column(Integer, ForeignKey('Neighborhoods.Neighborhoods_id', ondelete='SET NULL'))

class Flavors(Base):
    __tablename__ = 'Flavors'
    flavors_id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    base_price_per_scoop = Column(DECIMAL(10, 2), nullable=False)

class Contents(Base):
    __tablename__ = 'Contents'
    flavors_id = Column(Integer, ForeignKey('Flavors.flavors_id', ondelete='CASCADE'), primary_key=True)
    calories = Column(Integer, nullable=False)
    basis = Column(String(32), nullable=False)
    isvegan = Column(Boolean)

class Orders(Base):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True)
    Tours_id = Column(Integer, ForeignKey('Tours.Tours_id'), nullable=False)
    order_datetime = Column(TIMESTAMP, nullable=False)
    payment_type = Column(String(32), nullable=False)

class OrderDetails(Base):
    __tablename__ = 'OrderDetails'
    order_id = Column(Integer, ForeignKey('Orders.order_id'), primary_key=True)
    flavors_id=Column(Integer, ForeignKey('Flavors.flavors_id'), primary_key=True)
    amount=Column(Integer)
    price=Column(DECIMAL(10, 2))
    discount=Column(DECIMAL(10, 2))

class Warehouses(Base):
   __tablename__='Warehouses'
   warehouse_id=Column(Integer ,primary_key=True )
   address=Column(String(30))
   capacity=Column(DECIMAL(10 ,2))

class WarehouseStoresFlavors(Base):
   __tablename__='WarehouseStoresFlavors'
   warehouse_id=Column(Integer ,ForeignKey('Warehouses.warehouse_id') ,primary_key=True )
   flavors_id=Column(Integer ,ForeignKey('Flavors.flavors_id') ,primary_key=True )
   amount=Column(Integer ,nullable=False )

# postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@<db_container_name>:<port>/<POSTGRES-DB>
# engine = create_engine(
    # 'postgresql://postgres:projectsmoothies@database:5432/postgres', echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)



# session = Session()
# init db
# sql_statement = open("./db/init.sql", "r").read()
# engine.execute(sql_statement)


