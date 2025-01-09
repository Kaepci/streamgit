import datetime
import csv
import streamlit as st

class FishStockManagement:
    def __init__(self):
        self.stock = {}

    def add_fish(self, fish_name, quantity):
        if fish_name in self.stock:
            self.stock[fish_name]['quantity'] += quantity
        else:
            self.stock[fish_name] = {
                'quantity': quantity,
                'added_date': datetime.datetime.now()
            }

    def remove_fish(self, fish_name, quantity):
        if fish_name in self.stock and self.stock[fish_name]['quantity'] >= quantity:
            self.stock[fish_name]['quantity'] -= quantity
            if self.stock[fish_name]['quantity'] == 0:
                del self.stock[fish_name]
        else:
            st.error(f"Error: Not enough {fish_name} in stock or fish not found.")

    def view_stock(self):
        if not self.stock:
            st.write("No stock available.")
        else:
            for fish_name, details in self.stock.items():
                st.write(f"- {fish_name}: {details['quantity']} units (Added: {details['added_date']})")

    def upload_dataset(self, file):
        try:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                fish_name = row['fish_name']
                quantity = int(row['quantity'])
                self.add_fish(fish_name, quantity)
            st.success("Dataset successfully uploaded.")
        except KeyError:
            st.error("Dataset must contain 'fish_name' and 'quantity' columns.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

stock_manager = FishStockManagement()

st.title("Fish Stock Management")

menu = ["Add Fish", "Remove Fish", "View Stock", "Upload Dataset"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Fish":
    st.header("Add Fish")
    fish_name = st.text_input("Enter fish name:")
    quantity = st.number_input("Enter quantity to add:", min_value=1, step=1)
    if st.button("Add"):
        stock_manager.add_fish(fish_name, quantity)
        st.success(f"{quantity} {fish_name} added to stock.")

elif choice == "Remove Fish":
    st.header("Remove Fish")
    fish_name = st.text_input("Enter fish name:")
    quantity = st.number_input("Enter quantity to remove:", min_value=1, step=1)
    if st.button("Remove"):
        stock_manager.remove_fish(fish_name, quantity)
        st.success(f"{quantity} {fish_name} removed from stock.")

elif choice == "View Stock":
    st.header("Current Fish Stock")
    stock_manager.view_stock()

elif choice == "Upload Dataset":
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        stock_manager.upload_dataset(uploaded_file)
