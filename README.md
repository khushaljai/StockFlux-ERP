# Price Tracking & Business Analytics Suite

A comprehensive, natively-built Python desktop application designed to track and visually analyze multi-tier product pricing (Retail vs Wholesale vs Market benchmarks). Built entirely on **CustomTkinter** and **SQLite**, it provides highly responsive dashboards, an integrated inventory master catalog, and bidirectional Excel data integrations.

---

## 🌟 Key Features

- **Tri-Model Pricing Engine**: Securely track and separate Retail, Wholesale, Market Price, and MRP at the database level.
- **Dynamic Valuation Dashboard**: Features 7 live-updating metric cards mathematically calculating your **B2B Margins**, **Retail Edge**, and overall **Total Asset Value** in real-time with fluid numerical animations.
- **Three-Line Analytics**: A natively embedded `matplotlib` charting module plotting your competitive historical trends chronologically over your competitors' benchmarks.
- **Master Inventory Catalog**: A giant, searchable unified grid evaluating stock, quantities, variants (like SKU and Pack Size), and flagging critical "Low Stock Alerts" (<10 units).
- **Secure Data Integrations**: Built-in parsers safely map and ingest large CSV/Excel dumps from platforms like *Busy* or *Stocky*. Features an Excel auto-exporter for executive handoffs.
- **Customizable UI**: Fully responsive application window featuring an elegant Dark Mode ecosystem.

---

## 🛠️ Tech Stack & Requirements

### Tech Stack
- **Language**: Python 3.9+
- **GUI Framework**: CustomTkinter
- **Database**: Local SQLite 3
- **Data Engineering**: Pandas, OpenPyXL
- **Analytics**: Matplotlib (TkAgg backend)

### System Requirements
- OS: Windows OS (10/11) / macOS / Linux
- RAM: Minimum 1GB
- Display: Recommended 1200x800 resolution for Master Catalog

---

## 🚀 Setup & Installation

Follow these steps to launch the application locally on your machine.

**1. Clone the repository**
```bash
git clone <repository_url>
cd <repository_folder>
```

**2. Setup a Python Virtual Environment** (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the Application**
```bash
python main.py
```
> Note: The SQLite database (`price_tracker.db`) will auto-initialize seamlessly in the background during your very first launch. 

---

## 📂 Project Structure

```text
├── main.py                      # Main entry point hook
├── database.py                  # SQLite schema definitions & initialization
├── data_engine.py               # Data analytics, CRUD queries, and margin calculation layer
├── importer.py                  # Fault-tolerant CSV/Excel parsing module
├── exporter.py                  # OpenPyXL stylised multi-sheet exporter
├── requirements.txt             # Required Python pip dependencies
├── README.md                    # Project documentation
├── ui/                          
│   ├── app_window.py            # Primary CustomTkinter routing view manager
│   ├── dashboard_frame.py       # Metrics and Matplotlib charting frame
│   ├── inventory_frame.py       # Live Valuation & Master list module  
│   ├── add_entry_frame.py       # Multi-tab logic to create/edit and push prices
│   ├── sync_frame.py            # Import/Export graphical front-end & template generation
│   └── utils.py                 # UI helpers (Dynamic number counter animation framework)
```

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).
