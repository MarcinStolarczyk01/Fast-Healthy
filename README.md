# Fast&Healthy

## Introduction
**Fast&Healthy** is an API designed to create personalized diet plans, no matter your current body goal. It’s not just for people on a strict diet but also for those who struggle with deciding what to eat, which products to buy, and how much to spend on groceries.

Want to gain control over your diet? Follow these steps:
1. Manually add your favorite meals to the recipe database. The more meals you add, the greater the diversity, and the smaller the gap between your declared daily calorie goal and your actual consumption.
2. Set your daily nutritional goals, such as the number of calories to consume and how many meals per day you typically eat.
3. Receive your personalized weekly diet plan in PDF format, export your grocery list, and keep track of your spending.

## Idea
**Fast&Healthy** will be developed in Python for its flexibility and rapid development. 

Recipe ingredient data will be sourced from the **USDA Food Database**. Since the USDA doesn't provide direct access to its database, the Food Data API will be used to extract nutrient information.

The **Fast&Healthy** API will be built using the FastAPI framework, ensuring fast and efficient performance.

Diet optimization will be based on an Evolutionary (Genetic) Algorithm, with the goal of keeping calories and nutrient values close to those specified by the user, while maintaining a level of diet diversity.

## Setup
To set up **Fast&Healthy**, follow those steps:
1. Clone the repository.
   ```bash
   git clone https://github.com/MarcinStolarczyk01/Fast-Healthy.git
   ```
2. [optional] It is recommended to install requirements in an isolated environment. You can create one by running the script below.
   ```bash
   # Install venv package
   pip install virtualenv
   
   # Create new virtual environment under "venv" name
   virtualenv ./venv
   
   # Activate virtual environment
   source ./venv/bin/activate
   ```
   _More about venv package: [Python venv](https://docs.python.org/3/library/venv.html)._\
   _You can also create virtual environment using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-python)._
3. Install all dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API on the local host.
   ```bash
   fastapi dev src/api.py
   ```
5. Open API interactive documentation in your browser. The FastAPI runs at port 8000 by default.\
   Enter the site: [Fast&Healthy API docs](http://localhost:8000/docs)
## Running tests
Confirm that the program is working correctly.
```bash
pytest .
```
## Requirements
To run the Fast&Healthy API and confirm its functionality, ensure you have the following dependencies installed:

### Python Version
- Python >= 3.11

### Dependencies
The required Python packages are listed below.
```plaintext
fastapi[standard]==0.115.4
numpy==2.1.3
pydantic==2.9.2
pytest==8.3.2
Requests==2.32.3
starlette==0.41.2
```
#### Warning! Features mentioned in the *Introduction* section are still under development and are for informational purposes only.
