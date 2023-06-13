import streamlit as st
from streamlit import session_state
from classes.queries import Queries
from crudtour import crudtour
from crudorder import crudorder
from dashboard import dashboard

def main():
    st.set_page_config(
        page_title="Ice Cream Empire Dashboard", page_icon=":memo:", layout="wide"
    )
    db = Queries()

    pages = [
        "Dashboard",
        "Tour CRUD",
        "Orders CRUD",
        "IceCreamVendors",
        "Neighborhoods",
        "Vehicles",
        "VehicleStoresFlavors",
        "Tours",
        "Flavors",
        "Contents",
        "Orders",
        "OrderDetails",
        "Warehouses",
        "WarehouseStoresFlavors"
        
    ]

    # Startpage
    if not "page" in session_state:
        session_state.page = pages[0]

    # Create sidebar with tabs
    for page in pages:
        if st.sidebar.button(page):
            print(page)
            session_state.page = page

    st.title(session_state.page)

    # Side content
    # Create tabs with table views
    for page in pages[3:]:
        if session_state.page == page:
            query = f"SELECT * FROM {page}"
            df = db.sql(query)
            st.write(df)

    # Dashboard
    if session_state.page == "Dashboard":
        dashboard(db)

    if session_state.page == "Tour CRUD":
        crudtour(db)

    if  session_state.page == "Orders CRUD":
        crudorder(db)



if __name__ == "__main__":
    main()