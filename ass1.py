import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from itertools import combinations


class Apriori:
    def __init__(self, min_support=0.5, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = []
        self.itemsets = {}
        self.rules = []  # Initialize the rules attribute

    def load_data(self, file_path, percent=100):
        df = pd.read_csv(file_path)
        total_rows = len(df)
        rows_to_read = int(total_rows * (percent / 100))
        df = df.head(rows_to_read)

        self.transactions = df.groupby('TransactionNo')['Items'].apply(list).tolist()

    def get_frequent_itemsets(self, itemset_length):
        itemsets = {}
        transaction_count = len(self.transactions)
        for transaction in self.transactions:
            for item_combo in combinations(transaction, itemset_length):
                itemset = frozenset(item_combo)
                itemsets[itemset] = itemsets.get(itemset, 0) + 1

        frequent_itemsets = {itemset: support for itemset, support in itemsets.items() if
                             support / transaction_count >= self.min_support}
        return frequent_itemsets

    def generate_all_frequent_itemsets(self):
        itemset_length = 1
        while True:
            frequent_itemsets = self.get_frequent_itemsets(itemset_length)
            if not frequent_itemsets:
                break
            self.itemsets.update(frequent_itemsets)
            itemset_length += 1

    def generate_association_rules(self):
        for itemset, support in self.itemsets.items():
            if len(itemset) > 1:
                self.generate_rules_from_itemset(itemset)

    def generate_rules_from_itemset(self, itemset):
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                try:
                    confidence = self.itemsets[itemset] / self.itemsets[antecedent]
                except KeyError:
                    continue
                if confidence >= self.min_confidence:
                    self.rules.append((antecedent, consequent, confidence))

    def print_frequent_itemsets(self):
        output_text = "Frequent Itemsets:\n"
        for itemset, support in self.itemsets.items():
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
        self.geometry("400x300")

        self.file_path = ""
        self.min_support = tk.DoubleVar()
        self.min_confidence = tk.DoubleVar()
        self.percent = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Data File:").pack()
        tk.Button(self, text="Browse", command=self.browse_file).pack()

        tk.Label(self, text="Minimum Support Count (0-1):").pack()
        tk.Entry(self, textvariable=self.min_support).pack()

        tk.Label(self, text="Minimum Confidence Percentage (0-100):").pack()
        tk.Entry(self, textvariable=self.min_confidence).pack()

        tk.Label(self, text="Percentage of Data to Read (0-100):").pack()
        tk.Entry(self, textvariable=self.percent).pack()

        tk.Button(self, text="Run Apriori", command=self.run_apriori).pack()

        self.output_text = tk.Text(self, height=10, width=50)
        self.output_text.pack()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    def run_apriori(self):
        min_support = self.min_support.get()
        min_confidence = self.min_confidence.get()
        percent = self.percent.get()

        if not self.file_path:
            messagebox.showerror("Error", "Please select a data file.")
            return

        apriori = Apriori(min_support, min_confidence)
        apriori.load_data(self.file_path, percent)
        apriori.generate_all_frequent_itemsets()
        apriori.generate_association_rules()

        frequent_itemsets = apriori.print_frequent_itemsets()
        association_rules = apriori.print_association_rules()

        output = frequent_itemsets + association_rules
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, output)


def main():
    app = GUI()
    app.mainloop()


if __name__ == "__main__":
    main()
