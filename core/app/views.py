from django.shortcuts import render
from django.shortcuts import render
from django.utils.safestring import mark_safe
import plotly.express as px
from .models import Dash 
from django.db.models import Sum, F, Count
import math
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import seaborn as sns
from . forms import FailureForm,ApprovalForm
import joblib


# Function to generate chart by distribution of the type of machine in the dataset
def generate_chart1_data():
    count_data = (
        Dash.objects.values('Type')
        .annotate(counts=Count('Type'))
        .order_by('-counts')
    )

    labels = [entry['Type'] for entry in count_data]
    values = [entry['counts'] for entry in count_data]

    fig = px.pie(names=labels, values=values)
    fig.update_layout(title='Distribution by the type of Machine')
    chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart

## Function showing bar chart to show the distribution by failure
def generate_chart2_data():
    count_data = (
    Dash.objects.values('type_of_failure')
    .annotate(counts=Count('type_of_failure'))
    .order_by('-counts')
)
    labels = [entry['type_of_failure'] for entry in count_data]
    counts = [entry['counts'] for entry in count_data]

    # Create a bar chart using Plotly Express
    fig = px.bar(x=labels, y=counts, labels={'x': 'Type of Failure', 'y': 'Count'},
                 title='Count of Failures by Type')
    
    fig.update_layout(title='Distribution by the type of Machine')
    chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart

## Function to show a piechart for the distribution on the type of the faliures occured
def generate_chart3_data():
    # excluding the dataset with the datapoints that have actual faliure
    failures = Dash.objects.exclude(type_of_failure='no failure')

    # Perform grouping, counting, and sorting using Django ORM
    count_data = (
        failures.values('type_of_failure')
        .annotate(counts=Count('type_of_failure'))
        .order_by('-counts')
    )
    
    labels = [entry['type_of_failure'] for entry in count_data]
    values = [entry['counts'] for entry in count_data]

    fig = px.pie(names=labels, values=values,hole=0.5)
    fig.update_layout(title='Distribution by the type of actual faliure')
    chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart


## Function to generate boxplots for the columns mentioned below
def generate_chart4_data():
    num_cols = ['Air_temperature', 'Process_temperature', 'Rotational_speed_rpm', 'Torque_Nm', 'Tool_wear_min']

    # Retrieve the data from the database using Django ORM
    data = Dash.objects.all().values(*num_cols)

    fig = go.Figure()

    for col in num_cols:
        fig.add_trace(go.Box(x=[entry[col] for entry in data], name=col))

    fig.update_layout(
        title_text="Box plots"
    )

    chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart

## Checking the outliers in the two columns 
def generate_chart5_data():
    outlier_cols = ['Torque_Nm', 'Rotational_speed_rpm']  # Adjust column names based on your model

    # Retrieve the data from the database using Django ORM
    data = Dash.objects.all().values(*outlier_cols)

    fig2 = make_subplots(rows=1, cols=2, subplot_titles=outlier_cols, vertical_spacing=0.03)

    for i, col in enumerate(outlier_cols):
        # Create a histogram trace for each column
        hist_plot = go.Histogram(x=[entry[col] for entry in data], name=col)
        fig2.add_trace(hist_plot, row=1, col=i+1)

    fig2.update_layout(
        title='Distribution of Torque and Rotational speed',
        yaxis_title='Frequency',
        title_text="Histograms",
        width=900
    )
    chart = fig2.to_html(full_html=False, include_plotlyjs=False)
    return chart

# function to generate the correlation matrix
def generate_chart6_data():
    # Retrieve the data from the database using Django ORM
    data = Dash.objects.all()

    # Convert the data to a DataFrame
    df = pd.DataFrame(list(data.values('Air_temperature', 'Process_temperature', 'Rotational_speed_rpm', 'Torque_Nm', 'Tool_wear_min', 'Machine_failure')))

    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Generate the heatmap using Plotly Express
    fig = px.imshow(corr_matrix, zmin=-1, zmax=1, text_auto=True)

    fig.update_layout(
        title='Correlation Matrix',
        height=600,
        width=800
    )

    chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart

# function to generate the subplots
def generate_chart7_data():
    num_cols = ['Air_temperature', 'Process_temperature', 'Rotational_speed_rpm', 'Torque_Nm', 'Tool_wear_min']

    # Retrieve the data from the database using Django ORM
    data = Dash.objects.all()

    fig = make_subplots(rows=len(num_cols), cols=1, subplot_titles=num_cols, vertical_spacing=0.03, horizontal_spacing=0.01)

    for i, col in enumerate(num_cols):
        # Extract data for the current column using Django ORM methods
        col_data = list(data.values_list(col, flat=True))  # Convert QuerySet to list

        # Create a violin plot trace for the current column
        violin_trace = go.Violin(x=list(data.values_list('Type', flat=True)), y=col_data, name=col, box_visible=True, meanline_visible=True)
        
        # Add the violin plot trace to the figure
        fig.add_trace(violin_trace, row=i+1, col=1)

    fig.update_layout(height=2000, width=800, title_text="Subplots")
    chart = fig.to_html(full_html=False, include_plotlyjs=False)
    
    return chart


