import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="HR Salary Dashboard",
    page_icon="💼",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    font-weight: 700;
}

.kpi {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    text-align: center;
}

.kpi h2 {
    margin: 0;
    font-size: 30px;
}

.kpi p {
    margin: 5px;
    color: gray;
}

</style>
""", unsafe_allow_html=True)


# =========================
# TITLE
# =========================
st.title("💼 HR Salary Analytics Dashboard")
st.caption("Employee Salary & HR Data Analysis")


# =========================
# LOAD DATA
# =========================

FILE_PATH = (r"C:\Users\saanu\Desktop\EXCEL\HR_Salary_Dataset.csv")

try:
    df = pd.read_csv(FILE_PATH)

except Exception as e:
    st.error("CSV file load nahi ho rahi hai.")
    st.code(str(e))
    st.stop()


# =========================
# CLEAN COLUMN NAMES
# =========================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# =========================
# SHOW COLUMNS
# =========================

with st.expander("📋 Dataset Columns"):
    st.write(df.columns.tolist())


# =========================
# FIND IMPORTANT COLUMNS
# =========================

salary_col = None
department_col = None
gender_col = None
experience_col = None
age_col = None

for col in df.columns:

    if "salary" in col:
        salary_col = col

    if "department" in col or "dept" in col:
        department_col = col

    if "gender" in col or "sex" in col:
        gender_col = col

    if "experience" in col or "exp" in col:
        experience_col = col

    if col == "age" or "age" in col:
        age_col = col


# =========================
# CHECK SALARY COLUMN
# =========================

if salary_col is None:

    st.error("Salary column nahi mili.")

    st.write("Available columns:")
    st.write(df.columns.tolist())

    st.stop()


# =========================
# CONVERT SALARY TO NUMBER
# =========================

df[salary_col] = (
    df[salary_col]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("$", "", regex=False)
)

df[salary_col] = pd.to_numeric(
    df[salary_col],
    errors="coerce"
)

df = df.dropna(subset=[salary_col])


# =========================
# SIDEBAR
# =========================

st.sidebar.header("🔎 Filters")


# Department filter
if department_col:

    departments = sorted(
        df[department_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_department = st.sidebar.multiselect(
        "Department",
        departments,
        default=departments
    )

    df = df[
        df[department_col].isin(selected_department)
    ]


# Gender filter
if gender_col:

    genders = sorted(
        df[gender_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_gender = st.sidebar.multiselect(
        "Gender",
        genders,
        default=genders
    )

    df = df[
        df[gender_col].isin(selected_gender)
    ]


# =========================
# KPI CALCULATIONS
# =========================

total_employees = len(df)

avg_salary = df[salary_col].mean()

max_salary = df[salary_col].max()

min_salary = df[salary_col].min()


# =========================
# KPI CARDS
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="kpi">
        <h2>👥 {total_employees}</h2>
        <p>Total Employees</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="kpi">
        <h2>₹{avg_salary:,.0f}</h2>
        <p>Average Salary</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="kpi">
        <h2>₹{max_salary:,.0f}</h2>
        <p>Highest Salary</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="kpi">
        <h2>₹{min_salary:,.0f}</h2>
        <p>Lowest Salary</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================
# SALARY DISTRIBUTION
# =========================

st.subheader("💰 Salary Distribution")

fig = px.histogram(
    df,
    x=salary_col,
    nbins=30,
    title="Salary Distribution",
    labels={salary_col: "Salary"}
)

fig.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================
# DEPARTMENT ANALYSIS
# =========================

if department_col:

    st.subheader("🏢 Department-wise Salary")

    dept_salary = (
        df.groupby(department_col)[salary_col]
        .mean()
        .reset_index()
        .sort_values(salary_col, ascending=False)
    )

    fig = px.bar(
        dept_salary,
        x=department_col,
        y=salary_col,
        text_auto=".2s",
        title="Average Salary by Department"
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# GENDER ANALYSIS
# =========================

if gender_col:

    st.subheader("👨‍💼 Gender Analysis")

    col1, col2 = st.columns(2)

    with col1:

        gender_count = (
            df[gender_col]
            .value_counts()
            .reset_index()
        )

        gender_count.columns = [
            gender_col,
            "count"
        ]

        fig = px.pie(
            gender_count,
            names=gender_col,
            values="count",
            hole=0.5,
            title="Employees by Gender"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        gender_salary = (
            df.groupby(gender_col)[salary_col]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            gender_salary,
            x=gender_col,
            y=salary_col,
            text_auto=".2s",
            title="Average Salary by Gender"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================
# EXPERIENCE ANALYSIS
# =========================

if experience_col:

    st.subheader("📈 Experience vs Salary")

    df[experience_col] = pd.to_numeric(
        df[experience_col],
        errors="coerce"
    )

    experience_data = df.dropna(
        subset=[experience_col]
    )

    fig = px.scatter(
        experience_data,
        x=experience_col,
        y=salary_col,
        trendline="ols",
        title="Experience vs Salary",
        labels={
            experience_col: "Experience",
            salary_col: "Salary"
        }
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# AGE VS SALARY
# =========================

if age_col:

    st.subheader("👤 Age vs Salary")

    df[age_col] = pd.to_numeric(
        df[age_col],
        errors="coerce"
    )

    age_data = df.dropna(
        subset=[age_col]
    )

    fig = px.scatter(
        age_data,
        x=age_col,
        y=salary_col,
        title="Age vs Salary"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# TOP 10 HIGHEST SALARIES
# =========================

st.subheader("🏆 Top 10 Highest Paid Employees")

top10 = (
    df.sort_values(
        salary_col,
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10,
    use_container_width=True
)


# =========================
# DATA TABLE
# =========================

st.subheader("📊 Complete HR Dataset")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)


# =========================
# DOWNLOAD BUTTON
# =========================

csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_hr_salary_data.csv",
    mime="text/csv"
)


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "HR Salary Analytics Dashboard | Python + Pandas + Streamlit + Plotly"
)