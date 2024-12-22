from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from db_handler import add_expense, get_expenses
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap for styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Personal Expense Tracker"

# Define available categories
categories = ["Food", "Transport", "Shopping", "Entertainment", "Health", "Other"]

# Define the app layout
app.layout = dbc.Container([
    # Header with an image
    dbc.Row([
        dbc.Col(html.Img(src="https://via.placeholder.com/1200x200?text=Personal+Expense+Tracker", style={"width": "100%"}), width=12)
    ], className="mb-4"),
    
    # Expense Input Form
    dbc.Row([
        dbc.Col([
            dbc.Label("Date:"),
            dcc.DatePickerSingle(id="input-date", date=None),
        ], width=4),
        dbc.Col([
            dbc.Label("Category:"),
            dcc.Dropdown(id="input-category", options=[{"label": cat, "value": cat} for cat in categories], placeholder="Select a category"),
        ], width=4),
        dbc.Col([
            dbc.Label("Amount:"),
            dbc.Input(id="input-amount", type="number", placeholder="Enter amount"),
        ], width=4)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Button("Add Expense", id="add-expense-btn", color="primary", n_clicks=0), width=4)
    ], className="mb-4"),

    # Expense Table
    dbc.Row([
        dbc.Col(html.H3("Expense Records"), width=12),
        dbc.Col(html.Div(id="expense-table"), width=12)
    ], className="mb-4"),

    # Export Button
    dbc.Row([
        dbc.Col(dbc.Button("Download CSV", id="download-btn", color="success", n_clicks=0), width=4),
        dcc.Download(id="download-dataframe-csv")
    ], className="mb-4"),

    # Expense Summary Chart
    dbc.Row([
        dbc.Col(html.H3("Expense Summary"), width=12),
        dbc.Col(dcc.Graph(id="expense-summary-chart"), width=12)
    ])
], fluid=True)

# Callback to add expense and update the table and chart
@app.callback(
    Output("expense-table", "children"),
    Output("expense-summary-chart", "figure"),
    Input("add-expense-btn", "n_clicks"),
    State("input-date", "date"),
    State("input-category", "value"),
    State("input-amount", "value")
)
def update_expenses(n_clicks, date, category, amount):
    if n_clicks > 0 and date and category and amount:
        add_expense(date, category, float(amount))  # Add expense to the database

    # Fetch updated data
    expenses = get_expenses()
    df = pd.DataFrame(expenses, columns=["ID", "Date", "Category", "Amount"])

    # Generate expense table
    if not df.empty:
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    else:
        table = html.P("No expenses recorded yet.", style={"textAlign": "center"})

    # Generate summary chart
    summary = df.groupby("Category")["Amount"].sum()
    figure = {
        "data": [{"x": summary.index, "y": summary.values, "type": "bar", "name": "Expenses"}],
        "layout": {"title": "Expenses by Category", "xaxis": {"title": "Category"}, "yaxis": {"title": "Amount"}}
    }

    return table, figure

# Callback to download CSV
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-btn", "n_clicks")
)
def download_csv(n_clicks):
    if n_clicks > 0:
        expenses = get_expenses()
        df = pd.DataFrame(expenses, columns=["ID", "Date", "Category", "Amount"])
        return dcc.send_data_frame(df.to_csv, "expenses.csv")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
