import plotly.express as px
import streamlit as st
from streamlit import session_state
from classes.queries import Queries
from crudtour import crudtour
from crudorder import crudorder

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
        "Tours",
        "Flavors",
        "Contents",
        "Orders",
        "OrderDetails",
        "Warehouses",
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
    for page in pages[2:]:
        if session_state.page == page:
            query = f"SELECT * FROM {page}"
            df = db.sql(query)
            st.write(df)

    # Dashboard tab
    if session_state.page == "Dashboard":
        query = f"SELECT * FROM VendorPerformance"
        vendor_performance_data = db.sql(query)
        query = f"SELECT * FROM Stock"
        stock_data = db.sql(query)
        # Create bar charts using Plotly Express
        vendor_performance_chart = px.bar(
            vendor_performance_data,
            x="forename",
            y="total_sales",
            title="Vendor Performance",
            labels={"forename": "Forname", "total_sales": "Total Sales"},
        )
        stock_chart = px.bar(
            stock_data,
            x="name",
            y="amount",
            title="Current Stock",
            labels={"name": "Name", "amount": "Amount"},
        )
        st.plotly_chart(vendor_performance_chart)
        if st.button("Refresh Vendor Performance (Materialized View)"):
            db.sql("REFRESH MATERIALIZED VIEW VendorPerformance;")
            st.experimental_rerun()

        st.plotly_chart(stock_chart)
        

    if session_state.page == "Tour CRUD":
        crudtour(db)
    if  session_state.page == "Orders CRUD":
        crudorder(db)



if __name__ == "__main__":
    main()