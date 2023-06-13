import streamlit as st
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time


def crudtour(db):
    engine = db.engine
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Get the required tables

    print('Base.classes.keys():', Base.classes.keys())
    Tours = Base.classes.tours
    icecreamvendors = Base.classes.icecreamvendors
    vehicles = Base.classes.vehicles
    neighborhoods = Base.classes.neighborhoods
    session = sessionmaker(bind=engine)()


    # Create a new tour
    st.header("Create a New Tour")
    vendors = session.query(icecreamvendors).all()
    vehicles = session.query(vehicles).all()
    neighborhoods = session.query(neighborhoods).all()

    vendor_options = {v.forename + " " + v.lastname: v.vendor_id for v in vendors}
    vehicle_options = {v.type: v.vehicle_id for v in vehicles}
    neighborhood_options = {n.name: n.neighborhood_id for n in neighborhoods}

    selected_vendor = st.selectbox("Select Vendor", options=list(vendor_options.keys()))
    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()))
    selected_neighborhood = st.selectbox("Select Neighborhood", options=list(neighborhood_options.keys()))

    start_datetime = st.date_input("Select Start Date")
    start_datetime_hours = st.time_input("Select a Start time")
    start_datetime = datetime.combine(start_datetime, start_datetime_hours)

    end_datetime = st.date_input("Select End Date")
    end_datetime_hours = st.time_input("Select a End time")
    end_datetime = datetime.combine(end_datetime, end_datetime_hours)


    if st.button("Create Tour"):
        new_tour = Tours(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            vendor_id=vendor_options[selected_vendor],
            vehicle_id=vehicle_options[selected_vehicle],
            neighborhood_id=neighborhood_options[selected_neighborhood],
        )
        session.add(new_tour)
        session.commit()
        st.success("Tour created successfully!")
        time.sleep(1)
        st.experimental_rerun()

    # Update or delete a tour
    st.header("Update or Delete a Tour")
    tours = session.query(Tours).all()

    if not tours:
        st.warning("No tours found.")
    else:
        tour_options = {f"Tour {t.tours_id} - {t.start_datetime}": t.tours_id for t in tours}
        selected_tour = st.selectbox("Select Tour", options=list(tour_options.keys()))

        tour = session.query(Tours).get(tour_options[selected_tour])

        new_vendor = st.selectbox(
            "Select New Vendor", options=list(vendor_options.keys()), index=list(vendor_options.values()).index(tour.vendor_id)
        )
        new_vehicle = st.selectbox(
            "Select New Vehicle", options=list(vehicle_options.keys()), index=list(vehicle_options.values()).index(tour.vehicle_id)
        )
        new_neighborhood = st.selectbox(
            "Select New Neighborhood",
            options=list(neighborhood_options.keys()),
            index=list(neighborhood_options.values()).index(tour.neighborhood_id),
        )
        new_start_datetime = st.date_input("Select New Start Date", value=tour.start_datetime)
        new_start_selected_time = st.time_input("Select a new Start time", value=tour.start_datetime)
        new_start_datetime = datetime.combine(new_start_datetime, new_start_selected_time)
        
        new_end_datetime = st.date_input("Select New End Date", value=tour.end_datetime)
        new_end_selected_time = st.time_input("Select a new End time", value=tour.start_datetime)
        new_end_datetime = datetime.combine(new_end_datetime, new_end_selected_time)

        if st.button("Update Tour"):
            tour.vendor_id = vendor_options[new_vendor]
            tour.vehicle_id = vehicle_options[new_vehicle]
            tour.neighborhood_id = neighborhood_options[new_neighborhood]
            tour.start_datetime = new_start_datetime
            tour.end_datetime = new_end_datetime
            session.commit()
            st.success("Tour updated successfully!")
            time.sleep(1)
            st.experimental_rerun()

        if st.button("Delete Tour"):
            session.delete(tour)
            session.commit()
            st.success("Tour deleted successfully!")
            time.sleep(1)
            st.experimental_rerun()