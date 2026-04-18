import pandas as pd
from pathlib import Path


DATA_DIR = Path("/Users/karimkhabib/Downloads/a2_data")
OUTPUT_FILE = Path("/Users/karimkhabib/Downloads/generated_inserts.sql")


TABLES = [
    {
        "csv_file": "DEPARTMENT.csv",
        "table_name": "department",
        "csv_columns": ["ID", "Name", "Building_number", "Room_number"],
        "sql_columns": ["id", "name", "building_number", "room_number"],
    },
    {
        "csv_file": "DOCTOR.csv",
        "table_name": "doctor",
        "csv_columns": [
            "ID", "Full_name", "Specialization", "Phone", "Email",
            "Hire_date", "Licence_number", "Department_ID"
        ],
        "sql_columns": [
            "id", "full_name", "specialization", "phone", "email",
            "hire_date", "licence_number", "department_id"
        ],
    },
    {
        "csv_file": "PATIENT.csv",
        "table_name": "patient",
        "csv_columns": [
            "ID", "Full_name", "National_ID", "Gender", "Date_of_birth",
            "Phone", "Email", "Address"
        ],
        "sql_columns": [
            "id", "full_name", "national_id", "gender", "date_of_birth",
            "phone", "email", "address"
        ],
    },
    {
        "csv_file": "PROCEDURE.csv",
        "table_name": '"procedure"',
        "csv_columns": ["ID", "Name", "Price"],
        "sql_columns": ["id", "name", "price"],
    },
    {
        "csv_file": "APPOINTMENT.csv",
        "table_name": "appointment",
        "csv_columns": ["ID", "Date", "Time", "Status", "Patient_ID", "Doctor_ID"],
        "sql_columns": ["id", "date", "time", "status", "patient_id", "doctor_id"],
    },
    {
        "csv_file": "DIAGNOSIS.csv",
        "table_name": "diagnosis",
        "csv_columns": ["ID", "Title", "Description", "Appointment_ID"],
        "sql_columns": ["id", "title", "description", "appointment_id"],
    },
    {
        "csv_file": "APPOINTMENT_PROCEDURE.csv",
        "table_name": "appointment_procedure",
        "csv_columns": ["Appointment_ID", "Procedure_ID"],
        "sql_columns": ["appointment_id", "procedure_id"],
    },
]


def to_sql_value(value) -> str:
    if pd.isna(value):
        return "NULL"

    if isinstance(value, str):
        escaped = value.replace("'", "''")
        return f"'{escaped}'"

    return str(value)


with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    for table in TABLES:
        csv_path = DATA_DIR / table["csv_file"]
        df = pd.read_csv(csv_path)

        out.write(f"-- {table['table_name']}\n")

        for _, row in df.iterrows():
            values = [to_sql_value(row[col]) for col in table["csv_columns"]]
            columns_sql = ", ".join(table["sql_columns"])
            values_sql = ", ".join(values)

            insert_sql = (
                f"INSERT INTO {table['table_name']} ({columns_sql}) "
                f"VALUES ({values_sql});\n"
            )
            out.write(insert_sql)

        out.write("\n")

print(f"Done. SQL file created: {OUTPUT_FILE}")