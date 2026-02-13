def create_progress_column(header_name, field_name, is_bold=False) -> dict:
    color = "rgba(76, 175, 80, 0.5)"
    
    if is_bold:
        # Conditional styling based on Pass field with progress bar
        cell_style_function = '''({
                backgroundImage: params.value != null ? 
                    `linear-gradient(90deg, ''' + color + ''' ${params.value}%, transparent ${params.value}%)` : 
                    'none',
                backgroundRepeat: 'no-repeat',
                textAlign: 'center',
                fontWeight: params.data && (params.data['Pass'] === 'TRUE' || params.data['Pass'] === true) ? 'bold' : 'bold',
                color: params.data && (params.data['Pass'] === 'TRUE' || params.data['Pass'] === true) ? '#198754' : '#dc3545'
            })'''
    else:
        # Standard progress bar styling
        cell_style_function = '''({
                backgroundImage: params.value != null ? 
                    `linear-gradient(90deg, ''' + color + ''' ${params.value}%, transparent ${params.value}%)` : 
                    'none',
                backgroundRepeat: 'no-repeat',
                textAlign: 'center'
            })'''
    
    return {
        "headerName": header_name,
        "field": field_name,
        'cellStyle': {
            'function': cell_style_function
        }
    }

sample_sheet_col_def = {
                "columns": [
                        {"headerName": "ID Study", "field": "id_study"},
                        {"headerName": "ID Run", "field": "id_run"},
                        {"headerName": "Sample Name", "field": "sample_name"},
                        {"headerName": "Fastq 1", "field": "fastq_1"},
                        {"headerName": "Fastq 2", "field": "fastq_2"},
                        {"headerName": "Targeton ID", "field": "targeton_id"},
                        {"headerName": "Library Name", "field": "library_name"},
                        {"headerName": "Library Type", "field": "library_type"},
                        {"headerName": "Expt ID", "field": "Expt_ID"},
                        {"headerName": "Valiant Meta", "field": "valiant_meta"},
                ],
                "dashGridOptions": {
                        "pagination": True,
                        "paginationPageSize": 10,
                        "rowHeight": 28,
                        "headerHeight": 32
                },
                "style": {"height": 380, "width": "100%"}
            }

sample_qc_meta_col_def = {
                "columns": [
                    {"headerName": "Sample Name", "field": "sample_name"},
                    {"headerName": "Sample Info", "field": "sample_info"},
                    {"headerName": "Gene ID", "field": "gene_id"},
                    {"headerName": "Gene Name", "field": "gene_name"},
                    {"headerName": "Transcript ID", "field": "transcript_id"},
                    {"headerName": "Exon Num", "field": "exon_num"},
                    {"headerName": "Targeton ID", "field": "targeton_id"},
                    {"headerName": "SgRNA ID", "field": "sgrna_id"}
                ],
                "dashGridOptions": {
                        "pagination": True,
                        "paginationPageSize": 10,
                        "rowHeight": 28,
                        "headerHeight": 32
                },
                "style": {"height": 380, "width": "100%"}
}


sample_qc_read_length_col_def = {
            "columns": [
                {"headerName": "Group", "field": "Group"},
                {"headerName": "Sample", "field": "Sample"},
                {"headerName": "Sample Info", "field": "Sample Info"},
                {"headerName": "Sample Exon", "field": "Sample Exon"},
                {"headerName": "Total Reads", "field": "Total Reads"},
                create_progress_column("% 0 ~ 50", "% 0 ~ 50"),
                create_progress_column("% 50 ~ 100", "% 50 ~ 100"),
                create_progress_column("% 100 ~ 150", "% 100 ~ 150"),
                create_progress_column("% 150 ~ 200", "% 150 ~ 200"),
                create_progress_column("% 200 ~ 250", "% 200 ~ 250"),
                create_progress_column("% 250 ~ 300", "% 250 ~ 300"),
                {"headerName": "Pass Threshold (%)", "field": "Pass Threshold (%)"},
                {
                    "headerName": "Pass",
                    "field": "Pass",
                    "cellRenderer": {
                        "function": "params.value === 'TRUE' || params.value === true ? '✅' : '❌'"
                    },
                    "cellStyle": {
                        "function": "params.value === 'TRUE' || params.value === true ? \
                        {'color': '#198754', 'textAlign': 'center'} : \
                        {'color': '#dc3545', 'textAlign': 'center'}"
                    }
                }
            ],
        "dashGridOptions": {
                    "pagination": True,
                    "paginationPageSize": 10,
                    "rowHeight": 28,
                    "headerHeight": 32,
                    "animateRows": False,
                    "getRowStyle": {
                        "function": "params.data && (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) ? \
                            {'backgroundColor': 'rgb(226 165 165 / 55%)'} : {}"
                    }
                },
        "style": {"height": 380, "width": "100%"}
}

