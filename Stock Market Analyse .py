import tkinter as tk
from tkinter import messagebox, scrolledtext
import yfinance as yf
import requests
import matplotlib.pyplot as plt

NEWS_API_KEY = "f862cff32b874d40887a97aafb513fc0"

def search_stock():
    symbol = entry.get().strip()
    if not symbol:
        result_label.config(text="Please enter a stock symbol.", fg="red")
        return
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("regularMarketPrice", None)
        name = info.get("shortName", "Unknown")
        if price:
            result_label.config(text=f"{name} ({symbol.upper()}): ${price:.2f}", fg="#10b981")
        else:
            result_label.config(text="Invalid symbol or data not available.", fg="red")
    except:
        result_label.config(text="Error retrieving stock data.", fg="red")


def show_stock_chart():
    symbol = entry.get().strip()
    if not symbol:
        messagebox.showwarning("Input Error", "Please enter a stock symbol")
        return
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1mo", interval="1d")
        if history.empty:
            messagebox.showerror("Error", "No historical data found")
            return
        plt.figure(figsize=(8,4))
        plt.plot(history.index, history["Close"], marker='o', color="#3b82f6")
        plt.title(f"{symbol.upper()} - Last 1 Month Price")
        plt.xlabel("Date")
        plt.ylabel("Closing Price (USD)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load chart: {e}")

def plot_3month_pie():
    symbol = entry.get().strip()
    if not symbol:
        messagebox.showwarning("Input Error", "Please enter a stock symbol")
        return
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="3mo", interval="1d")
        if history.empty:
            messagebox.showerror("Error", "No historical data found")
            return
        rise_days = (history['Close'] > history['Open']).sum()
        fall_days = (history['Close'] <= history['Open']).sum()
        plt.figure(figsize=(6,6))
        plt.pie([rise_days, fall_days], labels=["Rise Days", "Fall Days"],
                autopct='%1.1f%%', colors=['#10b981','#ef4444'], startangle=90)
        plt.title("Graph of 3 months")
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to plot pie chart: {e}")

def plot_3years_line():
    symbol = entry.get().strip()
    if not symbol:
        messagebox.showwarning("Input Error", "Please enter a stock symbol")
        return
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="3y", interval="1d")  # exact historical daily data
        if history.empty:
            messagebox.showerror("Error", "No historical data found")
            return
        plt.figure(figsize=(12,6))
        plt.plot(history.index, history["Close"], color="#3b82f6", label="Close Price")
        plt.title(f"Graph of 3 Years - {symbol.upper()}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price (USD)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to plot 3-year graph: {e}")


def get_stock_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "stock market",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5
    }
    try:
        response = requests.get(url, params=params)
        news_text.delete("1.0", tk.END)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            for a in articles:
                news_text.insert(tk.END, f"• {a['title']}\n{a['url']}\n\n")
        else:
            news_text.insert(tk.END, "❌ Failed to fetch news.")
    except:
        news_text.insert(tk.END, "❌ Error fetching news.")

def on_enter(event):
    search_stock()

root = tk.Tk()
root.title("Stock Analyse")
root.geometry("720x750")
root.configure(bg="#1e293b")

title = tk.Label(root, text="Stock Analyse", font=("Helvetica", 24, "bold"), bg="#1e293b", fg="#38bdf8")
title.pack(pady=20)

frame = tk.Frame(root, bg="#334155", padx=20, pady=20)
frame.pack(pady=10)

entry_label = tk.Label(frame, text="Enter Stock Symbol:", font=("Helvetica", 12), bg="#334155", fg="#f8fafc")
entry_label.pack(anchor="w")

entry = tk.Entry(frame, font=("Helvetica", 14), width=30, bg="#f1f5f9", fg="#0f172a")
entry.pack(pady=10)
entry.bind("<Return>", on_enter)

search_button = tk.Button(frame, text="Search Price", font=("Helvetica", 12, "bold"), bg="#3b82f6", fg="white", command=search_stock)
search_button.pack(pady=5)

chart_button = tk.Button(frame, text="📊 Show 1-Month Price Chart", font=("Helvetica", 12, "bold"), bg="#10b981", fg="white", command=show_stock_chart)
chart_button.pack(pady=5)

pie_button = tk.Button(frame, text="🥧 Graph of 3 Months (Rise/Fall)", font=("Helvetica", 12, "bold"), bg="#facc15", fg="#1e293b", command=plot_3month_pie)
pie_button.pack(pady=5)

line3y_button = tk.Button(frame, text="📈 Graph of 3 Years", font=("Helvetica", 12, "bold"), bg="#3b82f6", fg="white", command=plot_3years_line)
line3y_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#1e293b")
result_label.pack(pady=10)

news_title = tk.Label(root, text="📰 Latest Stock Market News", font=("Helvetica", 16, "bold"), bg="#1e293b", fg="#f9fafb")
news_title.pack(pady=(10, 5))

news_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=12, bg="#0f172a", fg="#f1f5f9", font=("Helvetica", 11))
news_text.pack(pady=5)

refresh_button = tk.Button(root, text="🔄 Refresh News", command=get_stock_news, bg="#64748b", fg="white")
refresh_button.pack(pady=(0,20))

get_stock_news()
root.mainloop()
