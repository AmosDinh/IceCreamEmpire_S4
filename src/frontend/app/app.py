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

    # Dashboard tab
    if session_state.page == "Dashboard":
        query = f"SELECT * FROM VendorPerformance"
        vendor_performance_data = db.sql(query)

        query = "SELECT forename || ' ' || lastname as name, salary  FROM icecreamvendors"
        vendor_salary_data = db.sql(query)



        query = f"SELECT * FROM Stock"
        stock_data = db.sql(query)

        # Query 1 of the complex queries
        query = """SELECT F.name AS flavor_name,
                        ROUND(SUM(OD.amount * F.base_price_per_scoop * (100 - OD.discount)/100),2) AS total_revenue
                    FROM Flavors F
                        INNER JOIN OrderDetails OD ON F.flavor_id = OD.flavor_id
                    GROUP BY F.name
                    ORDER BY total_revenue DESC;"""
        icecream_sales_data = db.sql(query)


        # Create bar charts using Plotly
        vendor_performance_chart = px.bar(
            vendor_performance_data,
            x="forename",
            y="total_sales",
            title="Vendor Performance",
            labels={"forename": "Forname", "total_sales": "Total Sales"},
        )
        vendor_salary_data_chart = px.bar(
            vendor_salary_data,
            x="name",
            y="salary",
            title="Vendor Salary",
            labels={"name": "Name", "salary": "Salary"},
        )

        stock_chart = px.bar(
            stock_data,
            x="name",
            y="amount",
            title="Current Stock",
            labels={"name": "Name", "amount": "Amount"},
        )

        revenue_chart = px.bar(
            icecream_sales_data,
            x="flavor_name",
            y="total_revenue",
            title="Revenue in Euros per Flavor",
            labels={"flavor_name": "Flavor name", "total_revenue": "Revenue"},
        )


        st.plotly_chart(vendor_performance_chart)
        if st.button("Refresh Vendor Performance (Materialized View)"):
            db.sql("REFRESH MATERIALIZED VIEW VendorPerformance;")
            st.experimental_rerun()
        st.plotly_chart(vendor_salary_data_chart)

        st.plotly_chart(stock_chart)
        
        st.plotly_chart(revenue_chart)
        




        

    if session_state.page == "Tour CRUD":
        crudtour(db)
    if  session_state.page == "Orders CRUD":
        crudorder(db)



if __name__ == "__main__":
    main()