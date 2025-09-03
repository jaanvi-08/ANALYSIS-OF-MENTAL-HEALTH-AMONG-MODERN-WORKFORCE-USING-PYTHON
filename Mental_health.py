import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("mental_health_workforce_dataset.csv")

# Creating Age Groups
data['Age_Group'] = pd.cut(data['Age'], bins=[20,30,40,50,60], labels=['20-30','31-40','41-50','51-60'])

# Menu-driven Filter Application
def apply_filters_menu(df):
    filtered = df.copy()
    while True:
        print("""
--- Filter Menu ---
1. Filter by Department
2. Filter by Age Range
3. Filter by Remote Work
4. Clear All Filters
0. Done
-------------------
""")
        choice = int(input("Choose filter option (0-4): "))
        if choice == 1:
            dept = input("Enter Department: ").strip()
            if dept:
                filtered = filtered[filtered['Department'].str.lower() == dept.lower()]
                print("Filtered to",len(filtered),"records.")
        elif choice == 2:
            min_age = input("Enter minimum age: ").strip()
            max_age = input("Enter maximum age: ").strip()
            if min_age:
                filtered = filtered[filtered['Age'] >= int(min_age)]
            if max_age:
                filtered = filtered[filtered['Age'] <= int(max_age)]
            print("Filtered to",len(filtered),"records.")
        elif choice == 3:
            remote = input("Remote Work? (Yes/No): ").strip()
            if remote:
                filtered = filtered[filtered['Remote_Work'].str.lower() == remote.lower()]
            print("Filtered to",len(filtered),"records.")
        elif choice == 4:
            filtered = df.copy()
            print("All filters cleared.")
        elif choice == 0:
            break
        else:
            print("Invalid choice, try again.")
    return filtered

# Analysis Menu
def show_menu():
    print("""
--- Analysis Menu ---
1. Demographic Overview
2. Mental Health Overview
3. Workplace Factors Analysis
4. Workload Analysis
5. Productivity Insight
6. Department-Wise Stress & Mental Health
7. Age Group-Wise Stress & Mental Health
0. Exit
""")
# Main
while True:
    use_filter = input("Apply filters before analysis? (Yes/No): ").strip()
    if use_filter =='Yes':
        df =apply_filters_menu(data)
    else:
        df = data.copy()
    show_menu()
    choice = int(input("Enter your choice (0-7): "))

    if choice == 1:
        # Demographic Overview
        gender_counts = df['Gender'].value_counts()
        plt.figure(figsize=(6,6))
        plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Gender Distribution')
        plt.show()

        plt.figure(figsize=(8,5))
        plt.hist(df['Age'], bins=15, edgecolor='black')
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Number of Employees')
        plt.show()

        dept_counts = df['Department'].value_counts()
        dept_counts.plot(kind='bar')
        plt.title('Employee Distribution by Department')
        plt.xlabel('Department')
        plt.ylabel('Number of Employees')
        plt.xticks(rotation=45)
        plt.show()

    elif choice == 2:
        # Combined Mental Health Overview
        fig, ax1 = plt.subplots(figsize=(10,6))
        mh_counts = df['Mental_Health_Issues'].value_counts()
        mh_counts.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_xlabel('Mental Health Issues')
        ax1.set_ylabel('Number of Employees')
        ax1.set_title('Mental Health Issues & Stress Level by Status')

        ax2 = ax1.twinx()
        df.boxplot(column='Stress_Level', by='Mental_Health_Issues', ax=ax2)
        ax2.set_ylabel('Stress Level')
        plt.suptitle('')
        plt.tight_layout()
        plt.show()

    elif choice == 3:
        # Workplace Factors
        remote_mental = pd.crosstab(df['Remote_Work'], df['Mental_Health_Issues'])
        remote_mental.plot(kind='bar', stacked=True)
        plt.title('Remote Work vs Mental Health Issues')
        plt.xlabel('Remote Work')
        plt.ylabel('Number of Employees')
        plt.show()

        plt.figure(figsize=(8,5))
        df.boxplot(column='Manager_Support', by='Mental_Health_Issues')
        plt.title('Manager Support vs Mental Health Issues')
        plt.suptitle('')
        plt.xlabel('Mental Health Issues')
        plt.ylabel('Manager Support Level')
        plt.show()

        plt.figure(figsize=(8,5))
        df.boxplot(column='Job_Satisfaction', by='Mental_Health_Issues')
        plt.title('Job Satisfaction vs Mental Health Issues')
        plt.suptitle('')
        plt.xlabel('Mental Health Issues')
        plt.ylabel('Job Satisfaction Level')
        plt.show()

        counsel_mental = pd.crosstab(df['Access_to_Counseling'], df['Mental_Health_Issues'])
        counsel_mental.plot(kind='bar', stacked=True)
        plt.title('Access to Counseling vs Mental Health Issues')
        plt.xlabel('Access to Counseling')
        plt.ylabel('Number of Employees')
        plt.show()

    elif choice == 4:
        # Workload Analysis
        plt.scatter(df['Weekly_Work_Hours'], df['Stress_Level'], alpha=0.5)
        plt.title('Weekly Work Hours vs Stress Level')
        plt.xlabel('Weekly Work Hours')
        plt.ylabel('Stress Level')
        plt.show()

        plt.figure(figsize=(8,5))
        df.boxplot(column='Work_Life_Balance', by='Mental_Health_Issues')
        plt.title('Work Life Balance vs Mental Health Issues')
        plt.suptitle('')
        plt.xlabel('Mental Health Issues')
        plt.ylabel('Work Life Balance Score')
        plt.show()

    elif choice == 5:
        # Productivity Insight
        plt.figure(figsize=(8,5))
        df.boxplot(column='Productivity_Score', by='Mental_Health_Issues')
        plt.title('Productivity Score vs Mental Health Issues')
        plt.suptitle('')
        plt.xlabel('Mental Health Issues')
        plt.ylabel('Productivity Score')
        plt.show()

    elif choice == 6:
        # Department-Wise Analysis
        dept_mental = pd.crosstab(df['Department'], df['Mental_Health_Issues'])
        dept_mental.plot(kind='bar', stacked=True)
        plt.title('Mental Health Issues by Department')
        plt.xlabel('Department')
        plt.ylabel('Number of Employees')
        plt.xticks(rotation=45)
        plt.show()

        dept_stress = df.groupby('Department')['Stress_Level'].mean().sort_values()
        dept_stress.plot(kind='barh')
        plt.title('Average Stress Level by Department')
        plt.xlabel('Average Stress Level')
        plt.ylabel('Department')
        plt.show()

    elif choice == 7:
        # Age Group-Wise Combined Analysis
        fig, ax = plt.subplots(1, 2, figsize=(14, 6))

        age_mental = pd.crosstab(df['Age_Group'], df['Mental_Health_Issues'])
        age_mental.plot(kind='bar', stacked=True, ax=ax[0])
        ax[0].set_title('Mental Health Issues by Age Group')
        ax[0].set_xlabel('Age Group')
        ax[0].set_ylabel('Number of Employees')

        age_stress = df.groupby('Age_Group')['Stress_Level'].mean()
        age_stress.plot(kind='bar', ax=ax[1], color='salmon')
        ax[1].set_title('Average Stress Level by Age Group')
        ax[1].set_xlabel('Age Group')
        ax[1].set_ylabel('Average Stress Level')

        plt.tight_layout()
        plt.show()

    elif choice == 0:
        print("Exiting Analysis Menu. Thank you!")
        break

    else:
        print("Invalid choice. Please select a valid option (0-7).")
