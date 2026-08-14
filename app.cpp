#include <iostream>
using namespace std;


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