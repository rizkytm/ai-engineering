# Module 03: Exercise 01 — Data Engineering Practice

## Part 1: Data Exploration

**Goal**: Load a dataset, explore its structure, and identify issues.

### Tasks

1. **Load the dataset**
   - Download the Titanic dataset from Kaggle or use: `df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")`
   - Load it into a Pandas DataFrame

2. **Explore the structure**
   - Display the first 5 rows with `.head()`
   - Use `.info()` to check data types and non-null counts
   - Use `.describe()` to get statistics for numeric columns
   - Count unique values in categorical columns (`Sex`, `Embarked`, `Pclass`)

3. **Identify issues**
   - How many missing values are in each column? (`isnull().sum()`)
   - Are there duplicate rows?
   - Which columns have the most missing data?
   - What are the data types? Are any incorrect?

4. **Document your findings**
   - Write a short summary (3-5 bullet points) of the main issues you found

---

## Part 2: Data Cleaning

**Goal**: Fix the issues found in Part 1.

### Tasks

1. **Handle missing values**
   - Fill `Age` with the median age
   - Fill `Embarked` with the mode (most frequent value)
   - Drop the `Cabin` column (too many missing values)

2. **Remove duplicates**
   - Check for and remove any duplicate rows

3. **Fix data types**
   - Ensure `Survived` and `Pclass` are appropriate types
   - Convert `Age` to integer after filling nulls

4. **String cleanup**
   - Strip whitespace from `Name` column
   - Standardize `Sex` to lowercase

5. **Save cleaned data**
   - Save to `data/titanic_cleaned.csv`

---

## Part 3: Transformation & Feature Engineering

**Goal**: Transform the cleaned data for ML readiness.

### Tasks

1. **Normalization**
   - Apply MinMaxScaler to `Age` and `Fare` columns
   - Verify the scaled values are between 0 and 1

2. **Encoding**
   - One-hot encode `Sex` and `Embarked` columns
   - Label encode `Pclass` (or keep as-is — justify your choice)

3. **Feature engineering**
   - Create `FamilySize` = `SibSp` + `Parch` + 1
   - Create `IsAlone` = 1 if `FamilySize` == 1, else 0
   - Extract title from `Name` (Mr., Mrs., Miss., Master., etc.)
   - Create `AgeBin` by binning `Age` into groups: child, young_adult, adult, senior

4. **Save transformed data**
   - Save to `data/titanic_transformed.csv`

---

## Part 4: Build a Mini Pipeline

**Goal**: Combine all steps into a single reusable pipeline function.

### Tasks

1. **Create `pipeline.py`**
   - Write functions: `fetch_data()`, `clean_data()`, `transform_data()`, `save_data()`
   - Chain them in a `main()` function
   - Add `if __name__ == "__main__":` guard

2. **Add logging**
   - Print the shape of the DataFrame at each step
   - Print the number of missing values before and after cleaning

3. **Test the pipeline**
   - Run the script and verify the output file is correct
   - Check that the output has no missing values and all expected columns

---

## Bonus Challenge

**Goal**: Fetch data from a public API, clean it, and save it.

### Tasks

1. **Fetch data from an API**
   - Use the JSONPlaceholder API: `https://jsonplaceholder.typicode.com/users`
   - Or use a public dataset API from [OpenML](https://www.openml.org/)

2. **Clean the data**
   - Normalize nested JSON fields
   - Handle any missing or null values
   - Standardize string fields

3. **Save to CSV**
   - Save the cleaned data to `data/api_data_cleaned.csv`

4. **Push to GitHub**
   - Initialize a git repo (if not already)
   - Add `.gitignore` for `data/` if files are large
   - Commit and push your pipeline code (not the data files if >10MB)

---

## Submission Checklist

- [ ] Part 1: Exploration summary document
- [ ] Part 2: `titanic_cleaned.csv` with no missing values
- [ ] Part 3: `titanic_transformed.csv` with encoded features
- [ ] Part 4: `pipeline.py` that runs end-to-end
- [ ] Bonus: API data pipeline (if attempted)
