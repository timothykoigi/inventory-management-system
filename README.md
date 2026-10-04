# Inventory Management System

A beginner-friendly Inventory Management System built with Python and Flask.

The system provides a REST API for managing inventory products and includes a command-line interface that communicates with the Flask API.

It also integrates with the OpenFoodFacts API to search for product information and import products into the inventory.

## Features

- View all inventory products
- View one product
- Add a product
- Update a product using PATCH
- Delete a product
- Search OpenFoodFacts by barcode
- Search OpenFoodFacts by product name
- Import products from OpenFoodFacts
- Command-line interface
- Input validation
- Unit testing
- Git and GitHub version control

## Technologies

- Python 3
- Flask
- Requests
- Pytest
- OpenFoodFacts API
- Git
- GitHub

## Project Structure

```text
inventory-management-system/
├── app.py
├── cli.py
├── test_app.py
├── README.md
├── requirements.txt
└── .gitignore