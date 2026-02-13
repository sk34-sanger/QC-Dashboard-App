import dash
from dash import dcc, html

import dash_ag_grid as dag
import pandas as pd
from qc_plots import (
    read_length_distribution_plot,
    sample_qc_stats_accepted_reads_plot,
    sample_qc_stats_total_plot,
    sample_qc_position_coverage_plot
    )

from table_configs.table_config import (
    sample_sheet_col_def,
    sample_qc_meta_col_def,
    sample_qc_read_length_col_def,
    sample_qc_stats_missing_var_col_def,
    missing_variants_in_library_col_def,
    sample_qc_stats_total_col_def,
    sample_qc_stats_accepted_col_def,
    sample_qc_stats_coverage_col_def,
    )
# --- 2. Load Data ---

ss_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_sheet.tsv", sep='\t')
sample_qc_meta_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_meta.tsv", sep='\t')
sample_qc_read_length_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_read_length.tsv", sep='\t')
sample_qc_stats_missing_var_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_stats_missing.tsv", sep='\t')
missing_variants_in_library_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/missing_variants_in_library.tsv", sep='\t')
sample_qc_stats_total_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_stats_total.tsv", sep='\t')
sample_qc_stats_accepted_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_stats_accepted.tsv", sep='\t')
sample_qc_stats_coverage_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_stats_coverage.tsv", sep='\t')
sample_qc_position_cov_data_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_position_cov_data.tsv", sep='\t')
sample_qc_cutoffs_df = pd.read_csv("/home/ubuntu/QC-Dashboard-App/data/screen/sample_qc_cutoffs.tsv", sep='\t')

# --- 3. Define Dash App ---
app = dash.Dash(__name__, title="QC Dashboard")

app.layout = html.Div([
    html.H1("Genomic Sequencing QC Dashboard", style={'fontFamily': 'sans-serif'}),

    # The High-Performance ReactTable (AG Grid)
    html.Div([
        html.H3("Sample Sheet"),
        dag.AgGrid(
            id="sample-sheet",
            rowData=ss_df.to_dict('records'),
            columnDefs=sample_sheet_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            dashGridOptions=sample_sheet_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_sheet_col_def["style"]
        )
    ]),
    
    html.Div([
        html.H3("Sample QC Meta"),
        dag.AgGrid(
            id="sample-qc-meta",
            rowData=sample_qc_meta_df.to_dict('records'),
            columnDefs=sample_qc_meta_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_meta_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_meta_col_def["style"]
        )
    ]),
    
    # The Interactive Plot
    html.Div([
        html.H3("Read Length Distribution"),
        dcc.Graph(id='read-length-plot', figure=read_length_distribution_plot(sample_qc_read_length_df))
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H3("Sample QC Read Length"),
        dag.AgGrid(
            id="sample-qc-read-length",
            rowData=sample_qc_read_length_df.to_dict('records'),
            columnDefs=sample_qc_read_length_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_read_length_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_read_length_col_def["style"]
        )
    ]),
    
    
    html.Div([
        html.H3("Sample QC Stats Missing Variants"),
        dag.AgGrid(
            id="sample-qc-stats-missing-variants",
            rowData=sample_qc_stats_missing_var_df.to_dict('records'),
            columnDefs=sample_qc_stats_missing_var_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_stats_missing_var_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_stats_missing_var_col_def["style"]
        )
    ]),
    
    html.Div([
        html.H3("Missing Variants in Library"),
        dag.AgGrid(
            id="missing-variants-in-library",
            rowData=missing_variants_in_library_df.to_dict('records'),
            columnDefs=missing_variants_in_library_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            dashGridOptions=missing_variants_in_library_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=missing_variants_in_library_col_def["style"]
        )
    ]),
    
    html.Div([
        html.H3("Sample QC Stats"),
        dcc.Graph(id='sample-qc-stats-total', figure=sample_qc_stats_total_plot(sample_qc_stats_total_df))
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H3("Sample QC Stats Total"),
        dag.AgGrid(
            id="sample-qc-stats-total-table",
            rowData=sample_qc_stats_total_df.to_dict('records'),
            columnDefs=sample_qc_stats_total_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_stats_total_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_stats_total_col_def["style"]
        )
    ]),
    
    html.Div([
        html.H3("Sample QC Stats Accepted Reads"),
        dcc.Graph(
            id='sample-qc-stats-accepted-reads', 
            figure=sample_qc_stats_accepted_reads_plot(sample_qc_stats_accepted_df, sample_qc_stats_coverage_df)
        )
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H3("Sample QC Stats Accepted Reads Table"),
        dag.AgGrid(
            id="sample-qc-stats-accepted-reads-table",
            rowData=sample_qc_stats_accepted_df.to_dict('records'),
            columnDefs=sample_qc_stats_accepted_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_stats_accepted_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_stats_accepted_col_def["style"]
        )
    ]),
    
    html.Div([
        html.H3("Sample QC Stats Coverage Table"),
        dag.AgGrid(
            id="sample-qc-stats-coverage-table",
            rowData=sample_qc_stats_coverage_df.to_dict('records'),
            columnDefs=sample_qc_stats_coverage_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_stats_coverage_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_stats_coverage_col_def["style"]
        )
    ]),
    
    html.Div([
        html.H3("Sample QC Position Coverage Plot"),
        dcc.Graph(
            id='sample-qc-position-coverage', 
            figure=sample_qc_position_coverage_plot(sample_qc_position_cov_data_df, sample_qc_cutoffs_df)
        )
    ], style={'marginBottom': '50px'}),
    
], style={'padding': '20px'})


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')