def generate_chart9_data(request):
    if request.method == 'POST':
        form = FailureForm(request.POST)
        if form.is_valid():
            type_of_failure = form.cleaned_data['Failure']
            filtered_queryset = Dash.objects.filter(type_of_failure=type_of_failure)
            
            # Convert the filtered queryset to a DataFrame using Pandas
            df_filtered = pd.DataFrame(list(filtered_queryset.values('Type', 'Air_temperature', 'Process_temperature')))
            
            # Group the filtered DataFrame by 'Type' and count occurrences
            df_group = df_filtered.groupby('Type').size().reset_index(name='Counts').sort_values(by='Counts', ascending=False)
            
            # Create line graphs for Air temperature [°C] and Process temperature [°C]
            fig_air = px.line(df_filtered, x=df_filtered.index, y='Air_temperature', 
                              title=f'Line Graph of Air Temperature [°C] for {type_of_failure}',
                              labels={'x': 'Index', 'y': 'Air temperature [°C]'})
            
            fig_process = px.line(df_filtered, x=df_filtered.index, y='Process_temperature', 
                                  title=f'Line Graph of Process Temperature [°C] for {type_of_failure}',
                                  labels={'x': 'Index', 'y': 'Process temperature [°C]'})
            
            # Create bar plot for df_group
            fig_bar = px.bar(df_group, x='Type', y='Counts', title='Bar Plot of Counts by Type',
                             labels={'x': 'Type', 'y': 'Counts'})
            
            # Create subplots with shared x-axis
            fig = make_subplots(rows=1, cols=3, subplot_titles=('Air Temperature [°C]', 'Process Temperature [°C]', 'Counts by Type of machine'))
            
            # Add the line graphs and bar plot to the subplots
            fig.add_trace(fig_air.data[0], row=1, col=1)
            fig.add_trace(fig_process.data[0], row=1, col=2)
            fig.add_trace(fig_bar.data[0], row=1, col=3)

            chart = fig.to_html(full_html=False, include_plotlyjs=False)
            return render(request, 'app/customize_chart.html', {'form': form, 'chart': chart})
    else:
        form = FailureForm()
    
    return render(request, 'app/customize_chart.html', {'form': form})

## Function to render all the charts for EDA
def render_combined_charts(request):
    chart1 = generate_chart1_data()
    chart2 = generate_chart2_data()
    chart3 = generate_chart3_data()
    chart4 = generate_chart4_data()
    chart5 = generate_chart5_data()
    chart6 = generate_chart6_data()
    chart7 = generate_chart7_data()


    context = {
        'chart1': mark_safe(chart1),
        'chart2':mark_safe(chart2),
        'chart3':mark_safe(chart3),
        'chart4':mark_safe(chart4),
        'chart5':mark_safe(chart5),
        'chart6':mark_safe(chart6),
        'chart7':mark_safe(chart7),
    }
    
    return render(request, 'app/chart.html', context)

## function to display homepage
def display_base_html(request):
    return render(request, 'app/base.html')


def approvereject(unit):
    try:
        scalers = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Predictive-maintenence/core/app/scaler.pkl")
        mdl = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Predictive-maintenence/core/app/rf1.pkl")
        # Define the expected column names
        expected_cols = {
            'Rotational_speed_rpm': 'Rotational speed [rpm]',
            'Torque_Nm': 'Torque [Nm]',
            'Tool_wear_min': 'Tool wear [min]',
            'Air_temperature': 'Air temperature [c]',
            'Process_temperature': 'Process temperature [c]'
        }

        # Convert present column names of 'unit' to expected ones
        unit = unit.rename(columns=expected_cols)

        # Drop the 'csrfmiddlewaretoken' column if it exists
        if 'csrfmiddlewaretoken' in unit.columns:
            unit = unit.drop('csrfmiddlewaretoken', axis=1)

        # Only select columns mentioned in scale_cols
        scale_cols = ['Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Air temperature [c]', 'Process temperature [c]']
        unit_scaled = unit[scale_cols]
        X_scaled = scalers.transform(unit_scaled.values)
        y_pred = mdl.pred(X_scaled)


    except Exception as e:
        return str(e)

def cxcontact(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            Type = form.cleaned_data['Type']
            Rotational_speed_rpm=form.cleaned_data['Rotational_speed_rpm']
            Torque_Nm=form.cleaned_data['Torque_Nm']
            Tool_wear_min=form.cleaned_data['Tool_wear_min']
            Air_temperature=form.cleaned_data['Air_temperature']
            Process_temperature=form.cleaned_data['Process_temperature']
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            print(df)
            print(approvereject(df))
					
    form=ApprovalForm()

    return render(request, 'app/form1.html', {'form':form})


