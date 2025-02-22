import requests
from nicegui import ui
import pandas as pd
import plotly.express as px
from typing import Dict, Any

BACKEND_URL = "http://backend:8000/v1"
TICKERS = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "DMART.NS"]


def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
    response = requests.get(
        f"{BACKEND_URL}/price_history",
        params={"ticker": ticker, "start_date": start_date, "end_date": end_date},
    )
    return response.json()


def center_title(fig: px.line, title: str) -> px.line:
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=18, family="Arial"),
        },
    )
    return fig


def show_stock_data() -> None:
    ticker: str = ticker_input.value
    start_date: str = start_date_input.value
    end_date: str = end_date_input.value

    if not ticker or not start_date or not end_date:
        ui.notify("Please enter all required fields!", type="negative")
        return

    with ui.spinner():
        data: Dict[str, Any] = fetch_stock_data(ticker, start_date, end_date)

    if "error" in data:
        ui.notify(data["error"], type="negative")
        return

    df: pd.DataFrame = pd.DataFrame(data["price"])
    df.rename(columns={"date": "Date", "price": "Price"}, inplace=True)
    table_data = df.to_dict(orient="records")

    # Calculate the number of pages
    total_pages = (len(table_data) // 10) + (1 if len(table_data) % 10 != 0 else 0)
    pagination._props["max"] = total_pages  # Update the max pages dynamically
    pagination.update()

    def update_table(page: int) -> None:
        start_index = (page - 1) * 10
        end_index = start_index + 10
        paginated_data = table_data[start_index:end_index]

        table_container.clear()
        with table_container:
            ui.label(f"Showing Data for {data['ticker']}").classes(
                "text-lg font-semibold mt-2 text-center"
            )
            ui.table(
                rows=paginated_data,
                columns=[
                    {"name": "Date", "label": "Date", "field": "Date"},
                    {"name": "Price", "label": "Closing Price", "field": "Price"},
                ],
            ).classes("w-3/4")

    # Initial table update
    update_table(pagination.value)

    # Bind pagination to update the table
    pagination.on("update:model-value", lambda e: update_table(e.args))

    content_container.clear()
    with content_container:
        table_container.clear()
        chart_container.clear()

        with table_container:
            ui.label(f"Showing Data for {data['ticker']}").classes(
                "text-lg font-semibold mt-2 text-center"
            )
            ui.table(
                rows=table_data[:10],  # Show first 10 rows initially
                columns=[
                    {"name": "Date", "label": "Date", "field": "Date"},
                    {"name": "Price", "label": "Closing Price", "field": "Price"},
                ],
            ).classes("w-3/4")

        fig_line: px.line = center_title(
            px.line(
                df,
                x="Date",
                y="Price",
                markers=True,
                color_discrete_sequence=["#4c72b0"],
            ),
            f"{data['ticker']} Stock Trend",
        )

        with chart_container:
            ui.plotly(fig_line).classes("w-2/3")


# UI Layout
with ui.row().classes("items-center justify-center w-full"):
    ui.label("\U0001f4c8 Stock Price Dashboard").classes("text-2xl font-bold mt-4 text-center")

ticker_input = ui.select(TICKERS).classes("w-1/4")
start_date_input = ui.input("Start Date (YYYY-MM-DD)").classes("w-1/4")
end_date_input = ui.input("End Date (YYYY-MM-DD)").classes("w-1/4")

ui.button("Fetch Data", on_click=show_stock_data).classes("mt-4")

content_container = ui.column().classes("items-center w-full")
table_container = ui.column().classes("items-center w-full")

# Add pagination inside a centered row
with ui.row().classes("justify-center w-full mt-4"):
    pagination = ui.pagination(1, 1, direction_links=True)
    # ui.label().bind_text_from(pagination, "value", lambda v: f"Page {v}")

chart_container = ui.row().classes("w-full justify-around")

ui.run(port=8080)
