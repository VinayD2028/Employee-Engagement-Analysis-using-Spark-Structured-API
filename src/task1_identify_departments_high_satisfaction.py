# task1_identify_departments_high_satisfaction.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, round as spark_round

def initialize_spark(app_name="Task1_Identify_Departments"):
    """
    Initialize and return a SparkSession.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()
    return spark

def load_data(spark, file_path):
    """
    Load the employee data from a CSV file into a Spark DataFrame.

    Parameters:
        spark (SparkSession): The SparkSession object.
        file_path (str): Path to the employee_data.csv file.

    Returns:
        DataFrame: Spark DataFrame containing employee data.
    """
    schema = "EmployeeID INT, Department STRING, JobTitle STRING, SatisfactionRating INT, EngagementLevel STRING, ReportsConcerns BOOLEAN, ProvidedSuggestions BOOLEAN"
    
    df = spark.read.csv(file_path, header=True, schema=schema)
    return df

def identify_departments_high_satisfaction(df):
    """
    Identify departments with more than 50% of employees having a Satisfaction Rating > 4 and Engagement Level 'High'.

    Parameters:
        df (DataFrame): Spark DataFrame containing employee data.

    Returns:
        DataFrame: DataFrame containing departments meeting the criteria with their respective percentages.
    """
    # TODO: Implement Task 1
    # Steps:
    # 1. Filter employees with SatisfactionRating > 4 and EngagementLevel == 'High'.
    filtered_df = df.filter((col("SatisfactionRating") > 4) & (col("EngagementLevel") == "High"))
    # 2. Calculate the percentage of such employees within each department.
    dept_total = df.groupBy("Department").count().withColumnRenamed("count", "TotalEmployees")
    dept_high_satisfaction = filtered_df.groupBy("Department").count().withColumnRenamed("count", "HighSatisfactionEmployees")
    # 3. Identify departments where this percentage exceeds 50%.
    result_df = dept_high_satisfaction.join(dept_total, "Department") \
        .withColumn("Percentage", spark_round((col("HighSatisfactionEmployees") / col("TotalEmployees")) * 100, 2)) \
        .filter(col("Percentage") > 5) \
        .select("Department", "Percentage")
    # 4. Return the result DataFrame.
    return result_df


def write_output(result_df, output_path):
    """
    Write the result DataFrame to a CSV file.

    Parameters:
        result_df (DataFrame): Spark DataFrame containing the result.
        output_path (str): Path to save the output CSV file.

    Returns:
        None
    """
    result_df.coalesce(1).write.csv(output_path, header=True, mode='overwrite')

def main():
    """
    Main function to execute Task 1.
    """
    # Initialize Spark
    spark = initialize_spark()
    
    # Define file paths
    input_file = "employee_data.csv"
    output_file = "outputs/task1/departments_high_satisfaction.csv"
    
    # Load data
    df = load_data(spark, input_file)
    
    # Perform Task 1
    result_df = identify_departments_high_satisfaction(df)
    
    # Write the result to CSV
    write_output(result_df, output_file)
    
    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
