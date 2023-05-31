import dash
from dash import dcc
from dash import html
from jupyter_dash import JupyterDash
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import json

app = JupyterDash(__name__, external_stylesheets=[
                  "https://codepen.io/chriddyp/pen/bWLwgP.css"])

app.layout = html.Div([
    html.H1('BMI Calculation', style={'text-align': 'center'}),
    html.Button('Switch to Dark Mode', id='dark-mode-button', n_clicks=0, style={'margin': '0 auto', 'display': 'block',"border-radius": "40px"}),
    html.Div(style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'align-items': 'center'  # Add this line
    }, children=[
        html.Div(style={
            'flex': '1 0 300px',
            'maxWidth': '100%',
            'text-align': 'center' # Add this line
        }, children=[
            html.H2('Possible weight/height combinations', style={'text-align': 'center', 'font-size': '1.75rem',"border-radius": "40px"}),
            dcc.Input(id='input_bmi', type='number',
                      placeholder='Enter BMI', value=20,
                      style={'text-align': 'center',"border-radius": "40px"}),
            dcc.Graph(id='bmi_chart', clear_on_unhover=True),
            html.Div(id='hover-data', style={'display': 'none',"border-radius": "40px"})
        ]),
        html.Div(style={
            'flex': '1 0 300px',
            'margin': '0 auto'
        }, children=[
            html.H2('BMI Calculator', style={'text-align': 'center', 'font-size': '1.75rem',"border-radius": "40px"}),
            html.Div([
                dcc.Input(id='input_height', type='number',
                          placeholder='Enter height (cm)',
                          style={'text-align': 'center',"border-radius": "40px"}),
                dcc.Input(id='input_weight', type='number',
                          placeholder='Enter weight (kg)',
                          style={'text-align': 'center',"border-radius": "40px"}),
            ], style={'text-align': 'center'}),
            html.Div(id='bmi_result', style={'text-align': 'center',"border-radius": "40px"})
        ])
    ])
], id='main-div')

# rest of the code


def calculate_bmi_color(bmi):
    if bmi < 16:
        color = 'Red'
    elif bmi >= 16 and bmi < 17:
        color = 'Orange'
    elif bmi >= 17 and bmi < 18.5:
        color = 'Yellow'
    elif bmi >= 18.5 and bmi < 25:
        color = 'Green'
    elif bmi >= 25 and bmi < 30:
        color = 'Yellow'
    elif bmi >= 30 and bmi < 35:
        color = 'Orange'
    elif bmi >= 35 and bmi < 40:
        color = 'Red'
    else:
        color = 'Purple'
    return color

