import argparse
import logging
import xml.etree.ElementTree as ET

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


class ParseRowLogicDoFn(beam.DoFn):
    def __init__(self):
        pass

    def get_browser(self, operating_system):
        browsers = {
            "Apple iOS": "Safari",
            "Apple MacOS": "Safari",
            "Google Android": "Google Chrome",
            "Linux": "Firefox",
            "Microsoft Windows": "Microsoft Edge"
        }
        return browsers.get(operating_system, "Brave")

    def process(self, element):
        logging.info(f'Raw element: {element}')
        root = ET.fromstring(element['log'])
        logging.info(f'Root: {root}')
        ret = {'logId': element['id_review']}
        for child in root[0]:
            if child.tag == 'logDate':
                split_date = child.text.split('-')
                ret['logDate'] = f'{split_date[2]}-{split_date[0]}-{split_date[1]}'
            if child.tag == 'device':
                ret['device'] = child.text
            if child.tag == 'location':
                ret['location'] = child.text
            if child.tag == 'os':
                ret['os'] = child.text
            if child.tag == 'ipAddress':
                ret['ipAddress'] = child.text
            if child.tag == 'phoneNumber':
                ret['phoneNumber'] = child.text

        if ret['os']:
            ret['browser'] = self.get_browser(ret['os'])

        logging.info(f'Parsed dict: {ret}')
        return [ret]

def run(argv=None):
    parser = argparse.ArgumentParser()
    _, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    custom_options = pipeline_options.view_as(CustomPipelineOptions)

    std_options = pipeline_options.view_as(StandardOptions)
    std_options.runner = 'DirectRunner'
    
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
                | 'Read from BQ' >> beam.io.ReadFromBigQuery(
                    table='shaped-icon-344520:raw.log_review'
                )
                | 'Parse row' >> beam.ParDo(ParseRowLogicDoFn())
                | 'Write to BQ' >> beam.io.WriteToBigQuery(
                    'shaped-icon-344520:staging.log_review',
                    schema='logId:STRING,logDate:DATE,device:STRING,location:STRING,os:STRING,browser:STRING,ipAddress:STRING,phoneNumber:STRING',
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                    batch_size=50000
                )
                )



if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
