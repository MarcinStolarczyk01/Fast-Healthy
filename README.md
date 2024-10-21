# Fast&Healthy
## Introduction
The solution is an API desired to create your diet plan no mater what is your current body goal. Fast&Healthy is a great product not only for people with strict diet but also for those burning their time on thinking what they want to eat, what products they should buy and how much thei spend on groceries.
You want to gain control? Follow those steps:
1. Manually fill in recipes database with your favourite meals, the more you add the greater diversity and the lower difference between declared daily calorie and actual consumption.
2. Provide basic nutrition values you want to follow daily, for example the number of calories to consume and how many meals per day you are used to eat.
3. Get your personalized weekly diet in PDF format, export grocery list and keep control of your spendings

## Idea
Fast&Healthy will be based on Python for its flexibility and short development time. 
Recipes ingredients data will be provided by usda food database. 
As the usda do not support direct access to their database Food Data API will be used in order to extract information about nutrients.
Fast&Healthy API will be developed using FastAPI framework.
Diet optimization will be based on Evolution (Genetic) algorithm.
The optimization target will be keeping calories and nutrients values as close to those provide by a user while maintaining some level of diet diversity.
## Requirements
- Python3.12
- ...

#### Warning! Features mentioned in _Introduction_ section are under development and have only informational purpose.
