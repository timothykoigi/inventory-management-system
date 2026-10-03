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
├── .gitignore
├── app.py
├── cli.py
├── test_app.py
├── README.md
└── requirements.txt
```

## Installation

### Clone the Repository

```bash
git clone git@github.com:timothykoigi/inventory-management-system.git
```

### Enter the Project Directory

```bash
cd inventory-management-system
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
```

### Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Check Installed Packages

```bash
pip list
```

## Running the Application

### Start the Flask API

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

### Run the CLI

Open another terminal:

```bash
cd ~/inventory-management-system
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the CLI:

```bash
python cli.py
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/inventory` | Get all products |
| GET | `/inventory/<id>` | Get one product |
| POST | `/inventory` | Add product |
| PATCH | `/inventory/<id>` | Update product |
| DELETE | `/inventory/<id>` | Delete product |
| GET | `/external/barcode/<barcode>` | Search OpenFoodFacts by barcode |
| GET | `/external/search?name=milk` | Search OpenFoodFacts by name |
| POST | `/external/import/<barcode>` | Import OpenFoodFacts product |

## Example POST Request

```json
{
    "name": "Rice",
    "price": 200,
    "quantity": 15,
    "barcode": "",
    "brand": "Local Store"
}
```

## Example PATCH Request

```json
{
    "price": 250,
    "quantity": 20
}
```

## OpenFoodFacts Integration

The project uses OpenFoodFacts to retrieve product information such as:

- Product name
- Brand
- Barcode
- Ingredients
- Quantity

The application supports:

- Searching for products by barcode
- Searching for products by name
- Importing products into the inventory

Internet access is required for live OpenFoodFacts searches.

## Command-Line Interface

The CLI provides the following options:

1. View inventory
2. Add product
3. Update product
4. Delete product
5. Search/import OpenFoodFacts
6. Exit

## Testing

The project uses Pytest for automated testing.

### Run All Tests

```bash
pytest -v
```

### Run Tests Normally

```bash
pytest
```

### Run a Specific Test

```bash
pytest test_app.py::test_add_item -v
```

The test suite covers:

- Flask routes
- CRUD operations
- Input validation
- PATCH updates
- Delete operations
- OpenFoodFacts integration
- External API error handling
- CLI module

## Important Development Commands

### Check Python Version

```bash
python3 --version
```

### Check Flask Version

```bash
flask --version
```

### Check Current Directory

```bash
pwd
```

### List Project Files

```bash
ls
```

### List Files Including Hidden Files

```bash
ls -la
```

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Deactivate Virtual Environment

```bash
deactivate
```

## Git and GitHub Commands

### Initialize Git

```bash
git init
```

### Rename the Branch to Main

```bash
git branch -M main
```

### Check Git Status

```bash
git status
```

### Add All Project Files

```bash
git add .
```

### Add Specific Files

```bash
git add app.py cli.py README.md requirements.txt test_app.py .gitignore
```

### Create a Commit

```bash
git commit -m "feat: build inventory management API"
```

### View Commit History

```bash
git log --oneline
```

### Connect to GitHub

```bash
git remote add origin git@github.com:timothykoigi/inventory-management-system.git
```

### Check GitHub Remote

```bash
git remote -v
```

### Push Code to GitHub

```bash
git push origin main
```

### Pull Changes from GitHub

```bash
git pull origin main
```

## Git Branches

Feature branches can be used to develop different parts of the application.

### Create a Feature Branch

```bash
git checkout -b feature/crud-api
```

### View Branches

```bash
git branch
```

### Switch Back to Main

```bash
git checkout main
```

### Push a Feature Branch

```bash
git push -u origin feature/crud-api
```

### Delete a Local Feature Branch

```bash
git branch -d feature/crud-api
```

## Git Workflow

The project can be developed using the following workflow:

1. Create a feature branch
2. Implement the feature
3. Run the tests
4. Add the changes using `git add`
5. Commit the changes
6. Push the feature branch to GitHub
7. Create a Pull Request
8. Merge the Pull Request into `main`
9. Delete the completed feature branch

Example:

```bash
git checkout -b feature/crud-api
```

Make the changes, then test:

```bash
pytest -v
```

Add and commit the changes:

```bash
git add .
git commit -m "feat: add CRUD inventory endpoints"
```

Push the branch:

```bash
git push -u origin feature/crud-api
```

After the Pull Request is merged, switch back to main:

```bash
git checkout main
```

Update the local main branch:

```bash
git pull origin main
```

Delete the completed local branch:

```bash
git branch -d feature/crud-api
```

## Storage

The current version uses a Python list as temporary storage.

This means inventory changes are lost when the Flask application is restarted.

A database can be added in a future version.

## Complete Development Workflow

### 1. Enter the Project

```bash
cd ~/inventory-management-system
```

### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 3. Check the Project

```bash
git status
```

### 4. Run Tests

```bash
pytest -v
```

### 5. Start the Flask API

```bash
python app.py
```

### 6. Run the CLI

From a second terminal:

```bash
cd ~/inventory-management-system
source .venv/bin/activate
python cli.py
```

### 7. Add Changes to Git

```bash
git add .
```

### 8. Commit Changes

```bash
git commit -m "feat: update inventory management system"
```

### 9. Push to GitHub

```bash
git push origin main
```

## Author

**Timothy Koigi**

Inventory Management System  
Python • Flask • REST API • OpenFoodFacts • Pytest • Git • GitHub