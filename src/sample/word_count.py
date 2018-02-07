
def process(df):
    return df.count()

def run(spark,
        input_text_file):
    df = spark.read.csv(input_text_file)
    count = process(df)
    print(count)
    return count
