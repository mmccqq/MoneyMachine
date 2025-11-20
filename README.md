# Stock Dashboard
A stock dashboard project that displays a stock list and K-line graphs. 

# Reasons for choosing this topic

It is thrilling to design and evaluate your own investment strategies, but finding a suitable platform that supports custom calculation methods is time-consuming and most of the platforms are not free. So, why not set up a project tailored to my needs that also solves problems in the real world while allowing me to practice programming skills at the same time? 

This project:

1. provides solid experience in full-stack implementation, covering the entire flow from database to model, controller, view. 

2. makes use of multithreading and concurrency technologies which are skills I want to develop.

3. has strong potential for expansion, including online deployment and full user account support, etc. 

Additionally, there are many open-source stock platforms on github or active ones online where I can learn the best industry practices.

## Features

Includes a simple strategy that identifies potentially favorable stocks for purchase. 

Fetches the latest day-level data and updates the database.

The front-end is 90% completed by AI which is great for accelerating the project and learning the basic front-end knowledge. A breakthrough for a CS student who just took Java/Python and data structure and Algorithm.

## Tech Stack

Frontend: Vite + Vue 3

Backend: Flask

Database: SQLite3

## Project Structure

`stock_list.txt` - Stock list configuration file. 

`app.py` - Flask backend application

`my-project/` - Vue frontend project

`SQL/` - SQL database classes

## Configuration
`stock_list.txt`

To add new stocks, add them to this file. Currently, only Chinese stocks from the Main Board (主板) and ChiNext (创业板) are supported.
Stock IDs should contain only numbers, or numbers prefixed with 'sh' or 'sz'.

Example:

600000

sh600036

sz000001

## How to Run
Start the Flask backend in bash:

  `python app.py`

Start the Vue development server in bash:

  `cd my-project`

  `npm run dev`

Open your browser and navigate to the link as shown in the bash, for example: http://localhost:5174/

You should see the dashboard as shown in the screenshots.

## coming features

1. rewrite the core logic to make it more object-oriented.

2. reduce the times calculation() method needing to fetch data from the database.

3. supports more indicators on the graph.

4. able to review the strategy on the graph.

5. develop more strategies. 
