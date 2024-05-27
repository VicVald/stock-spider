from tkinter import *
from functions import counters, create_graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import csv
import matplotlib.pyplot as plt
import mplcursors

last_frame = ''

root = Tk()
root.attributes('-zoomed', True)
root.resizable(False, False)

def active():
    root.attributes('-zoomed', False)
    #Track the last frame
    global last_frame
    last_frame = 'active_frame'

    active_frame = Frame(root, background='navy')
    txt = Label(
        active_frame,
        text="Actives",
        font=("Helvetica", 40, 'bold'),
        background='navy',
        foreground='RoyalBlue2',
        )
    txt.grid(row=0, column=3, pady=50, padx=20)

    actives = ['MGLU3', 'HAPV3', 'PETR4', 'B3SA3', 'USIM5', 'CIEL3']#, 'COGN3', 'ABEV3', 'PETZ3', 'PCAR3', 'VALE3']
    for active_name in actives:
        index = actives.index(active_name)
        get_into = Button(
            active_frame,
            text=active_name,
            background='RoyalBlue2',
            foreground='white',
            font=("Helvetica", 20),
            border=0,
            highlightthickness=2,
            highlightbackground='RoyalBlue2',
            highlightcolor='WHITE',
            command=lambda index=index: [active_frame.destroy(), inspec(index, actives)]
            )
        get_into.grid(row= 1 + index % 2, column=2 + index % 3, pady=10, padx=5)

    homeButton = Button(
        active_frame,
        text="Home",
        background='navy',
        foreground='white',
        font=("Helvetica", 20),
        border=2,
        relief='flat',
        highlightthickness=2,
        highlightbackground='RoyalBlue2',
        highlightcolor='WHITE',
        command=lambda: [active_frame.destroy(), main()]
        )
    homeButton.grid(row=len(actives) // 3 + 1, column=3, pady=10, padx=20)

    active_frame.pack(fill='both', expand=True)
    active_frame.tkraise()
    



def crypto():
    root.attributes('-zoomed', False)
    #Track the last frame
    global last_frame
    last_frame = 'crypto_frame'

    crypto_frame = Frame(root, background='navy')
    txt = Label(
        crypto_frame,
        text="Cryptos",
        background='navy',
        font=("Helvetica", 40, 'bold'),
        foreground='RoyalBlue2'
        )
    txt.grid(row=0, column=2, pady=50, padx=60)

    cryptos = ["BTC", "ETH", "ADA", "BNB", "USDT", "XRP"]#, "DOGE", "LINK", "LTC", "BCH", "XLM"]
    for crypto_name in cryptos:
        index = cryptos.index(crypto_name)
        get_into = Button(
            crypto_frame,
            text=crypto_name,
            background='RoyalBlue2',
            foreground='white',
            font=("Helvetica", 20),
            border=0,
            highlightthickness=2,
            highlightbackground='RoyalBlue2',
            highlightcolor='WHITE',
            command=lambda index=index: [crypto_frame.destroy(), inspec(index, cryptos)]
            )
        get_into.grid(row= 2 + index % 2, column=1 + index % 3, pady=10, padx=2)

    homeButton = Button(
        crypto_frame,
        text="Home",
        background='navy',
        foreground='white',
        font=("Helvetica", 20),
        border=2,
        relief='flat',
        highlightthickness=2,
        highlightbackground='RoyalBlue2',
        highlightcolor='WHITE',
        command=lambda: [crypto_frame.destroy(), main()]
        )
    homeButton.grid(row=len(cryptos) // 3 + 2, column=2, pady=10, padx=20)

    crypto_frame.pack(fill='both', expand=True)
    crypto_frame.tkraise()
    




def inspec(index, list):
    root.attributes('-zoomed', True)
    root.resizable(True, True)
    #display the counters, graph
    #in acronym put the counters
    global last_frame
    file = ''
    if last_frame == 'crypto_frame':
        file = "crypto.csv"
    elif last_frame == 'active_frame':
        file = "ações.csv"

    index += 1

    inspec_frame = Frame(root, background='navy')
    title = Label(
        inspec_frame,
        text=list[index-1],
        font=("Helvetica", 40, 'bold'),
        foreground='RoyalBlue2',
        background='navy',
        )
    title.pack()

    #Counters
    dataMax, coinMax, dataMin, coinMin, lastCoin = counters(file, index)
    max = Label(
        inspec_frame,
        text=f"Max: {float(coinMax):,.2f} on {dataMax}    |    Min: {float(coinMin):,.2f} on {dataMin}    |    Last: {float(lastCoin):,.2f}",
        font=("Helvetica", 20),
        background='navy',
        foreground='RoyalBlue2',
        )
    max.pack()
    
    today_graph = Frame(
        inspec_frame,
        graphs('today', file, list, inspec_frame, index, coinMax, coinMin),
        background='navy'
        )
    today_graph.pack()

    historic_graph = Frame(
        inspec_frame,
        graphs('historic', file, list, inspec_frame, index),
        background='navy'
        )
    historic_graph.pack()

    homeButton = Button(
        inspec_frame,
        text="Home",
        command=lambda: [inspec_frame.destroy(), main()],
        background='navy',
        foreground='RoyalBlue2',
        font=("Helvetica", 20),
        border=2,
        relief='flat',
        highlightthickness=2,
        highlightbackground='RoyalBlue2',
        highlightcolor='WHITE',
        )
    homeButton.pack()

    inspec_frame.pack(fill='both', expand=True)
    inspec_frame.tkraise()

def graphs(mode, file, list, frame, index, coinMax=None, coinMin=None):
#file = acronym.csv, date = [0] and coinMax = [1] and coinMin = [2] and lastCoin = [3]
#print the tuple of value and date
    if mode == 'today':
        revenue_data = pd.read_csv(file)
        revenue_data = revenue_data.drop_duplicates(subset=[f' {list[index - 1]}'], keep='first')

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(revenue_data['Data'], revenue_data[f' {list[index - 1]}'], marker='o')
        ax.set_title(f'Today {list[index - 1]}')
        ax.tick_params(labelsize=7, axis='x', rotation=45)
        fig.autofmt_xdate()

        #limits
        ax.set_ylim([float(coinMin) - 0.001, float(coinMax) + 0.001])

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='x')

    
    elif mode == 'historic':
        revenue_data = pd.read_csv(f'{list[index-1]}.csv')

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        #y1 = coinMax
        #y2 = coinMin
        #y3 = lastCoin
    
        ax.plot(revenue_data['Data'], revenue_data[' Max'], label='Max', marker='o')
        ax.plot(revenue_data['Data'], revenue_data[' Min'], label='Min', marker='o')
        ax.plot(revenue_data['Data'], revenue_data[' Last'], label='Last', marker='o')

        ax.set_title(f'Historic {list[index-1]}')
        ax.tick_params(labelsize=7, axis='x', rotation=45)
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='x', expand=True)

        ax.legend()
        plt.show()

