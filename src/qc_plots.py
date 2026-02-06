import plotly.express as px


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