def compute_kpis(df):
    kpis = {}

    # Example KPIs (modify based on your dataset)
    kpis['Total Rows'] = len(df)
    kpis['Total Columns'] = df.shape[1]

    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        kpis['Average Value'] = df[numeric_cols].mean().mean()

    return kpis