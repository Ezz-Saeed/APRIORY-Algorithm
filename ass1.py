import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from itertools import combinations
from collections import defaultdict


class Apriori:
    def __init__(self, min_support=0.5, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = []
        self.frequent_itemsets = {}
        self.rules = []

    def read_file(self, file_path, percent=100):
        df = pd.read_csv(file_path)
        df.dropna()
        num_rows = len(df)
        selected_rows = int(num_rows * (percent / 100))
        df = df.head(selected_rows)
        df = df.groupby(['TransactionNo', 'Items']).size().reset_index(name='Count')

        self.transactions = df.groupby('TransactionNo')['Items'].apply(list).tolist()

    def generate_frequent_itemsets(self, order_of_itemet):
        num_transactions = len(self.transactions)

        count_dict = defaultdict(int)

        for transaction in self.transactions:
            item_combinations = combinations(transaction, order_of_itemet)

            for iteset_comination in item_combinations:
                itemset = frozenset(iteset_comination)

                count_dict[itemset] += 1

        frequent_itemsets = {itemset: support for itemset, support in count_dict.items() if
                             support / num_transactions >= self.min_support}

        return frequent_itemsets

    def update_APRRRIORY_frequent_itemsets(self):
        itemset_order = 1
        while True:
            frequent_itemsets = self.generate_frequent_itemsets(itemset_order)
            if not frequent_itemsets:
                break
            self.frequent_itemsets.update(frequent_itemsets)
            itemset_order += 1

    def get_strong_association_rules(self, itemset):
        for i in range(1, len(itemset)):
            for precedent in combinations(itemset, i):
                precedent = frozenset(precedent)
                latter = itemset - precedent

                given_support = self.frequent_itemsets.get(precedent, 0)

                if given_support != 0:
                    confidence = self.frequent_itemsets.get(itemset, 0) / given_support
                    if confidence >= self.min_confidence:
                        self.rules.append((precedent, latter, confidence))
                else:
                    return

    def check_for_association_rules(self):
        for itemset, support in self.frequent_itemsets.items():
            if len(itemset) > 1:
                self.get_strong_association_rules(itemset)

    def print_frequent_itemsets(self):
        output_text = "Frequent Itemsets:\n"
        for itemset, support in self.frequent_itemsets.items():
            output_text += f"{set(itemset)}: {support}\n"
        return output_text

    def print_association_rules(self):
        output_text = "\nAssociation Rules:\n"
        for antecedent, consequent, confidence in self.rules:
            output_text += f"{set(antecedent)} => {set(consequent)} (Confidence: {confidence})\n"
        return output_text


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Apriori Algorithm")
        self.geometry("500x400")
        self.config(bg="lightgray")  # Set background color for the main window

        self.file_path = ""
        self.min_support = tk.DoubleVar()
        self.min_confidence = tk.DoubleVar()
        self.percent = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        label_font = ("Arial", 10)
        entry_font = ("Arial", 10)

        tk.Label(self, text="Select Data File:", bg="lightgray", fg="black", font=label_font).pack(pady=5, anchor="w")
        tk.Button(self, text="Browse", command=self.read_file, bg="blue", fg="white", font=label_font).pack(pady=5, anchor="w")

        tk.Label(self, text="Minimum Support Count (0-1):", bg="lightgray", fg="black", font=label_font).pack(pady=5, anchor="w")
        tk.Entry(self, textvariable=self.min_support, bg="lightblue", fg="red", font=entry_font).pack(pady=5, anchor="w")

        tk.Label(self, text="Minimum Confidence Percentage (0-100):", bg="lightgray", fg="black",
                 font=label_font).pack(pady=5, anchor="w")
        tk.Entry(self, textvariable=self.min_confidence, bg="lightblue", fg="red", font=entry_font).pack(pady=5, anchor="w")

        tk.Label(self, text="Percentage of Data to Read (0-100):", bg="lightgray", fg="black",
                 font=label_font).pack(pady=5, anchor="w")
        tk.Entry(self, textvariable=self.percent, bg="lightblue", fg="red", font=entry_font).pack(pady=5, anchor="w")

        tk.Button(self, text="Execute", command=self.execute, bg="green", fg="white", font=label_font).pack(pady=10, anchor="w")

    def read_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    def execute(self):
        min_support = self.min_support.get()
        min_confidence = self.min_confidence.get()
        percent = self.percent.get()

        if not self.file_path:
            messagebox.showerror("Error", "Select your file.")
            return

        apriori = Apriori(min_support, min_confidence)
        apriori.read_file(self.file_path, percent)
        apriori.update_APRRRIORY_frequent_itemsets()
        apriori.check_for_association_rules()

        output_window = tk.Toplevel(self)
        output_window.title("Apriori Output")
        output_window.geometry("500x400")

        output_text = tk.Text(output_window, height=40, width=100, bg="lightblue", fg="black", font=("Arial", 10))
        output_text.pack(pady=10)

        frequent_itemsets = apriori.print_frequent_itemsets()
        association_rules = apriori.print_association_rules()

        output = frequent_itemsets + association_rules
        output_text.insert(tk.END, output)


def main():
    app = GUI()
    app.mainloop()


if __name__ == "__main__":
    main()
