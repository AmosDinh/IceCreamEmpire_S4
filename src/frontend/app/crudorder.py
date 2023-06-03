import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import os
from datetime import datetime
import time


def update_vehicle_stock(session, stored_flavors_amount, selected_flavor_id, vehiclestoresflavors, tour_vehicle_id, posneg_amount):
   
    stored_flavors_amount[selected_flavor_id] += posneg_amount

    all = session.query(vehiclestoresflavors).filter(vehiclestoresflavors.vehicle_id == tour_vehicle_id, vehiclestoresflavors.flavor_id == selected_flavor_id).all()
    if len(all) == 0:
        new_vehiclestoresflavors = vehiclestoresflavors(vehicle_id=tour_vehicle_id, flavor_id=selected_flavor_id, amount=stored_flavors_amount[selected_flavor_id])
        session.add(new_vehiclestoresflavors)
    else:
        session.query(vehiclestoresflavors).filter(vehiclestoresflavors.vehicle_id == tour_vehicle_id, vehiclestoresflavors.flavor_id == selected_flavor_id).update({"amount": stored_flavors_amount[selected_flavor_id]})

def crudorder(db):

    engine = db.engine
    Base = automap_base()
    Base.prepare(engine, reflect=True)


    
    tours = Base.classes.tours
    flavors = Base.classes.flavors
    orders = Base.classes.orders
    orderdetails = Base.classes.orderdetails
    vehiclestoresflavors = Base.classes.vehiclestoresflavors

    session = Session(engine)

 

    # get flavors in truck
    

    # Create new order
    st.header("Create New Order")
    tours = session.query(tours).all()
    tour_options = [(t.tours_id, f"Tour {t.tours_id}: from {t.start_datetime} - {t.end_datetime}") for t in tours]
    selected_tour_id = st.selectbox("Select Tour", tour_options, format_func=lambda x: x[1])[0]

    tour_vehicle_id = [t.vehicle_id for t in tours if t.tours_id == selected_tour_id][0]
    stored_flavors = session.query(vehiclestoresflavors).filter(vehiclestoresflavors.vehicle_id == tour_vehicle_id).all()
    stored_flavors_amount = {f.flavor_id: f.amount for f in stored_flavors}


    flavors = session.query(flavors).all()

    flavor_options = {f.flavor_id: f.name for f in flavors}
    flavor_baseprices = {f.flavor_id: f.base_price_per_scoop for f in flavors}

    
    # show vehicle stock in pretty streamlit table
    
    st.write('______________________')

    st.write(f"Vehicle {tour_vehicle_id} Stock")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    for f in flavor_options:
        if f in stored_flavors_amount:
            with col1:
                st.write(f"{flavor_options[f]}")
            with col2:
                st.write(f"{stored_flavors_amount[f]}")
        else:
            with col1:
                st.write(f"{flavor_options[f]}")
            with col2:
                st.write(f"0")
                stored_flavors_amount[f] = 0
    
    st.write('______________________')
        

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

    # Create new order detail
    
    orders_local = session.query(orders).filter(orders.tours_id == selected_tour_id).all()
    order_options = [(o.order_id, f"Order {o.order_id}") for o in orders_local]
    if len(order_options) == 0:
        st.warning("Create an order first to add order details")
    else:

        st.header("Select Order")
        selected_order_id = st.selectbox("Select Order", order_options, format_func=lambda x: x[1])[0]
        st.header("Add Order Detail: Order "+str(selected_order_id))
        order_details = session.query(orderdetails).filter(orderdetails.order_id == selected_order_id).all()

        already_bought = [f.flavor_id for f in order_details]
        flavor_option = [(f.flavor_id, f.name) for f in flavors if f.flavor_id not in already_bought]
        if len(flavor_option) == 0:
            st.warning("No more flavors to add to this order")
            
        else:
            selected_flavor_id = st.selectbox("Select Flavor", flavor_option, format_func=lambda x: x[1])[0]
            maximum_amount = stored_flavors_amount[selected_flavor_id] 

            amount = st.number_input("Amount (scoops)", min_value=0, value=0, max_value=maximum_amount)
            discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=0)
            st.write(f'Flavor Base Price {flavor_baseprices[selected_flavor_id]}')
            st.write(f'Current Price {round(flavor_baseprices[selected_flavor_id] - (flavor_baseprices[selected_flavor_id] * discount / 100),2)}')
            if st.button("Add Order Detail"):
                new_order_detail = orderdetails(order_id=selected_order_id, flavor_id=selected_flavor_id, amount=amount, discount=discount)
                session.add(new_order_detail)

                # update vehiclestoresflavors
                update_vehicle_stock(session, stored_flavors_amount, selected_flavor_id, vehiclestoresflavors, tour_vehicle_id, -amount,)
                    
                session.commit()
                st.success(f"Order detail added to Order {selected_order_id}")
                time.sleep(1)
                st.experimental_rerun()

        # Update orders and order details
        st.header("Update orders and Order Details: Order "+str(selected_order_id))
        # selected_order_id = st.selectbox("Select Order to Update", order_options, format_func=lambda x: x[1], key="update_order")[0]
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
                
                maximum_amount = stored_flavors_amount[selected_order_detail_flavor_id] 
                
                updated_amount = st.number_input("Update Amount (scoops)", min_value=0, value=order_detail.amount, key="update_amount", max_value=order_detail.amount+maximum_amount)
                updated_discount = st.number_input("Update Discount (%)", min_value=0, max_value=100, value=order_detail.discount, key="update_discount")
                st.write(f'Flavor Base Price {flavor_baseprices[selected_order_detail_flavor_id]}')
                st.write(f'Current Price {round(flavor_baseprices[selected_order_detail_flavor_id] - (flavor_baseprices[selected_order_detail_flavor_id] * updated_discount / 100),2)}')
                if st.button("Update Order Detail"):

                    update_vehicle_amount = order_detail.amount - updated_amount
                    order_detail.amount = updated_amount
                    order_detail.discount = updated_discount
                     # update vehiclestoresflavors

                    update_vehicle_stock(session, stored_flavors_amount, selected_order_detail_flavor_id, vehiclestoresflavors, tour_vehicle_id, update_vehicle_amount)
                    
                    # stored_flavors_amount[selected_flavor_id] -= amount
                    # session.query(vehiclestoresflavors).filter(vehiclestoresflavors.vehicle_id == tour_vehicle_id, vehiclestoresflavors.flavor_id == selected_flavor_id).update({"amount": stored_flavors_amount[selected_flavor_id]})

                    session.commit()
                    st.success(f"Order detail of Order {selected_order_id} and Flavor {selected_order_detail_flavor_id} updated")
                    time.sleep(1)
                    st.experimental_rerun()

        # Delete orders and order details
        st.header("Delete orders and Order Details: Order "+str(selected_order_id))
        # selected_order_id = st.selectbox("Select Order to Delete", order_options, format_func=lambda x: x[1], key="delete_order")[0]
        if st.button("Delete Order"):
            order_to_delete = session.query(orders).filter(orders.order_id == selected_order_id).one()
            session.delete(order_to_delete)
            session.commit()
            st.success(f"Order {selected_order_id} deleted")
            time.sleep(1)
            #st.experimental_rerun()

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