@app.callback(
    [dash.dependencies.Output('bmi_chart', 'figure'),
     dash.dependencies.Output('hover-data', 'children'),
     dash.dependencies.Output('bmi_chart', 'clickData'),
     dash.dependencies.Output('dark-mode-button', 'children')],
    [dash.dependencies.Input('input_bmi', 'value'),
     dash.dependencies.Input('bmi_chart', 'hoverData'),
     dash.dependencies.Input('bmi_chart', 'clickData'),
     dash.dependencies.Input('dark-mode-button', 'n_clicks')]
)
def update_graph(bmi, hoverData, clickData, n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = None
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    dark_mode = n_clicks % 2 == 1
    
    if bmi is None:
        bmi = 0
    height = [i for i in range(50, 260)]
    weight = [round((bmi * (i/100)**2), 2) for i in height]
    df = pd.DataFrame({'Height (cm)': height, 'Weight (kg)': weight})
    
    color = calculate_bmi_color(bmi)
    
    fig = px.line(df, x='Height (cm)', y='Weight (kg)', title=f'BMI: {bmi}')
    fig.update_traces(line=dict(color=color), mode='lines')
    
    if hoverData is not None:
        x_val = hoverData['points'][0]['x']
        y_val = hoverData['points'][0]['y']
        fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers', marker=dict(color='blue'), showlegend=False, hoverinfo='skip'))
    
    if clickData is not None and input_id != 'input_bmi':
        x_val = clickData['points'][0]['x']
        y_val = clickData['points'][0]['y']
        fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers', marker=dict(color='blue'), showlegend=False, hoverinfo='skip'))
    
    if dark_mode:
        fig.update_layout(
            plot_bgcolor='#000',
            paper_bgcolor='#000',
            font_color='#fff'
        )
    
    return fig, json.dumps(hoverData), None if input_id == 'input_bmi' else dash.no_update, 'Switch to Light Mode' if dark_mode else 'Switch to Dark Mode'


@app.callback(
    dash.dependencies.Output('bmi_result', 'children'),
    [dash.dependencies.Input('input_height', 'value'),
     dash.dependencies.Input('input_weight', 'value')]
)
def update_bmi(height, weight):
    if height is None or weight is None:
        return html.P('Please enter your data')
    height_meters = height / 100
    bmi = round(weight / (height_meters**2), 2)
    
    if bmi < 16:
        result_text = f'Underweight (Severe thinness) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)


        
        
    elif bmi >= 16 and bmi < 17:
        result_text = f'Underweight (Moderate thinness) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    elif bmi >= 17 and bmi < 18.5:
        result_text = f'Underweight (Mild thinness) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    elif bmi >= 18.5 and bmi < 25:
        result_text = f'Normal range ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    elif bmi >= 25 and bmi < 30:
        result_text = f'Overweight (Pre-obese) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    elif bmi >= 30 and bmi < 35:
        result_text = f'Obese (Class I) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    elif bmi >= 35 and bmi < 40:
        result_text = f'Obese (Class II) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    else:
        result_text = f'Obese (Class III) ({bmi:.2f})'
        color = calculate_bmi_color(bmi)
    
    return html.Div([
        html.P(result_text, style={'font-weight': 'bold',
                                   'border-bottom': f'3px solid {color}',
                                   'display': 'inline-block'}),
        html.P('(According to WHO)')
    ])

@app.callback(
    dash.dependencies.Output('bmi_histogram', 'figure'),
    [dash.dependencies.Input('dark-mode-button', 'n_clicks')]
)
def update_histogram(n_clicks):
    dark_mode = n_clicks % 2 == 1
    
    df = pd.read_csv('BMI.csv')

    def calculate_bmi_bin(bmi):
        if bmi < 16:
            return "Underweight (Severe thinness)"
        elif bmi >= 16 and bmi < 17:
            return "Underweight (Moderate thinness)"
        elif bmi >= 17 and bmi < 18.5:
            return "Underweight (Mild thinness)"
        elif bmi >= 18.5 and bmi < 25:
            return "Normal range"
        elif bmi >= 25 and bmi < 30:
            return "Overweight (Pre-obese)"
        elif bmi >= 30 and bmi < 35:
            return "Obese (Class I)"
        elif bmi >= 35 and bmi < 40:
            return "Obese (Class II)"
        else:
            return "Obese (Class III)"

    df['BMI_bin'] = df['BMI'].apply(calculate_bmi_bin)

    bin_counts = df['BMI_bin'].value_counts(normalize=True).sort_index()

    fig = px.bar(bin_counts,
                 labels={'index': 'BMI Range', 'value': 'Frequency'},
                 color=bin_counts.index,
                 color_discrete_sequence=['Red', 'Orange', 'Yellow', 'Green', 'Yellow', 'Orange', 'Red', 'Purple'],
                 category_orders={'index': ["Underweight (Severe thinness)", "Underweight (Moderate thinness)", "Underweight (Mild thinness)", "Normal range", "Overweight (Pre-obese)", "Obese (Class I)", "Obese (Class II)", "Obese (Class III)"]})

    fig.update_yaxes(tickformat=',.0%')
    fig.update_layout(height=700, showlegend=False)
    
    if dark_mode:
        fig.update_layout(
            plot_bgcolor='#000',
            paper_bgcolor='#000',
            font_color='#fff'
        )
    
    return fig

legend_labels = ["Underweight (Severe thinness)", "Underweight (Moderate thinness)", "Underweight (Mild thinness)", "Normal range", "Overweight (Pre-obese)", "Obese (Class I)", "Obese (Class II)", "Obese (Class III)"]
legend_colors = ['Red', 'Orange', 'Yellow', 'Green', 'Yellow', 'Orange', 'Red', 'Purple']

legend_data = []
for label, color in zip(legend_labels, legend_colors):
    legend_data.append(
        html.Div(style={'display': 'flex'}, children=[
            html.Div(style={'background-color': color, 'width': '20px', 'height': '20px'}),
            html.P(label)
        ])
    )



app.layout.children.append(
    html.H2('BMI distribution', style={'text-align': 'center', 'font-size': '1.75rem'})
)

app.layout.children.append(
    dcc.Graph(
        id='bmi_histogram'
    )
)


app.layout.children.append(
    html.Div(
        style={
            'text-align': 'right'
        },
        children=[
            html.A('Processed data source', href='https://www.kaggle.com/datasets/mustafaali96/weight-height'),
            html.Br(),
            html.P('(According to WHO)')
        ]
    )
)
@app.callback(
    [dash.dependencies.Output('main-div', 'style'),
     dash.dependencies.Output('input_bmi', 'style'),
     dash.dependencies.Output('input_height', 'style'),
     dash.dependencies.Output('input_weight', 'style'),
     dash.dependencies.Output('dark-mode-button', 'style')],
    [dash.dependencies.Input('dark-mode-button', 'n_clicks')]
)
def toggle_dark_mode(n_clicks):
    dark_mode = n_clicks % 2 == 1
    if dark_mode:
        main_div_style = {'backgroundColor': '#000', 'color': '#fff', 'borderColor': '#000'}
        input_style = {'backgroundColor': '#000', 'color': '#fff', 'text-align': 'center',"border-radius": "40px"}
        button_style = {'color': '#fff','margin': '0 auto', 'display': 'block',"border-radius": "40px","border-radius": "40px"}
    else:
        main_div_style = {}
        input_style = {'text-align': 'center',"border-radius": "40px"}
        button_style = {'margin': '0 auto', 'display': 'block',"border-radius": "40px"}
    return main_div_style, input_style, input_style, input_style, button_style



app.run_server(host='0.0.0.0')