import dash
from dash import Dash, Input, Output, html, dcc, callback
import json
import dash_ag_grid as dag
from screen_data_loader import load_screen_dataframes


dash.register_page(__name__)


from qc_plots import (
    exp_qc_pca_plot,
    read_length_distribution_plot,
    sample_correlation_plot,
    sample_qc_position_anno_plot,
    sample_qc_stats_accepted_reads_plot,
    sample_qc_stats_total_plot,
    sample_qc_position_coverage_plot,
    sample_dendogram_plot
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
    sample_qc_stats_pos_coverage_col_def,
    sample_qc_stats_pos_percentage_col_def,
    experiment_qc_corr_col_def
    )
# --- 2. Load Data ---

screen_dataframes = load_screen_dataframes()

ss_df = screen_dataframes["ss_df"]
sample_qc_meta_df = screen_dataframes["sample_qc_meta_df"]
sample_qc_read_length_df = screen_dataframes["sample_qc_read_length_df"]
sample_qc_stats_missing_var_df = screen_dataframes["sample_qc_stats_missing_var_df"]
missing_variants_in_library_df = screen_dataframes["missing_variants_in_library_df"]
sample_qc_stats_total_df = screen_dataframes["sample_qc_stats_total_df"]
sample_qc_stats_accepted_df = screen_dataframes["sample_qc_stats_accepted_df"]
sample_qc_stats_coverage_df = screen_dataframes["sample_qc_stats_coverage_df"]
sample_qc_stats_pos_coverage_df = screen_dataframes["sample_qc_stats_pos_coverage_df"]
sample_qc_stats_pos_counts_df = screen_dataframes["sample_qc_stats_pos_counts_df"]
sample_qc_position_cov_data_df = screen_dataframes["sample_qc_position_cov_data_df"]
sample_qc_cutoffs_df = screen_dataframes["sample_qc_cutoffs_df"]
sample_qc_position_anno_df = screen_dataframes["sample_qc_position_anno_df"]
sample_qc_stats_pos_percentage_df = screen_dataframes["sample_qc_stats_pos_percentage_df"]
sample_data_df = screen_dataframes["sample_data_df"]
correlation_matrix_df = screen_dataframes["correlation_matrix_df"]
experiment_qc_corr_df = screen_dataframes["experiment_qc_corr_df"]

col_data_df = screen_dataframes["col_data_df"]
pca_center_df = screen_dataframes["pca_center_df"]
pca_scale_df = screen_dataframes["pca_scale_df"]
pca_sdev_df = screen_dataframes["pca_sdev_df"]
pca_rotation_df = screen_dataframes["pca_rotation_df"]
pca_x_scores_df = screen_dataframes["pca_x_scores_df"]


# Process position coverage data with boxplot
sample_qc_stats_pos_coverage_df_processed, sample_qc_stats_pos_coverage_col_def_config = sample_qc_stats_pos_coverage_col_def(
    sample_qc_stats_pos_coverage_df, 
    sample_qc_stats_pos_counts_df
)

experiment_qc_corr_processed_df = experiment_qc_corr_col_def(experiment_qc_corr_df)


layout = html.Div([
    html.H1("QC Dashboard", style={'fontFamily': 'sans-serif'}),

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
        html.H3("Sample QC Stats Coverage Plot"),
        dcc.Graph(
            id='sample-qc-position-coverage', 
            figure=sample_qc_position_coverage_plot(sample_qc_position_cov_data_df, sample_qc_cutoffs_df)
        )
    ], style={'marginBottom': '50px'}),
    
    
    html.Div([
        html.H3("Sample QC Stats Position Coverage Table"),
        dag.AgGrid(
            id="sample-qc-stats-position-coverage-table",
            rowData=sample_qc_stats_pos_coverage_df_processed.to_dict('records'),
            columnDefs=sample_qc_stats_pos_coverage_col_def_config["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_stats_pos_coverage_col_def_config["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_stats_pos_coverage_col_def_config["style"]
        ),
    ]),
    
    html.Div([
        html.H3("Sample QC Position Annotation"),
        dcc.Graph(
            id='sample_qc_position_anno_plot', 
            figure=sample_qc_position_anno_plot(sample_qc_position_anno_df, sample_qc_cutoffs_df)
        )
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H3("Sample QC Stats Position Percentage Table"),
        dag.AgGrid(
            id="sample-qc-stats-position-percentage-table",
            rowData=sample_qc_stats_pos_percentage_df.to_dict('records'),
            columnDefs=sample_qc_stats_pos_percentage_col_def["columns"],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            columnSize="sizeToFit",
            dashGridOptions=sample_qc_stats_pos_percentage_col_def["dashGridOptions"],
            className="ag-theme-alpine",
            style=sample_qc_stats_pos_percentage_col_def["style"]
        ),
    ]),
        
    html.Div([
        html.H3("Sample Correlation Dendogram"),
        dcc.Graph(
            id='sample-correlation-dendogram', 
            figure=sample_dendogram_plot(sample_data_df, correlation_matrix_df)
        )
    ], style={
    'display': 'flex',
    'flexDirection': 'column',  # Stacks the H3 and Graph vertically
    'alignItems': 'center',     # Centers them horizontally
    'justifyContent': 'center', # Centers them vertically (if the div has a height)
    'width': '80%',             # Controls how wide the graph area should be
    'margin': '0 auto 50px auto' # '0 auto' centers the whole Div itself; '50px' keeps your bottom margin
}),
    
    html.Div([
        html.H3("Sample Correlation Plot"),
        dcc.Graph(
            id='sample_correlation_plot',
            figure=sample_correlation_plot(experiment_qc_corr_df)
        )
    ], style={
    'display': 'flex',
    'flexDirection': 'column',  # Stacks the H3 and Graph vertically
    'alignItems': 'center',     # Centers them horizontally
    'justifyContent': 'center', # Centers them vertically (if the div has a height)
    'width': '80%',             # Controls how wide the graph area should be
    'margin': '0 auto 50px auto' # '0 auto' centers the whole Div itself; '50px' keeps your bottom margin
}),
    
    
    html.Div([
        html.H3("Experiment QC Correlation Table"),
            dag.AgGrid(
                id="experiment-qc-correlation-table",
                rowData=experiment_qc_corr_df.to_dict('records'),
                columnDefs=experiment_qc_corr_processed_df["columns"],
                defaultColDef={"sortable": True, "filter": True, "resizable": True},
                columnSize="sizeToFit",
                dashGridOptions=experiment_qc_corr_processed_df["dashGridOptions"],
                className="ag-theme-alpine",
                style=experiment_qc_corr_processed_df["style"]
            ),
    ]),
    
    html.Div([
        html.H3("Sample PCA Plot"),
        dcc.Graph(
            id='sample_pca_plot',
            figure=exp_qc_pca_plot(
                col_data_df,
                pca_center_df,
                pca_scale_df,
                pca_sdev_df,
                pca_rotation_df,
                pca_x_scores_df,
            )
        )
    ], style={
    'display': 'flex',
    'flexDirection': 'column',  # Stacks the H3 and Graph vertically
    'alignItems': 'center',     # Centers them horizontally
    'justifyContent': 'center', # Centers them vertically (if the div has a height)
    'width': '80%',             # Controls how wide the graph area should be
    'margin': '0 auto 50px auto' # '0 auto' centers the whole Div itself; '50px' keeps your bottom margin
}),
    
], style={'padding': '20px'})


@callback(
    Input("sample-qc-stats-position-coverage-table", "cellRendererData")
)
def graphClickData(d):
    return json.dumps(d)

