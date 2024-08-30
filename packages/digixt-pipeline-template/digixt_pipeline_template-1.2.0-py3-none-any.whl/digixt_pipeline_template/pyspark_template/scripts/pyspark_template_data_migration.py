from pyspark.sql.functions import *
import copy
from pyspark.sql.types import StructType
from pyspark.sql.functions import lit
import time
# Custom Dependencies
# TODO: this is added to help airflow detect common_utils as module
import sys
sys.path.append("/workflows/pyspark_template/")
print("Current working directory:", sys.path)

from common_utils.scripts.common_utilities import CommonLogging, CommonIcebergUtilities
from common_utils.scripts.helper.common_helper_utilities import CommonProcessHelperUtils, CommonAPIUtilities
from common_utils.scripts.data.common_data_utilities import CommonDataUtilities
from common_utils.scripts.s3.common_s3_utilities import CommonS3Utilities

from common_utils.scripts.db_operations.db_operations_factory import DBOperationsFactory
from common_utils.scripts.db_operations.db_operations import BaseDBOperations



logging = CommonLogging.get_logger()

# ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****

MOUNT_BUCKET = '/workflows'

class SparkDataIngestion:
    def read_and_load_data(dbOps: BaseDBOperations, spark, table_name, column_for_partitioning, selected_columns, 
                            lower_bound, upper_bound,  num_partitions, output_warehouse_fq_table, output_wh_table_load_strategy):
        has_data = True
        update_lower_bound=lower_bound
        update_upper_bound=upper_bound
        while has_data:
                logging.info(f">> Iteration : num_partitions: {num_partitions} lower_bound: {update_lower_bound} upper_bound: {update_upper_bound}" )
               
                data_df: DataFrame = dbOps.read_data(table_name=table_name,column_names=selected_columns,column_for_partitioning=column_for_partitioning,
                                        lower_bound=update_lower_bound,upper_bound=update_upper_bound,num_partitions=num_partitions)
                data_df.cache()
                # Spark V 3.1 does not support data_df.isEmpty(), it's new on 3.3
                # count = data_df.count()
                if len(data_df.take(1)) <= 0:
                    has_data = False
                else:
                   
                    data_df = data_df.drop("id")
                    # Adding this to remove duplicates, we may get duplicates
                    data_df = data_df.withColumn("ingested_at", to_timestamp(lit(current_timestamp())))

                    script_adding_columns = ["ingested_at"]
                    logging.info(">> Dataframe schema: " + str(data_df.schema))
                    data_df.show(10)
                    # data_df.writeTo(output_warehouse_fq_table).append()
                    CommonIcebergUtilities.iceberg_load_operation(spark, output_wh_table_load_strategy, data_df,output_warehouse_fq_table,
                                                                         script_adding_columns,merge_data_join_fields=None)
                    update_lower_bound +=upper_bound
                    update_upper_bound +=upper_bound
                data_df.unpersist()

    def run_ingestion_pipeline(output_wh_table_load_strategy, output_warehouse_fq_table, output_table_snapshots_delete_period, db_details):                                             
      
        db_properties = db_details["db_properties"]
        table_name  = db_details["db_table"] 
        column_for_partitioning  = db_details["partitioning_column"] 
        lower_bound  = db_details["lower_bound"] 
        upper_bound  = db_details["upper_bound"] 
        num_partitions  = db_details["num_partitions"] 
        selected_columns  = db_details["selected_columns"] 

        selected_columns = CommonDataUtilities.parse_selected_columns(selected_columns, column_for_partitioning)
        dbOps: BaseDBOperations = DBOperationsFactory().create(db_properties, spark)

        SparkDataIngestion.read_and_load_data(dbOps, spark, table_name, column_for_partitioning, selected_columns, lower_bound, 
                                        upper_bound, num_partitions, output_warehouse_fq_table, output_wh_table_load_strategy)


        warehouse_catalog, warehouse_schema, warehouse_ref_table = output_warehouse_fq_table.split(".")

        CommonIcebergUtilities.optimize_commands(spark, warehouse_catalog, warehouse_schema, warehouse_ref_table)
                                                             

def main():
    try:
       
        project_dir_name = spark_job_args["project_dir_name"]
        db_details = spark_job_args["db_details"]
        
        # Arguments - DW output table
        output_warehouse_fq_table = spark_job_args["output_warehouse_fq_table"]
        output_wh_table_load_strategy = spark_job_args.get("output_wh_table_load_strategy", "APPEND")
        output_table_snapshots_delete_period = spark_job_args.get("output_table_snapshots_delete_period", 60)
        logging.info("""output_warehouse_fq_table: %s, output_wh_table_load_strategy: %s, output_table_snapshots_delete_period: %s
                """.format(output_warehouse_fq_table, output_wh_table_load_strategy, output_table_snapshots_delete_period))

        # Starter spark code  called
        SparkDataIngestion.run_ingestion_pipeline(output_wh_table_load_strategy, output_warehouse_fq_table, 
                                                    output_table_snapshots_delete_period, db_details)

      
    except Exception as ex:
        logging.error(ex)
        sc.stop()
        raise Exception('! Something went wrong with this job')

    finally:
        logging.info('Stopping...')
        sc.stop()


if __name__ == '__main__':
    # Provide Spark Session additional config options as dictionary
    spark_options = {
        "spark.sql.shuffle.partitions": "10",
        "spark.default.parallelism": "10"
    }
    spark, sc, spark_app_name, spark_job_args, cluster_details_spark_args, minio_s3_credentials,\
    credentials ,package_path = CommonProcessHelperUtils.\
                                            initialize_read_arguments(spark_options=spark_options, mount_bucket_name=MOUNT_BUCKET)
    sc.addPyFile(package_path)
    logging.info(f"spark_job_args: {spark_job_args}")

    main()
    exit()
