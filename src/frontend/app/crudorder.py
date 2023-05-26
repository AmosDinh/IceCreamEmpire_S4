import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import os
from datetime import datetime
import time




def crudorder(db):

    engine = db.engine
    Base = automap_base()
    Base.prepare(engine, reflect=True)


    # icecreamvendors = Base.classes.icecreamvendors
    # neighborhoods = Base.classes.neighborhoods
    # vehicles = Base.classes.vehicles
    tours = Base.classes.tours
    flavors = Base.classes.flavors
    # contents = Base.classes.contents
    orders = Base.classes.orders
    orderdetails = Base.classes.orderdetails

    session = Session(engine)

    # Streamlit frontend
    st.title("Ice Cream orders")

    # Create new order
    st.header("Create New Order")
    tours = session.query(tours).all()
    tour_options = [(t.tours_id, f"Tour {t.tours_id}: from {t.start_datetime} - {t.end_datetime}") for t in tours]
    selected_tour_id = st.selectbox("Select Tour", tour_options, format_func=lambda x: x[1])[0]

    flavors = session.query(flavors).all()

    flavor_options = {f.flavor_id: f.name for f in flavors}
    flavor_baseprices = {f.flavor_id: f.base_price_per_scoop for f in flavors}

    payment_types = ["cash", "credit"]
    selected_payment_type = st.selectbox("Payment Type", payment_types)


    order_datetime = st.date_input("Select Order Date")
    order_datetime_hours = st.time_input("Select a Order time")
    order_datetime = datetime.combine(order_datetime, order_datetime_hours)

    if st.button("Create Order"):
        new_order = orders(tours_id=selected_tour_id, payment_type=selected_payment_type, order_datetime=order_datetime)
        session.add(new_order)
        session.commit()
        st.success(f"Order created with ID: {new_order.order_id}")
        time.sleep(1)
        st.experimental_rerun()

    # Create new order detail
    st.header("Add Order Detail")
    orders_local = session.query(orders).all()
    order_options = [(o.order_id, f"Order {o.order_id}") for o in orders_local]
    selected_order_id = st.selectbox("Select Order", order_options, format_func=lambda x: x[1])[0]
    order_details = session.query(orderdetails).filter(orderdetails.order_id == selected_order_id).all()

    already_bought = [f.flavor_id for f in order_details]
    flavor_option = [(f.flavor_id, f.name) for f in flavors if f.flavor_id not in already_bought]
    if len(flavor_option) == 0:
        st.warning("No more flavors to add to this order")
        
    else:
        selected_flavor_id = st.selectbox("Select Flavor", flavor_option, format_func=lambda x: x[1])[0]

        amount = st.number_input("Amount (scoops)", min_value=1, value=1)
        discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=0)
        st.write(f'Flavor Base Price {flavor_baseprices[selected_flavor_id]}')
        st.write(f'Current Price {round(flavor_baseprices[selected_flavor_id] - (flavor_baseprices[selected_flavor_id] * discount / 100),2)}')
        if st.button("Add Order Detail"):
            new_order_detail = orderdetails(order_id=selected_order_id, flavor_id=selected_flavor_id, amount=amount, discount=discount)
            session.add(new_order_detail)
            session.commit()
            st.success(f"Order detail added to Order {selected_order_id}")
            time.sleep(1)
            st.experimental_rerun()

    # Update orders and order details
    st.header("Update orders and Order Details")
    selected_order_id = st.selectbox("Select Order to Update", order_options, format_func=lambda x: x[1], key="update_order")[0]
    order = session.query(orders).filter(orders.order_id == selected_order_id).one()
    if order is not None: # empty
        updated_payment_type = st.selectbox("Update Payment Type", payment_types, index=payment_types.index(order.payment_type))
        if st.button("Update Order"):
            order.payment_type = updated_payment_type
            session.commit()
            st.success(f"Order {selected_order_id} updated")
            time.sleep(1)
            st.experimental_rerun()

        order_details = session.query(orderdetails).filter(orderdetails.order_id == selected_order_id).all()
        if type(order_details) is list and len(order_details)>0 : # empty
            order_detail_options = [(od.flavor_id, f"{flavor_options[od.flavor_id]}: {od.amount} scoops") for od in order_details]
            selected_order_detail_flavor_id = st.selectbox("Select Order Detail to Update", order_detail_options, format_func=lambda x: x[1])[0]

            order_detail = session.query(orderdetails).filter(orderdetails.order_id == selected_order_id, orderdetails.flavor_id == selected_order_detail_flavor_id).one()
            updated_amount = st.number_input("Update Amount (scoops)", min_value=1, value=order_detail.amount, key="update_amount")
            updated_discount = st.number_input("Update Discount (%)", min_value=0, max_value=100, value=order_detail.discount, key="update_discount")
            st.write(f'Flavor Base Price {flavor_baseprices[selected_order_detail_flavor_id]}')
            st.write(f'Current Price {round(flavor_baseprices[selected_order_detail_flavor_id] - (flavor_baseprices[selected_order_detail_flavor_id] * updated_discount / 100),2)}')
            if st.button("Update Order Detail"):
                order_detail.amount = updated_amount
                order_detail.discount = updated_discount
                session.commit()
                st.success(f"Order detail of Order {selected_order_id} and Flavor {selected_order_detail_flavor_id} updated")
                time.sleep(1)
            st.experimental_rerun()

    # Delete orders and order details
    st.header("Delete orders and Order Details")
    selected_order_id = st.selectbox("Select Order to Delete", order_options, format_func=lambda x: x[1], key="delete_order")[0]
    if st.button("Delete Order"):
        order_to_delete = session.query(orders).filter(orders.order_id == selected_order_id).one()
        session.delete(order_to_delete)
        session.commit()
        st.success(f"Order {selected_order_id} deleted")
        time.sleep(1)
        st.experimental_rerun()

    order_details = session.query(orderdetails).filter(orderdetails.order_id == selected_order_id).all()

    if type(order_details) is list and len(order_details)>0 : # empty
        order_detail_options = [(od.flavor_id, f"{flavor_options[od.flavor_id]}: {od.amount} scoops") for od in order_details]
        selected_order_detail_flavor_id = st.selectbox("Select Order Detail to Delete", order_detail_options, format_func=lambda x: x[1], key="delete_order_detail")[0]
        if st.button("Delete Order Detail"):
            order_detail_to_delete = session.query(orderdetails).filter(orderdetails.order_id == selected_order_id, orderdetails.flavor_id == selected_order_detail_flavor_id).one()
            session.delete(order_detail_to_delete)
            session.commit()
            st.success(f"Order detail of Order {selected_order_id} and Flavor {selected_order_detail_flavor_id} deleted")
            time.sleep(1)
            st.experimental_rerun()

        session.close()