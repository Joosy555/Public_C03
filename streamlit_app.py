# Import python packages.
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched
from snowflake.snowpark.functions import count
session = get_active_session()

# Write directly to the app.
st.title(f":cup_with_straw: Customize")
st.write(
  """Werk aan de winkel.
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()
#st.dataframe(data=my_dataframe, use_container_width=True)
editable_df = st.data_editor(my_dataframe);

st.write(my_dataframe.__len__())

submitted = st.button('Submit')
if submitted:   
    if my_dataframe.__len__() > 0:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
        
            st.success("Button clicked",icon=":material/thumb_up:")
        except:
            st.write("Somewthing went wrong")
    else:
        st.write("Niets te doen")
        st.write(my_dataframe.__len__())
        

#st.write(my_dataframe)
