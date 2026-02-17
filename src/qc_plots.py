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
    