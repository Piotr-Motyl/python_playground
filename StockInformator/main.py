import contextlib
import tkinter as tk
import yfinance as yf
import plotly.graph_objects as go

#Defaul/harcoded settings
DEFAULT_FONT = "Helvetica 12"
HISTORY_INTERVAL = "1d"
CHART_INTERVAL = "1d"
HISTORY_PERIOD = "6mo"

# Main window with data to show
main_window = tk.Tk()
main_window.title("*** STOCK INFORMATION ***")

# Top widget to input stock ticker to search
ticker_widget = tk.Frame(main_window)
label_ticker_widget = tk.Label(ticker_widget, font=DEFAULT_FONT, text="Write stock ticker ==>")
label_ticker_widget.pack(side=tk.LEFT)
entry_ticker_widget = tk.Entry(ticker_widget)
entry_ticker_widget.pack(side=tk.RIGHT)
ticker_widget.pack()

# Middle widget to show current price of stock with user ticker
price_widget = tk.Frame(main_window)
label_price_widget = tk.Label(price_widget, font=DEFAULT_FONT, text="Current price ==>")
label_price_widget.pack(side=tk.LEFT)
price_widget.pack()

# Bottom widget with Radiobutton to choose time period for charts
chart_period = tk.StringVar(value="1mo")
period_selection_widget = tk.Frame(main_window)
label_period_widget = tk.Label(period_selection_widget, 
                               font=DEFAULT_FONT, 
                               text="Select chart period: ")
label_period_widget.pack(side=tk.LEFT)

chart_periods_to_choose = [("1 month", "1mo"), ("6 months", "6mo"), ("1 year", "1y")]

# Generating radiobuttons with period of time for chart
for text, period in chart_periods_to_choose:
    radiobutton = tk.Radiobutton(period_selection_widget, text=text, 
                                 variable=chart_period, value=period,
                                 command=lambda: generate_chart(entry_ticker_widget.get(), 
                                                                chart_period.get()))
    radiobutton.pack(side=tk.LEFT)

period_selection_widget.pack()

scrollbar = tk.Scrollbar(main_window)

text_box = tk.Text(main_window, height=15, width=80,
                   padx=5, pady=5, font=DEFAULT_FONT)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=text_box.yview)
text_box.config(yscrollcommand=scrollbar.set)

# Function to download and display data
def download_data(e):
    
    stock_ticker = str(e.widget.get()).upper().strip()
    if not stock_ticker:
        print("---no stock ticker---")
        return

    stock_data = yf.Ticker(stock_ticker)
    print("Downloaded data for: ", stock_ticker, "\n")
    display_stock_info(stock_data, stock_ticker)
    update_price_label(stock_data)  
    generate_chart(stock_ticker, chart_period.get())
# Updating price widget after confirming stock ticker
def update_price_label(stock_data):
    current_price = stock_data.info.get("currentPrice", "N/A")
    currency = stock_data.info.get("currency", "N/A")
    label_price_widget.config(text=f"Current price ==> {current_price} {currency}")

# Showigm full data from Yahoo Finance for user ticker
def display_stock_info(stock_data, stock_ticker):
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, f"Ticker: [{stock_ticker}]" + "\n\n")

    for key, value in stock_data.info.items():
        with contextlib.suppress(Exception):
            text_box.insert(tk.END, f"{key}: {value}\n\n")
    history_stock_data = stock_data.history(period=HISTORY_PERIOD, interval=HISTORY_INTERVAL)
    text_box.insert(tk.END, str(history_stock_data))

#  Generate chaet base on ticker and period of time for chart, period of time from radiobutton
def generate_chart(stock_ticker, chart_period):
    if not stock_ticker:
        return
    
    stock_ticker = str(stock_ticker).upper().strip()

    stock_data = yf.Ticker(stock_ticker)
    chart_data = stock_data.history(period=chart_period, interval=CHART_INTERVAL)

    chart_graf = go.Figure()
    chart_graf.add_trace(go.Candlestick(x=chart_data.index,
                                        open=chart_data["Open"],
                                        high=chart_data["High"],
                                        low=chart_data["Low"],
                                        close=chart_data["Close"],
                                        name="Price chart"))

    stock_currency = stock_data.info.get("currency", "N/A")

    chart_graf.update_layout(
                            title=f"[{stock_ticker}] share price with period [{chart_period}]" + 
                            f" and interval [{CHART_INTERVAL}]",
                            yaxis_title=f"Stock price [{stock_currency}]")
    chart_graf.show()

# Enter key to start download_data function
entry_ticker_widget.bind("<Return>", download_data)
main_window.mainloop()