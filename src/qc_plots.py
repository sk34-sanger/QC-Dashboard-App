import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram as scipy_dendrogram




def read_length_distribution_plot(df):
    bins = ['% 0 ~ 50', '% 50 ~ 100', '% 100 ~ 150', '% 150 ~ 200', '% 200 ~ 250', '% 250 ~ 300']
    df_melted = df.melt(
        id_vars=['Sample'], 
        value_vars=bins, 
        var_name='Length Distribution', 
        value_name='Composition Percentage'
    )
    df_melted['Length Distribution'] = df_melted['Length Distribution'].str.replace('% ', '')

    fig = px.bar(
        df_melted, 
        x="Length Distribution", 
        y="Composition Percentage", 
        facet_col="Sample",  # Creates separate subplot for each sample
        facet_col_wrap=3,    # Number of columns in the grid
        title="Read Length Distribution (50nt Increments)",
        template="plotly_white",
        color_discrete_sequence=["#4591DC"]  # Single color since each sample is separate
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    fig.update_layout(
        yaxis=dict(
            range=[0, 100], 
            ticksuffix="%"
        ),
        xaxis_title="Length Distribution",
        yaxis_title="Composition Percentage",
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        hovermode="x unified",
        height=800  # Adjust height for multiple subplots
    )

    # Update all y-axes to have consistent range
    fig.update_yaxes(range=[0, 100], ticksuffix="%")
    return fig


def sample_qc_stats_total_plot(df):
    # Create a stacked bar chart Total reads and Excluded Reads vs Sample
    df_long = df.melt(
        id_vars=["Sample"],
        value_vars=["Total Reads", "Excluded Reads"],
        var_name="Read Type",
        value_name="Read Counts",
    )
    fig = px.bar(
        df_long,
        x="Sample",
        y="Read Counts",
        color="Read Type",
        title="Total Reads vs Excluded Reads per Sample",
        template="plotly_white",
        labels={"Read Counts": "Read Counts", "Read Type": "Read Type"},
        color_discrete_sequence=["#4591DC", "#F26419"],  # Colors for Total reads and Excluded Reads
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Sample",
        yaxis_title="Read Counts",
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        hovermode="x unified",
        height=600
    )
    return fig

def sample_qc_stats_accepted_reads_plot(df, qc_stats_coverage_df):
    categories = ["% Library Reads", "% PAM Reads", "% Reference Reads", "% Unmapped Reads"]
    # Colorblind-friendly colors with 50% transparency (matching R's t_col with 0.5 alpha)
    colors = {
        "% Library Reads": "rgba(127, 205, 187, 0.5)",   # #7FCDBB with alpha
        "% PAM Reads": "rgba(246, 215, 122, 0.5)",       # #F6D77A with alpha
        "% Reference Reads": "rgba(155, 211, 240, 0.5)", # #9BD3F0 with alpha
        "% Unmapped Reads": "rgba(232, 174, 119, 0.5)",  # #E8AE77 with alpha
    }

    # Normalize to 100% (equivalent to R's position = "fill")
    percent_df = df[categories].div(df[categories].sum(axis=1), axis=0) * 100
    percent_df["Sample"] = df["Sample"]

    # Calculate y_scale for secondary axis (matching R's y_scale = max(library_cov) * 2)
    y_scale = qc_stats_coverage_df["Library Coverage"].max() * 2

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for category in categories:
        fig.add_trace(
            go.Bar(
                x=percent_df["Sample"],
                y=percent_df[category],
                name=category,
                marker_color=colors[category],
                text=percent_df[category].round(1).astype(str) + "%",
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate="%{x}<br>%{fullData.name}: %{y:.1f}%<extra></extra>",
            ),
            secondary_y=False,
        )

    fig.add_trace(
        go.Scatter(
            x=qc_stats_coverage_df["Sample"],
            y=qc_stats_coverage_df["Library Coverage"],
            name="Library Coverage",
            mode="lines+markers",
            marker=dict(color="#E31A1C", symbol="diamond", size=10),
            line=dict(color="#E31A1C", dash="dash"),
            hovertemplate="%{x}<br>Library Coverage: %{y}<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        barmode="stack",
        title=dict(text="Sample QC Stats", font=dict(size=24, family="sans-serif")),
        template="plotly_white",
        xaxis_title="Samples",
        yaxis_title="Percentage",
        yaxis_title_font=dict(size=18, family="sans-serif"),
        xaxis_title_font=dict(size=18, family="sans-serif"),
        hovermode="x unified",
        height=700,
        legend=dict(
            title_text="",
            font=dict(size=16),
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        plot_bgcolor="ivory",
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%", tickfont=dict(size=14), secondary_y=False)
    fig.update_yaxes(
        title_text="Library Coverage",
        range=[0, y_scale],
        tickfont=dict(size=14),
        secondary_y=True
    )
    fig.update_xaxes(tickangle=-90, tickfont=dict(size=14))
    return fig

def sample_qc_position_coverage_plot(df, sample_qc_cutoffs_df):
    """
    Create position coverage scatter plot for each sample
    
    Args:
        df: DataFrame with columns: sequence, position, count, sample, log2p1
        sample_qc_cutoffs_df: DataFrame with cutoff values including seq_low_count
    """
    import numpy as np
    import math
    
    # Get the threshold value for horizontal line: log2(seq_low_count + 1)
    seq_low_count = sample_qc_cutoffs_df['seq_low_count'].iloc[0]
    threshold = np.log2(seq_low_count + 1)
    
    # Get unique samples and calculate number of rows needed
    samples = df['sample'].unique()
    n_samples = len(samples)
    n_cols = 3
    n_rows = math.ceil(n_samples / n_cols)
    
    # Calculate y-axis max
    y_max = int(df['log2p1'].max()) + 1
    
    # Create subplots
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        subplot_titles=[str(s) for s in samples],
        vertical_spacing=0.08,
        horizontal_spacing=0.06
    )
    
    # Add scatter plot for each sample
    for idx, sample in enumerate(samples):
        row = (idx // n_cols) + 1
        col = (idx % n_cols) + 1
        
        sample_df = df[df['sample'] == sample]
        
        # Get position range for this sample
        x_min = sample_df['position'].min()
        x_max = sample_df['position'].max()
        
        # Add scatter points
        fig.add_trace(
            go.Scatter(
                x=sample_df['position'],
                y=sample_df['log2p1'],
                mode='markers',
                marker=dict(
                    color='tomato',
                    size=2,
                    opacity=0.8
                ),
                name=sample,
                showlegend=False,
                hovertemplate="Position: %{x}<br>log2(count+1): %{y:.2f}<extra></extra>"
            ),
            row=row,
            col=col
        )
        
        # Add horizontal threshold line
        fig.add_trace(
            go.Scatter(
                x=[x_min, x_max],
                y=[threshold, threshold],
                mode='lines',
                line=dict(color='springgreen', dash='dash', width=1),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=row,
            col=col
        )
        
        # Update x and y axes for each subplot with independent scales
        fig.update_xaxes(
            title_text="",
            tickfont=dict(size=8, weight=700),
            range=[x_min, x_max],
            tickvals=[x_min, x_max],
            tickformat=',d',
            row=row,
            col=col
        )
        fig.update_yaxes(
            range=[0, y_max],
            title_text="",
            tickfont=dict(size=8, weight=700),
            row=row,
            col=col
        )
    
    # Update overall layout
    fig.update_layout(
        title=dict(
            text="Sample QC Position Coverage",
            font=dict(size=12, family="Arial", weight=700)
        ),
        showlegend=False,
        plot_bgcolor='ivory',
        paper_bgcolor='white',
        height=400 * n_rows,
        hovermode='closest'
    )
    
    # Add common axis labels
    fig.add_annotation(
        text="Genomic Coordinate",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.05,
        showarrow=False,
        font=dict(size=12, family="Arial", weight=700),
        xanchor='center'
    )
    
    fig.add_annotation(
        text="log2(count+1)",
        xref="paper",
        yref="paper",
        x=-0.02,
        y=0.5,
        showarrow=False,
        font=dict(size=12, family="Arial", weight=700),
        textangle=-90,
        yanchor='middle'
    )
    
    return fig


def sample_qc_position_anno_plot(df, sample_qc_cutoffs_df):
    
    # Calculate compressed range with small padding
    pos_min = df['position'].min()
    pos_max = df['position'].max()
    padding = (pos_max - pos_min) * 0.02  # 2% padding on each side
    libcounts_pos_range = [pos_min - padding, pos_max + padding]
    
    df['consequence'] = df['consequence'].apply(lambda x: 'LOF' if x == 'LOF' else 'Others')

    samples = [col for col in df.columns if col not in ['position', 'consequence']]
    for sample in samples:
        df[sample] = df[sample] / df[sample].sum() * 100

    df_melted = df.melt(
        id_vars=['position', 'consequence'], 
        value_vars=samples, 
        var_name='sample', 
        value_name='counts'
    )
    df_melted['sample'] = pd.Categorical(df_melted['sample'], categories=samples, ordered=True)
    
    tmp_cutoff = sample_qc_cutoffs_df['low_abundance_per'].iloc[0] * 100
    
    fig = px.scatter(
        df_melted, 
        x="position", 
        y="counts", 
        color="consequence",
        facet_row="sample",
        title="Sample QC Position Percentage",
        template="plotly_white",
        color_discrete_map={
            'LOF': 'rgba(255, 0, 0, 1)',       # Red with full opacity
            'Others': 'rgba(65, 105, 225, 0.2)'  # Royal Blue with 20% opacity
        },
        labels={"position": "Genomic Coordinate", "counts": "Percentage", "consequence": "Type"}
    )
    fig.update_xaxes(
        range=libcounts_pos_range,
        tickvals=[pos_min, pos_max],
        tickformat='d',
        tickfont=dict(size=8, weight=700)
    )
    
    # Calculate y-axis range to include both data and tmp_cutoff
    import numpy as np
    y_min = min(df_melted['counts'].min(), tmp_cutoff * 0.5)
    y_max = max(df_melted['counts'].max(), tmp_cutoff * 2)
    
    fig.update_yaxes(
        type='log',
        range=[np.log10(y_min), np.log10(y_max)],
        tickvals=[0.005, 0.01, 0.05, 0.2, 0.5, 1],
        tickfont=dict(size=8, weight=700)
    )
    fig.update_layout(
        title=dict(text="Sample QC Position Percentage", font=dict(size=12, family="Arial", weight=700)),
        legend_title_text="Type",
        legend=dict(
            font=dict(size=10),
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        plot_bgcolor='ivory',
        paper_bgcolor='white',
        height=300 * len(samples),  # Adjust height based on number of samples (vertical stacking)
        hovermode='closest'
    )
    
    # Add horizontal line at tmp_cutoff (equivalent to geom_hline in R)
    fig.add_hline(
        y=tmp_cutoff,
        line_dash="dash",
        line_color="darkgreen",  # springgreen4 equivalent
        line_width=0.4
    )
    
    return fig
    
def sample_dendogram_plot(sample_data_df, correlation_matrix_df):
    """
    Create a dendrogram plot showing hierarchical clustering of samples
    based on their correlation matrix.
    
    Args:
        sample_data_df: DataFrame with sample information
        correlation_matrix_df: Correlation matrix between samples (samples x samples)
    """
    # Set index to match column names (sample IDs) if not already set
    if len(correlation_matrix_df.index) != len(correlation_matrix_df.columns) or not correlation_matrix_df.index.equals(correlation_matrix_df.columns):
        correlation_matrix_df.index = correlation_matrix_df.columns
    
    # Convert correlation to distance (distance = 1 - correlation)
    distance_matrix = 1 - correlation_matrix_df.values
    
    # Ensure the distance matrix is symmetric and has no negative values
    distance_matrix = np.clip(distance_matrix, 0, None)
    
    # Convert to condensed distance matrix (required for linkage)
    condensed_dist = squareform(distance_matrix, checks=False)
    
    # Perform hierarchical clustering
    linkage_matrix = linkage(condensed_dist, method='complete')
    
    # Get sample labels (the sample IDs)
    labels = correlation_matrix_df.columns.tolist()
    
    # Create dendrogram using scipy to get the structure
    dend = dendrogram(linkage_matrix, labels=labels, orientation='right', no_plot=True)
    
    # Extract dendrogram data
    icoord = np.array(dend['icoord'])
    dcoord = np.array(dend['dcoord'])
    ordered_labels = dend['ivl']
    
    # Create the figure
    fig = go.Figure()
    
    # Add dendrogram lines
    for i in range(len(icoord)):
        fig.add_trace(go.Scatter(
            x=dcoord[i],
            y=icoord[i],
            mode='lines',
            line=dict(color='#CD853F', width=2),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Get the y-positions for labels (from dendrogram structure)
    # Labels appear at positions 5, 15, 25, 35... (increments of 10 in scipy dendrogram)
    label_positions = list(range(5, len(labels) * 10 + 1, 10))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="Sample Dendrogram (Hierarchical Clustering)",
            font=dict(size=18, family="Arial", weight=700)
        ),
        xaxis=dict(
            title="Distance",
            title_font=dict(size=14, family="Arial", weight=700),
            tickfont=dict(size=12),
            side='bottom'
        ),
        yaxis=dict(
            title="",
            tickvals=label_positions,
            ticktext=ordered_labels,
            tickfont=dict(size=10),
            side='left'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=max(400, len(labels) * 30),
        width=800,
        hovermode='closest',
        showlegend=False,
        margin=dict(l=50, r=150, t=80, b=80)  # Extra right margin for labels
    )
    
    return fig

def sample_correlation_plot(correlation_matrix_df):
    """
    Create a correlation heatmap showing pairwise correlations between samples.
    
    Args:
        correlation_matrix_df: Correlation matrix between samples (samples x samples)
                              Can include metadata columns like 'Sample', 'Cluster', etc.
    """
    # If dataframe has a 'Sample' column, use it as index and extract only sample correlation columns
    if 'Sample' in correlation_matrix_df.columns:
        # Get sample IDs that appear in both Sample column and as column names
        sample_ids = correlation_matrix_df['Sample'].tolist()
        # Filter to only columns that are sample IDs (numeric correlation values)
        corr_cols = [col for col in correlation_matrix_df.columns if col in sample_ids]
        # Extract just the correlation matrix part
        corr_matrix = correlation_matrix_df[corr_cols].copy()
        corr_matrix.index = sample_ids
    else:
        # Use as-is if already a pure correlation matrix
        corr_matrix = correlation_matrix_df.copy()
        if len(corr_matrix.index) != len(corr_matrix.columns) or not corr_matrix.index.equals(corr_matrix.columns):
            corr_matrix.index = corr_matrix.columns
    
    # Get sample labels
    sample_labels = corr_matrix.columns.tolist()
    
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=sample_labels,
        y=sample_labels,
        colorscale='RdBu_r',  # Red-Blue reversed (red for high, blue for low)
        zmid=0.5,  # Center the colorscale
        zmin=0.8,  # Min correlation value for color scale
        zmax=1.0,  # Max correlation value
        text=np.round(corr_matrix.values, 2),  # Show correlation values
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(
            title="",
            tickfont=dict(size=12),
            len=0.7
        ),
        hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="Sample Correlation Matrix",
            font=dict(size=18, family="Arial", weight=700),
            y=0.98,  # Position title higher to avoid overlap
            yanchor='top'
        ),
        xaxis=dict(
            title="",
            tickangle=-90,
            tickfont=dict(size=10),
            side='top'
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=10),
            autorange='reversed'  # Reverse y-axis to match typical correlation matrix display
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        width=700,
        margin=dict(l=150, r=100, t=200, b=100)  # Increased top margin for title and x-axis labels
    )
    
    return fig
    

def exp_qc_pca_plot(col_data_df, pca_center_df, pca_scale_df, pca_sdev_df, pca_rotation_df, pca_x_scores_df):
    """
    Create PCA plots showing PC1 vs PC2, PC2 vs PC3, PC1 vs PC3, and variance explained bar chart.
    
    Args:
        col_data_df: DataFrame with sample metadata (should contain 'Day' and 'Replicate' columns)
        pca_center_df: PCA centering values
        pca_scale_df: PCA scaling values
        pca_sdev_df: DataFrame with standard deviations for each PC
        pca_rotation_df: PCA loadings/rotation matrix
        pca_x_scores_df: DataFrame with PCA scores (PC coordinates for each sample)
    """
    # Calculate variance explained from standard deviations
    # Handle different possible formats of pca_sdev_df
    if isinstance(pca_sdev_df, pd.DataFrame):
        # Check for 'sdev' column first
        if 'sdev' in pca_sdev_df.columns:
            sdev_values = pca_sdev_df['sdev'].values
        else:
            # Try to find numeric column with sdev values
            numeric_cols = pca_sdev_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                sdev_values = pca_sdev_df[numeric_cols[0]].values
            else:
                sdev_values = pca_sdev_df.iloc[:, 0].values
    else:
        sdev_values = np.array(pca_sdev_df).astype(float)
    
    sdev_values = np.array(sdev_values, dtype=float)
    variance = sdev_values ** 2
    variance_explained = (variance / variance.sum()) * 100
    
    # Prepare PCA scores dataframe
    pca_scores = pca_x_scores_df.copy()
    
    # Merge with metadata - try different approaches
    if 'Sample' in col_data_df.columns and 'Sample' in pca_scores.columns:
        pca_scores = pca_scores.merge(col_data_df, on='Sample', how='left')
    elif 'Sample' in col_data_df.columns:
        pca_scores = pca_scores.merge(col_data_df, left_index=True, right_on='Sample', how='left')
    else:
        pca_scores = pd.concat([pca_scores.reset_index(drop=True), col_data_df.reset_index(drop=True)], axis=1)
    

    
    # Create 2x2 subplot layout
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PC1 vs PC2', 'PC2 vs PC3', 'PC1 vs PC3', ''),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'bar'}]],
        horizontal_spacing=0.12,
        vertical_spacing=0.12
    )
    
    # Get PC column names
    pc_cols = [col for col in pca_scores.columns if str(col).startswith('PC')]
    if len(pc_cols) < 3:
        pc_cols = pca_scores.columns[:3].tolist()
    
    pc1_col = pc_cols[0] if len(pc_cols) > 0 else 'PC1'
    pc2_col = pc_cols[1] if len(pc_cols) > 1 else 'PC2'
    pc3_col = pc_cols[2] if len(pc_cols) > 2 else 'PC3'
    
    # Determine Day/Condition and Replicate column names (case-insensitive search)
    day_col = None
    rep_col = None
    for col in pca_scores.columns:
        col_lower = str(col).lower()
        if col_lower in ['day', 'timepoint', 'condition']:
            day_col = col
        if col_lower in ['replicate', 'rep']:
            rep_col = col
    
    # Build dynamic color mapping based on unique values in day_col
    base_colors = [
        'rgba(239, 138, 138, 0.8)',   # Salmon/light red
        'rgba(100, 149, 237, 0.8)',   # Cornflower blue
        'rgba(144, 238, 144, 0.8)',   # Light green
        'rgba(255, 215, 0, 0.8)',     # Gold
        'rgba(186, 85, 211, 0.8)',    # Medium orchid
        'rgba(255, 127, 80, 0.8)',    # Coral
    ]
    day_colors = {}
    if day_col:
        unique_days = pca_scores[day_col].unique()
        for i, day in enumerate(sorted(unique_days, key=str)):
            day_colors[str(day)] = base_colors[i % len(base_colors)]
    
    # Build dynamic symbol mapping based on unique values in rep_col
    base_symbols = ['circle', 'square', 'diamond', 'triangle-up', 'cross', 'x']
    replicate_symbols = {}
    if rep_col:
        unique_reps = pca_scores[rep_col].unique()
        for i, rep in enumerate(sorted(unique_reps, key=str)):
            replicate_symbols[str(rep)] = base_symbols[i % len(base_symbols)]
    
    # Track legend items to avoid duplicates
    legend_added = set()
    
    # Function to add scatter traces for a specific PC combination
    def add_pca_scatter(row, col, x_col, y_col, x_label, y_label):
        for _, sample in pca_scores.iterrows():
            day = str(sample.get(day_col, 'Unknown')) if day_col else 'Unknown'
            rep = str(sample.get(rep_col, 'R1')) if rep_col else 'R1'
            
            color = day_colors.get(day, 'rgba(128, 128, 128, 0.8)')
            symbol = replicate_symbols.get(rep, 'circle')
            
            # Create legend name combining day and replicate
            legend_name = f"{day} - {rep}"
            show_legend = legend_name not in legend_added
            if show_legend:
                legend_added.add(legend_name)
            
            fig.add_trace(
                go.Scatter(
                    x=[sample[x_col]],
                    y=[sample[y_col]],
                    mode='markers',
                    marker=dict(
                        color=color,
                        symbol=symbol,
                        size=12,
                        line=dict(color='black', width=1)
                    ),
                    name=legend_name,
                    legendgroup=legend_name,
                    showlegend=show_legend,
                    hovertemplate=f"{x_label}: %{{x:.1f}}<br>{y_label}: %{{y:.1f}}<extra></extra>"
                ),
                row=row, col=col
            )
    
    # Plot PC1 vs PC2 (top left)
    add_pca_scatter(1, 1, pc1_col, pc2_col, 'PC1', 'PC2')
    
    # Plot PC2 vs PC3 (top right)
    add_pca_scatter(1, 2, pc2_col, pc3_col, 'PC2', 'PC3')
    
    # Plot PC1 vs PC3 (bottom left)
    add_pca_scatter(2, 1, pc1_col, pc3_col, 'PC1', 'PC3')
    
    # Add variance explained bar chart (bottom right)
    n_pcs = min(len(variance_explained), 9)
    pc_labels = [f'PC{i+1}' for i in range(n_pcs)]
    
    fig.add_trace(
        go.Bar(
            x=pc_labels,
            y=variance_explained[:n_pcs],
            marker_color='rgba(100, 149, 237, 0.7)',
            text=[f'{v:.1f}%' for v in variance_explained[:n_pcs]],
            textposition='outside',
            textfont=dict(size=9),
            showlegend=False,
            hovertemplate='%{x}: %{y:.1f}%<extra></extra>'
        ),
        row=2, col=2
    )
    
    # Update axes labels
    fig.update_xaxes(title_text='PC1', row=1, col=1)
    fig.update_yaxes(title_text='PC2', row=1, col=1)
    
    fig.update_xaxes(title_text='PC2', row=1, col=2)
    fig.update_yaxes(title_text='PC3', row=1, col=2)
    
    fig.update_xaxes(title_text='PC1', row=2, col=1)
    fig.update_yaxes(title_text='PC3', row=2, col=1)
    
    fig.update_xaxes(title_text='', row=2, col=2)
    fig.update_yaxes(title_text='', ticksuffix='%', row=2, col=2)
    
    # Update overall layout
    fig.update_layout(
        title=dict(
            text='PCA Analysis',
            font=dict(size=18, family='Arial', weight=700)
        ),
        height=700,
        width=1000,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            title=dict(text='Condition / Replicate'),
            font=dict(size=9),
            yanchor='top',
            y=0.45,
            xanchor='left',
            x=1.02,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        showlegend=True
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=True, zerolinecolor='gray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=True, zerolinecolor='gray')
    
    return fig


def plot_expqc_deseq_fc(df, comparison_name, cons=None, ymin=-5, ymax=5):
    """
    Replicate qcplot_expqc_deseq_fc using Plotly.
    
    Parameters:
    -----------
    df : DataFrame with columns ['consequence', 'log2FoldChange', 'stat']
    comparison_name : str, title for the plot
    cons : list, consequences to include (default: Synonymous_Variant, LOF, Missense_Variant)
    ymin, ymax : y-axis limits
    """
    if cons is None:
        cons = ["Synonymous_Variant", "LOF", "Missense_Variant"]
    
    # Filter to selected consequences
    df_filtered = df[df['consequence'].isin(cons)].copy()
    
    # Define colors/sizes by stat level (matches R: non-sig, up, down)
    stat_colors = {
        'non_significant': 'rgba(0,0,0,0.4)',
        'up_regulated': 'rgba(255,0,0,0.8)',
        'down_regulated': 'rgba(154,205,50,0.8)'
    }
    stat_sizes = {
        'non_significant': 4,
        'up_regulated': 8,
        'down_regulated': 8
    }
    
    fig = go.Figure()
    
    # Add violin for each consequence
    for cons_type in cons:
        subset = df_filtered[df_filtered['consequence'] == cons_type]
        
        # Violin trace
        fig.add_trace(go.Violin(
            y=subset['log2FoldChange'],
            name=cons_type,
            side='positive',
            line_color='royalblue',
            fillcolor='rgba(173,216,230,0.5)',
            meanline_visible=False,
            showlegend=False
        ))
        
        # Scatter points (beeswarm-like with jitter)
        for stat_val in subset['stat'].unique():
            stat_subset = subset[subset['stat'] == stat_val]
            jitter = np.random.uniform(-0.15, 0.15, len(stat_subset))
            
            fig.add_trace(go.Scatter(
                x=[cons_type] * len(stat_subset),
                y=stat_subset['log2FoldChange'],
                mode='markers',
                marker=dict(
                    size=stat_sizes.get(stat_val, 4),
                    color=stat_colors.get(stat_val, 'black')
                ),
                name=stat_val,
                showlegend=True,
                customdata=stat_subset.index
            ))
    
    fig.update_layout(
        title=comparison_name,
        yaxis_title='log2FoldChange',
        yaxis=dict(range=[ymin, ymax]),
        plot_bgcolor='ivory',
        violinmode='overlay',
        legend_title='Type'
    )
    
    return fig

# Example usage:
# df = pd.DataFrame({
#     'consequence': ['LOF', 'LOF', 'Synonymous_Variant', ...],
#     'log2FoldChange': [1.5, -0.8, 0.2, ...],
#     'stat': ['up_regulated', 'non_significant', 'down_regulated', ...]
# })
# fig = plot_expqc_deseq_fc(df, "Treatment_vs_Control")
# fig.show()