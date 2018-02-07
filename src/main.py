#!/usr/bin/python
"""
Main file to load from pyspark. This will be in charge of running the proper job.
"""

# Disable invalid names (we use a lot of names it doesn't like, like 'args'
# pylint:disable=C0103

import argparse
import importlib
import time
import os
import sys

import pyspark
import pyspark.sql

if os.path.exists('libs.zip'):
    sys.path.insert(0, 'libs.zip')
else:
    sys.path.insert(0, './libs')

if os.path.exists('jobs.zip'):
    sys.path.insert(0, 'jobs.zip')
else:
    sys.path.insert(0, './jobs')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a PySpark job')
    parser.add_argument('--job', type=str, required=True, dest='job_name',
                        help="The name of the job module you want to run. "
                             "(ex: poc will run job on jobs.poc package)")
    parser.add_argument('--job-args', nargs='*',
                        help="Extra arguments to send to the PySpark job "
                             "(example: --job-args template=manual-email1 foo=bar")

    args = parser.parse_args()
    print("Called with arguments: %s" % args)

    environment = {
        'PYSPARK_JOB_ARGS': ' '.join(args.job_args) if args.job_args else '',
        'PYTHON_EGG_CACHE': '/tmp/'
    }

    job_args = dict()
    if args.job_args:
        job_args_tuples = [arg_str.split('=') for arg_str in args.job_args]
        print('job_args_tuples: %s' % job_args_tuples)
        job_args = {a[0]: a[1] for a in job_args_tuples}

    print('\nRunning job %s...\nenvironment is %s\n' % (args.job_name, environment))

    os.environ.update(environment)
    sc = pyspark.SparkContext(appName=args.job_name, environment=environment)
    spark = pyspark.sql.SparkSession(sc)
    job_module = importlib.import_module('%s' % args.job_name)

    start = time.time()
    job_module.run(spark, **job_args)
    end = time.time()

print("\nExecution of job %s took %s seconds" % (args.job_name, end-start))