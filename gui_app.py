import tkinter as tk

from constants import Markets, Headers
from logic_controller import Logic_controller


class Gui_app(tk.Tk):

    def __init__(self):
        super().__init__()

        self.controller = Logic_controller()

        # Setup
        self.title("OB Scanner")
        self.resizable(False, False)
        self.geometry("700x700")

        # Wrapper
        wrapper = tk.Frame(self)
        wrapper.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)
        wrapper.columnconfigure(0, weight=1)
        wrapper.columnconfigure(1, weight=1)
        wrapper.rowconfigure(2, weight=1)

        # Depth input
        depth_input_container = tk.Frame(wrapper)
        depth_input_container.grid(row=0, column=0, sticky=tk.W)

        depth_label = tk.Label(depth_input_container, text="Depth:")
        depth_label.grid(row=0, column=0)

        depth_percent = tk.StringVar(value="10")
        depth_input = tk.Entry(
            depth_input_container, textvariable=depth_percent, width=5, font=("normal", 10))
        depth_input.grid(row=0, column=1)

        percent_label = tk.Label(depth_input_container, text="%")
        percent_label.grid(row=0, column=2)

        # Refresh button
        refresh_btn_container = tk.Frame(wrapper)
        refresh_btn_container.grid(row=0, column=1, sticky=tk.E)

        refresh_btn = tk.Button(refresh_btn_container, text="Refresh",
                                font=("normal, 11"), command=lambda: self.load_table(market_options, depth_percent.get()))
        refresh_btn.grid(row=0, column=0)

        # Markets selector
        markets_container = tk.Frame(wrapper)
        markets_container.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        markets_label = tk.Label(markets_container, text="Markets:")
        markets_label.grid(row=0, column=0)

        market_options = {
            Markets.BTC: tk.IntVar(value=1),
            Markets.ETH: tk.IntVar(),
            Markets.USDT: tk.IntVar(value=1)
        }

        for i, (market, selected) in enumerate(market_options.items()):
            checkbox = tk.Checkbutton(
                markets_container, text=market.value, variable=selected)
            # i + 1 because column 0 is the label
            checkbox.grid(row=0, column=i + 1)

        # Table
        table_outer_container = tk.Frame(wrapper)
        table_outer_container.grid(
            row=2, column=0, columnspan=2, sticky=tk.NSEW)
        table_outer_container.columnconfigure(0, weight=1)
        table_outer_container.rowconfigure(0, weight=1)

        canvas = tk.Canvas(table_outer_container)
        canvas.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = tk.Scrollbar(
            table_outer_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.scrollable_content = tk.Frame(canvas)
        self.scrollable_content.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window(
            (0, 0), window=self.scrollable_content, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        headers = [Headers.SYMBOL, Headers.VOLUME,
                   Headers.DEPTH, Headers.PRICE]

        header_choice = tk.StringVar()
        for i, header in enumerate(headers):
            header_radio = tk.Radiobutton(
                self.scrollable_content, text=header.value, value=header.value, indicatoron=0,
                variable=header_choice, command=lambda: self.sort_table(header_choice.get()))
            header_radio.grid(row=0, column=i, sticky=tk.NSEW)

    def fill_table(self, data):
        for row_counter, ticker in enumerate(data):
            row_data = [ticker.get_name(), ticker.get_volume(),
                        ticker.get_depth(), ticker.get_price()]
            for i, entry_data in enumerate(row_data):
                entry = tk.Entry(
                    self.scrollable_content, width=20, font=("bold, 10"))
                entry.grid(row=row_counter + 1, column=i, sticky=tk.NSEW)
                entry.insert(tk.END, entry_data)
                entry.config(state="readonly")

    def load_table(self, market_options, depth):
        markets_list = [market.value for market,
                        selected in market_options.items() if selected.get()]
        data = self.controller.load_table_data(markets_list, 10)
        self.fill_table(data)

    def sort_table(self, sort_by_header):
        data = self.controller.get_last_table_data()
        if sort_by_header == Headers.SYMBOL.value:
            self.controller.sort_by_symbol(data)
        elif sort_by_header == Headers.VOLUME.value:
            self.controller.sort_by_volume(data)
        elif sort_by_header == Headers.DEPTH.value:
            self.controller.sort_by_depth(data)
        elif sort_by_header == Headers.PRICE.value:
            self.controller.sort_by_price(data)
        self.fill_table(data)