def center(win):
    # :param win: the main window or Toplevel window to center

    # Apparently a common hack to get the window size. Temporarily hide the
    # window to avoid update_idletasks() drawing the window in the wrong
    # position.
    win.update_idletasks()  # Update "requested size" from geometry manager

    # define window dimensions width and height
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    # Get the window position from the top dynamically as well as position from left or right as follows
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2

    # this is the line that will center your window
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    win.deiconify()

def main():
    #root.attributes('-zoomed', True)
    home = Frame(root, bg='navy')
    txt = Label(
        home,
        text="Stock Spider",
        bg='navy',
        font=("Helvetica", 40, 'bold'),
        foreground='RoyalBlue2',
        border=0,
        )
    txt.grid(row=0, column=3, columnspan=5, pady=150, padx=250)

    activeButton = Button(
        home,
        text="Actives",
        bg='RoyalBlue2',
        foreground='white',
        font=("Helvetica", 20, 'bold'),
        border=0,
        highlightthickness=2,
        highlightbackground='RoyalBlue2',
        highlightcolor='WHITE',
        command=lambda: [active(), home.destroy()]
        )
    activeButton.grid(row=5, column=0,columnspan=3, pady=150, padx=200)

    cryptoButton = Button(
        home,
        text="Cryptos",
        bg='RoyalBlue2',
        foreground='white',
        font=("Helvetica", 20, 'bold'),
        border=0,
        highlightthickness=2,
        highlightbackground='RoyalBlue2',
        highlightcolor='RoyalBlue2',
        command=lambda: [crypto(), home.destroy()]
        )
    cryptoButton.grid(row=5, column=8,columnspan=3, pady=10, padx=200)

    home.pack(
        fill='both',
        expand=True)
    home.tkraise()

    root.title("Stock Spider")
    root.mainloop()

if __name__ == "__main__":
    main()