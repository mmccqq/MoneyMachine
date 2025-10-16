# Stock Dashboard
A stock dashboard project that displays a stock list and K-line graphs.

## Features

A simple strategy that identifies potentially favorable stocks for purchase
Fetches the latest day-level data and updates the database

## Tech Stack

Frontend: Vite + Vue 3
Backend: Flask
Database: SQLite3

## Project Structure

stock_list.txt - Stock list configuration file
app.py - Flask backend application
my-project/ - Vue frontend project
SQL/ - SQL database classes

## Configuration
stock_list.txt

To add new stocks, add them to this file. Currently, only Chinese stocks from the Main Board (主板) and ChiNext (创业板) are supported.
Stock IDs should contain only numbers, or numbers prefixed with 'sh' or 'sz'.

Example:
600000
sh600036
sz000001

## How to Run
Start the Flask backend in bash:
  python app.py

Start the Vue development server in bash:
  cd my-project
  npm run dev

Open your browser and navigate to: http://localhost:5174/

You should see the dashboard as shown in the screenshots.