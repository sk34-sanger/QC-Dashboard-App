import dash
from dash import Dash, html, dcc

# --- 3. Define Dash App ---
app = dash.Dash(__name__, use_pages=True, title="QC Dashboard")

app.layout = html.Div([
    # html.H1('Multi-Page Dashboard Navigation'),
    
    # Navigation links built dynamically from your pages
    # html.Div([
    #     dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"], style={"margin-right": "15px"})
    #     for page in dash.page_registry.values()
    # ]),

    # html.Hr(),

    # This is where the content of home.py, sales.py, etc., will dynamically render
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
