import streamlit as st

def get_write_relation_to_screen(db, relation_name:str):

    df, primary_key_column_names = db.get_relation(relation_name)
    df_display = df.copy()
    df_key = f"{relation_name}dftoggle1"

    col1, col2 = st.columns(2)
    
    
    if df_key in st.session_state:
        # get all edited cells
        for key, value in st.session_state[df_key]['edited_cells'].items():
            row_index = int(key.split(":")[0])
            col_index = int(key.split(":")[1])-1
            col_name = df.columns[col_index]
            if col_name not in primary_key_column_names:
                # keep[key] = value
                df_display.iloc[row_index,col_index] = value

        # get all added rows
        st.write("added rows")
        for row in st.session_state[df_key]['added_rows']:
            # check not null
            new_row = {}
            only_key_added = True
            for k, v in row.items():
                col_name = df.columns[int(k)-1]
                if col_name not in primary_key_column_names:
                    new_row[col_name] = v
                    only_key_added = False
                else:
                    new_row[col_name] = None
            
            if only_key_added:
                continue 

            df_display = df_display.append(new_row, ignore_index=True)
            # st.write(row)
            # values = list(row.values())
            st.write(new_row)
        # remove deleted rows
        deleted_index = df_display.index.isin(st.session_state[df_key]['deleted_rows'])
        df_display = df_display[~deleted_index]
        

    with col1:
        edited_df = st.experimental_data_editor(df,num_rows='dynamic', key=df_key)

    with col2:
        st.write(df_display)
        st.button("Save", key=df_key+'button')



    

    

    