sample_qc_stats_missing_var_col_def = {
        "columns": [
            {"headerName": "Group", "field": "Group"},
                {"headerName": "Sample", "field": "Sample"},
                {"headerName": "Sample Info", "field": "Sample Info"},
                {"headerName": "Sample Exon", "field": "Sample Exon"},
                {"headerName": "Library Sequences", "field": "Library Sequences"},
                {"headerName": "Missing Library Sequences", "field": "Missing Library Sequences"},
                {
                    "headerName": "% Missing Library Sequences", 
                    "field": "% Missing Library Sequences",
                    "cellStyle": {
                        "function": "params.data && (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) ? \
                            {'color': '#dc3545', 'fontWeight': 'bold'} : \
                            {'color': '#198754', 'fontWeight': 'bold'}"
                    }
                },
                {"headerName": "Pass Threshold (%)", "field": "Pass Threshold (%)"},
                {
                    "headerName": "Pass",
                    "field": "Pass",
                    "cellRenderer": {
                        "function": "params.value === 'TRUE' || params.value === true ? '✅' : '❌'"
                    },
                    "cellStyle": {
                        "function": "params.value === 'TRUE' || params.value === true ? \
                            {'color': '#198754', 'textAlign': 'center'} : \
                            {'color': '#dc3545', 'textAlign': 'center'}"
                    }
                }
        ],
        "dashGridOptions": {
                "pagination": True,
                "paginationPageSize": 10,
                "rowHeight": 28,
                "headerHeight": 32,
                "getRowStyle": {
                    "function": "params.data && (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) ? \
                        {'backgroundColor': '#E2A5A5'} : {}"
                }
            },
        "style": {"height": 380, "width": "100%"}
}

missing_variants_in_library_col_def = {
        "columns": [
                {"headerName": "ID", "field": "id"},
                {"headerName": "Name", "field": "name"},
                {"headerName": "Sequence", "field": "sequence"},
                {"headerName": "Length", "field": "length"},
                {"headerName": "Count", "field": "count"},
                {"headerName": "Unique", "field": "unique"},
                {"headerName": "Sample", "field": "sample"},
                {"headerName": "Is Ref", "field": "is_ref"},
                {"headerName": "Is PAM", "field": "is_pam"}
        ],
        "dashGridOptions": {
                "pagination": True,
                "paginationPageSize": 10,
                "rowHeight": 28,
                "headerHeight": 32
            },
        "style": {"height": 380, "width": "100%"}
}


sample_qc_stats_total_col_def = {    
            "columns": [
                {"headerName": "Group", "field": "Group"},
                {"headerName": "Sample", "field": "Sample"},
                {"headerName": "Sample Info", "field": "Sample Info"},
                {"headerName": "Sample Exon", "field": "Sample Exon"},
                {"headerName": "Accepted Reads", "field": "Accepted Reads"},
                create_progress_column("% Accepted Reads", "% Accepted Reads"),
                {"headerName": "Excluded Reads", "field": "Excluded Reads"},
                create_progress_column("% Excluded Reads", "% Excluded Reads"),
                {
                    "headerName": "Total Reads",
                    "field": "Total Reads",
                    "cellStyle": {
                        "function": "params.data && (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) ? \
                            {'color': '#dc3545', 'fontWeight': 'bold'} : \
                            {'color': '#198754', 'fontWeight': 'bold'}"
                    }
                },
                {"headerName": "Pass Threshold", "field": "Pass Threshold"},
                {
                    "headerName": "Pass",
                    "field": "Pass",
                    "cellRenderer": {
                        "function": "params.value === 'TRUE' || params.value === true ? '✅' : '❌'"
                    },
                    "cellStyle": {
                        "function": "params.value === 'TRUE' || params.value === true ? \
                        {'color': '#198754', 'textAlign': 'center'} : \
                        {'color': '#dc3545', 'textAlign': 'center'}"
                    }
                }
            ],
        "dashGridOptions": {
                    "pagination": True,
                    "paginationPageSize": 10,
                    "rowHeight": 28,
                    "headerHeight": 32,
                    "animateRows": False,
                    "getRowStyle": {
                        "function": "params.data && \
                            (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) \
                                ? {'backgroundColor': 'rgb(226 165 165 / 55%)'} : {}"
                    }
                },
        "style": {"height": 380, "width": "100%"}
}


