import csv
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def validate_columns(file_path, required_columns):
    print(f"Validating columns in {os.path.basename(file_path)}...")
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        missing = [col for col in required_columns if col not in headers]
        if missing:
            print(f"  Missing columns: {missing}")
            return False
    print("  Columns OK")
    return True


def validate_unique_ids(file_path, id_column):
    print(f"Checking unique IDs in {os.path.basename(file_path)}...")
    seen = set()
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row.get(id_column)
            if not value:
                print("  Empty ID detected")
                return False
            if value in seen:
                print(f"  Duplicate ID detected: {value}")
                return False
            seen.add(value)
    print("  Unique IDs OK")
    return True


def validate_numeric_column(file_path, column_name):
    print(f"Checking numeric values in {column_name} of {os.path.basename(file_path)}...")
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row.get(column_name)
            if value is None:
                print(f"  Missing column: {column_name}")
                return False
            try:
                float(value)
            except ValueError:
                print(f"  Non-numeric value found: {value}")
                return False
    print(f"  {column_name} numeric OK")
    return True


def validate_enum_column(file_path, column_name, allowed_values):
    print(f"Checking allowed values in {column_name} of {os.path.basename(file_path)}...")
    bad = {}
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row.get(column_name)
            if value is None:
                print(f"  Missing column: {column_name}")
                return False
            value = value.strip()
            if value not in allowed_values:
                bad[value] = bad.get(value, 0) + 1
                if len(bad) >= 10:
                    break
    if bad:
        print(f"  Unexpected values found (showing up to 10): {bad}")
        return False
    print(f"  {column_name} values OK")
    return True


def main():
    success = True

    answerbench = os.path.join(BASE_DIR, "answerbench_v2.csv")
    proofbench = os.path.join(BASE_DIR, "proofbench.csv")
    gradingbench = os.path.join(BASE_DIR, "gradingbench.csv")

    success &= validate_columns(
        answerbench,
        ["Problem ID", "Problem", "Short Answer", "Category", "Subcategory", "Source"],
    )
    success &= validate_unique_ids(answerbench, "Problem ID")

    success &= validate_columns(
        proofbench,
        ["Problem ID", "Problem", "Solution", "Grading guidelines", "Category", "Level", "Short Answer", "Source"],
    )
    success &= validate_unique_ids(proofbench, "Problem ID")

    success &= validate_columns(
        gradingbench,
        ["Grading ID", "Problem ID", "Problem", "Solution", "Grading guidelines", "Response", "Points", "Reward", "Problem Source"],
    )
    success &= validate_unique_ids(gradingbench, "Grading ID")
    success &= validate_numeric_column(gradingbench, "Points")
    success &= validate_enum_column(
        gradingbench,
        "Reward",
        {"Correct", "Incorrect", "Partial", "Almost"},
    )

    if not success:
        print("\nValidation failed.")
        sys.exit(1)

    print("\nAll validations passed.")


if __name__ == "__main__":
    main()

