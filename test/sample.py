from src.sample.word_count import *


def test_word_count_process(spark_session):
    df = spark_session.read.csv('src/resources/word_count.csv')
    count = process(df)
    expected_count = 3

    assert count == expected_count


def test_word_count_job(spark_session):
    count = run(spark_session, 'src/resources/word_count.csv')
    expected_count = 3

    assert count == expected_count
