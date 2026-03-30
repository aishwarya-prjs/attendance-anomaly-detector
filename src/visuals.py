import plotly.express as px
import plotly.graph_objects as go

def plot_duration_distribution(df):
    """Plots the distribution of work duration, highlighted by anomaly status."""
    fig = px.histogram(
        df, x="total_work_minutes", color="is_anomaly",
        nbins=30, barmode='overlay',
        labels={'is_anomaly': 'Anomaly', 'total_work_minutes': 'Minutes Worked'},
        color_discrete_map={0: '#636EFA', 1: '#EF553B'}
    )
    fig.update_layout(
        xaxis_title="Minutes Worked",
        yaxis_title="Count",
        showlegend=True
    )
    return fig

def plot_login_vs_duration(df):
    """Plots a scatter of login time vs work duration."""
    fig = px.scatter(
        df, x="login_minutes", y="total_work_minutes", 
        color="is_anomaly",
        hover_data=['employee_id', 'date', 'department'],
        color_discrete_map={0: '#636EFA', 1: '#EF553B'},
        labels={'login_minutes': 'Login (Minutes since midnight)', 'total_work_minutes': 'Work Duration'}
    )
    return fig

def plot_anomalies_by_department(anomaly_df):
    """Bar chart showing anomaly count per department."""
    dept_anom = anomaly_df.groupby('department').size().reset_index(name='count')
    fig = px.bar(
        dept_anom, x='department', y='count', 
        title="Anomalies per Department",
        color='count',
        color_continuous_scale='Reds'
    )
    return fig

def plot_top_employees(anomaly_df):
    """Bar chart showing top 10 employees with flagged logs."""
    emp_anom = anomaly_df.groupby('employee_id').size().reset_index(name='count')
    emp_anom = emp_anom.sort_values('count', ascending=False).head(10)
    fig = px.bar(
        emp_anom, x='employee_id', y='count', 
        title="Top 10 Employees with Flagged Logs",
        color='count',
        color_continuous_scale='Oranges'
    )
    return fig

def plot_anomaly_heatmap(anomaly_df):
    """Heatmap of anomaly concentration by Day and Department."""
    if anomaly_df.empty:
        return None
        
    heat_data = anomaly_df.groupby(['day_of_week', 'department']).size().reset_index(name='count')
    days = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
    heat_data['day_of_week'] = heat_data['day_of_week'].map(days)
    
    fig = px.density_heatmap(
        heat_data, x="day_of_week", y="department", z="count",
        category_orders={"day_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
        color_continuous_scale='Viridis',
        title="Anomaly Concentration (Day vs Department)"
    )
    return fig
