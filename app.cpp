#include <iostream>
using namespace std;
class employee
{
private:
    int ID;
    string name;
    double salary, working_hour;

public:
    // Constructer
    employee(int ID, string name, double salary, double working_hour)
    {
        this->ID = ID;
        this->name = name;
        this->salary = salary;
        this->working_hour = working_hour;
    }

    void show(int j)
    {
        cout << "\n----------- employee " << j + 1 << " information -----------\n";
        cout << "Name " << j + 1 << ":  " << name << endl;
        cout << "Id " << j + 1 << ":  " << ID << endl;
        cout << "Salary " << j + 1 << ":   " << salary << endl;
        cout << "Working hour " << j + 1 << ":   " << working_hour << endl;
        cout << "---------------------------------------------\n";
    }
};

string names[10];
int ID[10];
double salary[10], work_hour[10];
int employee_num = 0;

void add_employee()
{
    int new_count;
    do {
        cout << "Enter the number of employees to add (1-10): ";
        cin >> new_count;
        if (new_count <= 0) {
            cout << "Invalid count! Please enter a positive number.\n";
        }
    } while (new_count <= 0);

    if (employee_num + new_count > 10) {
        cout << "Space available for only " << (10 - employee_num) << " more employees!\n";
        new_count = 10 - employee_num;
    }

    cin.ignore(); // Clears '\n' left by entering the employee count before entering names

    int start_index = employee_num;
    employee_num += new_count;

    for (int i = start_index; i < employee_num; i++)
    { // Validate names
        do {
            cout << "\nEnter Name " << i + 1 << ": ";
            getline(cin, names[i]);

            if (names[i] == "" || names[i].length() < 3) {
                cout << "Invalid Name! Name cannot be left blank.\n";
            }
        } while (names[i] == "" || names[i].length() < 3);

        // Validate ID
        do {
            cout << "Enter ID " << i + 1 << ": ";
            cin >> ID[i];
            if (ID[i] <= 0) {
                cout << "Invalid ID! ID must be greater than 0.\n";
            }
        } while (ID[i] <= 0);

        // Validate Salary
        do {
            cout << "Enter salary " << i + 1 << ": ";
            cin >> salary[i];
            if (salary[i] < 0) {
                cout << "Invalid Salary! Salary cannot be negative.\n";
            }
        } while (salary[i] < 0);

        // Validate Working Hours
        do {
            cout << "Enter working hour " << i + 1 << ": ";
            cin >> work_hour[i];
            if (work_hour[i] < 0) {
                cout << "Invalid Working Hours! Working hours cannot be negative.\n";
            }
        } while (work_hour[i] < 0);

        cin.ignore(); // Clears '\n' left by work_hour input before the next iteration calls getline()
    }
}
void display_employee()
{
    if (employee_num == 0) {
        cout << "\nNo employees added yet!\n";
        return;
    }

    for (int j = 0; j < employee_num; j++)
    {
        employee emp(ID[j], names[j], salary[j], work_hour[j]);
        emp.show(j);
    }
}

void search_employee()
{
    if (employee_num == 0) {
        cout << "\nNo employees added yet!\n";
        return;
    }

    int search_id;
    bool found = false;

    cout << "Enter Employee ID to search: ";
    cin >> search_id;

    for(int j = 0; j < employee_num; j++)
    {
        if(ID[j] == search_id)
        {
            cout << "\nEmployee Found!";
            employee emp(ID[j], names[j], salary[j], work_hour[j]);
            emp.show(j);
            found = true;
            break;
        }
    }

    if (!found) {
        cout << "\nEmployee with ID " << search_id << " not found!\n";
    }
}

void calculateFinalSalary()
{
    if (employee_num == 0) {
        cout << "\nNo employees added yet!\n";
        return;
    }

    cout << "\n--- Final Calculated Salaries ---\n";
    for (int i = 0; i < employee_num; i++)
    {
        double final_salary = salary[i];
        if (work_hour[i] > 40) {
            final_salary += (salary[i] * 0.10);
        }
        cout << "Employee: " << names[i] << " | ID: " << ID[i]
             << " | Final Salary: " << final_salary << endl;
    }
    cout << "--------------------------------\n";
}

int main()
{
    int num;
    do {
        cout << "\nSystem Options: " << endl;
        cout << "1. Add Employee" << endl;
        cout << "2. Display Employees" << endl;
        cout << "3. Search for Employee" << endl;
        cout << "4. Calculate Salary" << endl;
        cout << "5. Exit" << endl;
        cout << "Select option: ";
        cin >> num;

        if (num == 1)
        {
            add_employee();
        }
        else if (num == 2)
        {
            display_employee();
        }
        else if (num == 3)
        {
            search_employee();
        }
        else if (num == 4)
        {
            calculateFinalSalary();
        }
        else if (num != 5)
        {
            cout << "Invalid Option! Please try again." << endl;
        }

    } while (num != 5);

    return 0;
}