sample_qc_stats_accepted_col_def = {  
            "columns": [
                {"headerName": "Group", "field": "Group"},    
                {"headerName": "Sample", "field": "Sample"},
                {"headerName": "Sample Info", "field": "Sample Info"},
                {"headerName": "Sample Exon", "field": "Sample Exon"},
                create_progress_column("% Library Reads", "% Library Reads", is_bold=True),
                create_progress_column("% Reference Reads", "% Reference Reads"),
                create_progress_column("% PAM Reads", "% PAM Reads"),
                create_progress_column("% Unmapped Reads", "% Unmapped Reads"),
                {"headerName": "Pass Threshold (%)", "field": "Pass Threshold (%)"},
                {
                    "headerName": "Pass",
                    "field": "Pass",
                    "cellRenderer": {
                        "function": "params.value === 'TRUE' || params.value === true ? '✅' : '❌'"
                    },
                    "cellStyle": {
                        "function": "params.value === 'TRUE' || params.value === true ? \
                        {'color': '#198754', 'textAlign': 'center'} : \
                        {'color': '#dc3545', 'textAlign': 'center'}"
                    }
                }
            ],
        "dashGridOptions": {
                    "pagination": True,
                    "paginationPageSize": 10,
                    "rowHeight": 28,
                    "headerHeight": 32,
                    "animateRows": False,
                    "getRowStyle": {
                        "function": "params.data && \
                            (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) \
                                ? {'backgroundColor': 'rgb(226 165 165 / 55%)'} : {}"
                    }
                },
        "style": {"height": 380, "width": "100%"}
}


sample_qc_stats_coverage_col_def = {  
            "columns": [
                {"headerName": "Group", "field": "Group"},    
                {"headerName": "Sample", "field": "Sample"},
                {"headerName": "Sample Info", "field": "Sample Info"},
                {"headerName": "Sample Exon", "field": "Sample Exon"},
                {"headerName": "Total Library Reads", "field": "Total Library Reads"},
                {"headerName": "Total Library Sequences", "field": "Total Library Sequences"},
                {
                    "headerName": "Library Coverage", 
                    "field": "Library Coverage", 
                    "cellStyle": {
                        "function": "params.data && (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) ? \
                            {'color': '#dc3545', 'fontWeight': 'bold'} : \
                            {'color': '#198754', 'fontWeight': 'bold'}"
                    }
                },
                {"headerName": "Median Coverage", "field": "Median Coverage"},
                {"headerName": "Pass Threshold", "field": "Pass Threshold"},
                {
                    "headerName": "Pass",
                    "field": "Pass",
                    "cellRenderer": {
                        "function": "params.value === 'TRUE' || params.value === true ? '✅' : '❌'"
                    },
                    "cellStyle": {
                        "function": "params.value === 'TRUE' || params.value === true ? \
                        {'color': '#198754', 'textAlign': 'center'} : \
                        {'color': '#dc3545', 'textAlign': 'center'}"
                    }
                }
            ],
        "dashGridOptions": {
                    "pagination": True,
                    "paginationPageSize": 10,
                    "rowHeight": 28,
                    "headerHeight": 32,
                    "animateRows": False,
                    "getRowStyle": {
                        "function": "params.data && \
                            (params.data['Pass'] === 'FALSE' || params.data['Pass'] === false) \
                                ? {'backgroundColor': 'rgb(226 165 165 / 55%)'} : {}"
                    }
                },
        "style": {"height": 380, "width": "100%"}
}