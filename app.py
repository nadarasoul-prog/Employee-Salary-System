import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# Page Configuration & Session State Setup
# ---------------------------------------------------------
st.set_page_config(page_title="Employee Salary System", page_icon="💼", layout="wide")

# Initialize in-memory storage for up to 10 employees
if "employees" not in st.session_state:
    st.session_state.employees = []

MAX_EMPLOYEES = 10

# Helper function to calculate final salary
def compute_final_salary(basic_salary, hours):
    if hours > 40:
        return basic_salary * 1.10  # 10% bonus
    return basic_salary

# ---------------------------------------------------------
# UI Layout Header
# ---------------------------------------------------------
st.title("💼 Employee Management & Salary Dashboard")
st.markdown("Easily manage employee records, view active staff, and auto-calculate bonuses.")

# Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio(
    "Go to:", 
    ["1. Add Employee", "2. Display Employees", "3. Search Employee", "4. Salary Report"]
)

# Sidebar System Counter Status
st.sidebar.divider()
st.sidebar.metric(
    label="Capacity Status", 
    value=f"{len(st.session_state.employees)} / {MAX_EMPLOYEES}", 
    delta=f"{MAX_EMPLOYEES - len(st.session_state.employees)} slots left"
)

# ---------------------------------------------------------
# Option 1: Add Employee (Modern Form Layout)
# ---------------------------------------------------------
if menu == "1. Add Employee":
    st.subheader("➕ Add New Employee")
    
    if len(st.session_state.employees) >= MAX_EMPLOYEES:
        st.error("System capacity reached! Maximum limit is 10 employees.")
    else:
        # Streamlit Form with structured input grid
        with st.form("add_employee_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                emp_id = st.number_input("Employee ID", min_value=1, step=1, help="Must be greater than 0")
                emp_name = st.text_input("Employee Name", placeholder="e.g. Sarah Ahmed")
                
            with col2:
                basic_salary = st.number_input("Basic Salary ($)", min_value=0.0, step=100.0, format="%.2f")
                working_hours = st.number_input("Working Hours", min_value=0.0, max_value=168.0, step=1.0)

            submit_button = st.form_submit_button(label="Submit Employee Record")

        if submit_button:
            # Form Validation
            existing_ids = [e["ID"] for e in st.session_state.employees]
            if emp_id in existing_ids:
                st.warning(f"An employee with ID {emp_id} already exists!")
            elif len(emp_name.strip()) < 3:
                st.warning("Please enter a valid name (at least 3 characters).")
            else:
                # Add employee to state
                st.session_state.employees.append({
                    "ID": int(emp_id),
                    "Name": emp_name.strip(),
                    "Basic Salary ($)": float(basic_salary),
                    "Working Hours": float(working_hours)
                })
                st.success(f"Employee '{emp_name}' added successfully!")
                st.rerun()

# ---------------------------------------------------------
# Option 2: Display Employees (Interactive Data Table)
# ---------------------------------------------------------
elif menu == "2. Display Employees":
    st.subheader("📋 All Registered Employees")
    
    if not st.session_state.employees:
        st.info("No employees registered yet. Go to 'Add Employee' to start.")
    else:
        df = pd.DataFrame(st.session_state.employees)
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={
                "Basic Salary ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Working Hours": st.column_config.NumberColumn(format="%.1f hrs")
            }
        )

# ---------------------------------------------------------
# Option 3: Search Employee
# ---------------------------------------------------------
elif menu == "3. Search Employee":
    st.subheader("🔍 Search Employee Record")
    
    if not st.session_state.employees:
        st.info("No employees registered yet.")
    else:
        search_id = st.number_input("Enter Employee ID to Search:", min_value=1, step=1)
        search_button = st.button("Search")
        
        if search_button:
            match = next((e for e in st.session_state.employees if e["ID"] == search_id), None)
            
            if match:
                st.success("Employee Found!")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("ID", match["ID"])
                col2.metric("Name", match["Name"])
                col3.metric("Basic Salary", f"${match['Basic Salary ($)']:,.2f}")
                col4.metric("Working Hours", f"{match['Working Hours']} hrs")
            else:
                st.error(f"No employee found with ID {search_id}")

# ---------------------------------------------------------
# Option 4: Calculate Salary Report (Auto-Bonus Highlight)
# ---------------------------------------------------------
elif menu == "4. Salary Report":
    st.subheader("💰 Salary & Overtime Calculation Report")
    
    if not st.session_state.employees:
        st.info("No employees registered yet.")
    else:
        calculated_data = []
        for emp in st.session_state.employees:
            hours = emp["Working Hours"]
            base = emp["Basic Salary ($)"]
            final_salary = compute_final_salary(base, hours)
            bonus_status = "10% Overtime Bonus" if hours > 40 else "Standard Rate"
            
            calculated_data.append({
                "ID": emp["ID"],
                "Name": emp["Name"],
                "Basic Salary ($)": base,
                "Working Hours": hours,
                "Status": bonus_status,
                "Final Salary ($)": final_salary
            })
            
        df_calc = pd.DataFrame(calculated_data)
        
        # Display summary metrics
        st.markdown("#### Summary Insights")
        mcol1, mcol2 = st.columns(2)
        total_payout = df_calc["Final Salary ($)"].sum()
        bonus_count = len(df_calc[df_calc["Working Hours"] > 40])
        
        mcol1.metric("Total Payroll Payout", f"${total_payout:,.2f}")
        mcol2.metric("Employees Eligible for Bonus (>40 hrs)", f"{bonus_count}")
        
        st.divider()
        st.dataframe(
            df_calc,
            use_container_width=True,
            column_config={
                "Basic Salary ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Final Salary ($)": st.column_config.NumberColumn(format="$%.2f"),
            }
        )