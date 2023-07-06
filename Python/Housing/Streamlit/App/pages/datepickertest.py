import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from typing import List
from st_aggrid import AgGrid, GridOptionsBuilder

def main():
    # Create an empty DataFrame
    data = {
        'Date': ['2023-06-01', '2023-06-02', '2023-06-03'],
        'Value': [10, 20, 30]
    }
    df = pd.DataFrame(data)

    # Build AgGrid options
    gob = GridOptionsBuilder.from_dataframe(df)
    gob.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum')
    gob.configure_grid_options(domLayout='autoHeight', autoGroupColumnDef=True, editable=True)

    # Specify the React component renderer for the 'Date' column
    gob.configure_column('Date', editable=True, cellRenderer='datePickerRenderer')

    grid_options = gob.build()

    # Register the custom renderer
    js_code = """
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { render } from 'react-dom';
    import Flatpickr from 'react-flatpickr';

    const DatePickerRenderer = ({ value, api }) => {
        const handleChange = (date) => {
            const selectedDate = date[0].toISOString().split('T')[0];
            api.applyTransaction({ update: [{ id: api.getFocusedCell().rowIndex, field: api.getFocusedCell().column.getId(), value: selectedDate }] });
        };

        return (
            <div>
                <Flatpickr
                    value={value}
                    options={{ dateFormat: 'Y-m-d' }}
                    onChange={handleChange}
                />
            </div>
        );
    };

    // Render the React component
    const renderDatePicker = (params) => {
        ReactDOM.render(<DatePickerRenderer value={params.value} api={params.api} />, params.eParentElement);
    };

    export { renderDatePicker };
    """

    # Render the AgGrid
    with st.container():
        AgGrid(df, gridOptions=grid_options, key='grid')

    # Add the custom JavaScript code to the page
    components.html(js_code, height=0)

if __name__ == '__main__':
    main()
