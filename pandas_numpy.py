import pandas as pd
import numpy as np

data = {
    "Name": ["Amit", "Raj", "Sneha", "Priya", "Kiran", "Vikas", "Meena", "Alok", "Nisha", "Arjun"],
    "Age": [22, 25, 28, 32, 26, 24, 35, 30, 27, 29],
    "Sal": [35000, 50000, 60000, 45000, 70000, 30000, 80000, 55000, 40000, 65000]
}
df = pd.DataFrame(data)
print(df['Name'], "\n")

# Filter rows where Salary > 50000

df_salary = df[df["Sal"] > 50000] 
print("Employees with Salary > 50000\n", df_salary, "\n")

#Filter with 2 conditions (Age > 25 and Salary > 50000)
df_cond = df[(df["Age"] > 25) & (df["Sal"] > 50000)]
print("Employees Age > 25 and Salary > 50000\n", df_cond, "\n")

# Replace "Amit" with "Amit Kumar" within Name column 
df["Name"] = df["Name"].replace("Amit", "Amit Kumar")
df["Sal"] = df["Sal"].replace(35000, 40000)
print("After Replacing Name and Salary\n", df, "\n")

# Append dummy DataFrames
dummy_data = {
    "Name": ["Rohit", "Sunita", "Deepak", "Komal", "Manoj", "Shreya", "Pooja", "Vivek", "Anil", "Seema"],
    "Age": [45, 38, 29, 41, 33, 36, 28, 39, 31, 34],
    "Sal": [10021, 20034, 30045, 40056, 50067, 60078, 70089, 80090, 90012, 11023]
}
df2 = pd.DataFrame(dummy_data)
df_appended = pd.concat([df, df2], ignore_index=True)
print("After Appending Dummy DataFrame\n", df_appended, "\n")