import argparse
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import (GoogleCloudOptions,
                                                  PipelineOptions,
                                                  SetupOptions,
                                                  StandardOptions,
                                                  WorkerOptions)

from datetime import datetime


class CustomPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--input', type=str)


class BQStructureDoFn(beam.DoFn):
    def __init__(self):
        pass

    def process(self, element):
        logging.info(f'Raw element: {element}')
        values = element.split(',')
        logging.info(f'Splitted element: {values}')
        try:
            values_dict = {
                'cid': values[0],
                'review_str': values[1],
                'id_review': values[2],
            }
            logging.info(f'Dict element: {values_dict}')
            return [values_dict]
        except:
            logging.info(f'ME MORIIII')
            return []


def run(argv=None):
    parser = argparse.ArgumentParser()
    _, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    custom_options = pipeline_options.view_as(CustomPipelineOptions)

    std_options = pipeline_options.view_as(StandardOptions)
    std_options.runner = 'DataflowRunner'
    
    gcp_options = pipeline_options.view_as(GoogleCloudOptions)
    gcp_options.project = 'shaped-icon-344520'
    gcp_options.region = 'us-central1'
    gcp_options.temp_location = 'gs://rg-acp-storage/tmp'
    pipeline_options.view_as(
        GoogleCloudOptions).staging_location = 'gs://rg-acp-storage/staging'

    worker_options = pipeline_options.view_as(WorkerOptions)
    worker_options.disk_size_gb = 30
    worker_options.num_workers = 1
    worker_options.machine_type = 'n1-standard-1'
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        rows = (p
                | 'Read from GCS' >> beam.io.ReadFromText(custom_options.input, skip_header_lines=1)
                | 'Make BQ structure' >> beam.ParDo(BQStructureDoFn())
                | 'Write to BQ' >> beam.io.WriteToBigQuery(
                    'shaped-icon-344520:raw.movie_review',
                    schema='cid:STRING,review_str:STRING,id_review:STRING',
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                    batch_size=50000
                )
                )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
