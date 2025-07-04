# 🌀 SQL Row Streamer (Python Generator)

This project demonstrates how to **stream rows one by one** from a SQL database using a **Python generator**, allowing for memory-efficient processing of large datasets.

---

## 📌 Objective

Create a Python generator function that connects to a MySQL database and yields one row at a time from a query result. This is useful for:

- Efficiently handling large datasets
- Avoiding memory overload
- Integrating with data pipelines or processing loops

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **PyMySQL** – for connecting to MySQL databases
- **MySQL Server**

---

## 🚀 Features

- Connects to a MySQL database
- Executes a given SQL query
- Streams results row by row using a generator
- Closes the connection safely

---

## 📦 Installation

1. **Install Dependencies**

```bash
pip install pymysql
