# Student Management Dashboard
#Live Project - > https://student-management-system-dashboard-nqhr8ssn5typdu7cmawsjh.streamlit.app/
## Overview

The Student Management Dashboard is an interactive data analytics project built using Python, Pandas, Plotly, and Streamlit. The project focuses on data cleaning, exploratory data analysis (EDA), and dashboard development to generate meaningful insights from student data.

## Objectives

* Clean and preprocess raw student data
* Handle missing values and duplicates
* Standardize categorical columns
* Perform exploratory data analysis
* Create interactive visualizations
* Build and deploy a Streamlit dashboard

## Dataset Features

The dataset contains student information such as:

* Student ID
* Name
* Age
* Gender
* Department
* City
* CGPA
* Attendance Percentage
* Total Marks
* Placement Status

## Data Cleaning Steps

### 1. Data Inspection

* Checked dataset structure using Pandas
* Analyzed data types and summary statistics

### 2. Missing Value Handling

* Filled numerical missing values using median
* Filled categorical missing values using mode

### 3. Duplicate Removal

* Identified and removed duplicate records

### 4. Data Type Conversion

* Converted CGPA and Total Marks to numeric format
* Corrected inconsistent data types

### 5. Gender Standardization

Examples:

* male → Male
* female → Female
* m/f values standardized

### 6. Department Standardization

Examples:

* CS → CSE
* Comp Sci → CSE
* Computer Science → CSE

### 7. Placement Status Cleaning

Examples:

* placed → Placed
* UNPLACED → Unplaced

### 8. Attendance Validation

* Identified attendance values above 100%
* Cleaned invalid records

## Dashboard Features

### KPI Cards

* Total Students
* Average CGPA
* Average Attendance
* Total Departments
* Total Cities

### Interactive Filters

* Gender
* Department
* City
* Age Range

### Visualizations

* Gender Distribution
* Department-wise Student Count
* City-wise Student Count
* Age Distribution
* CGPA Distribution
* Attendance Distribution
* Attendance vs CGPA Analysis
* Average CGPA by Department
* Placement Analysis
* Correlation Heatmap

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* GitHub

## Project Structure

Student-Management-Dashboard/

├── app.py

├── student_management_clean.csv

├── requirements.txt

├── README.md

├── images/
```
└── data_cleaning.ipynb
```

## Deployment

The dashboard is deployed using Streamlit Community Cloud.

## Learning Outcomes

Through this project, I learned:

* Data Cleaning and Preprocessing
* Exploratory Data Analysis (EDA)
* Data Visualization
* Interactive Dashboard Development
* Streamlit Deployment
* GitHub Project Management

## Author

Bitu Sahu

B.Tech (AI & Data Science)
