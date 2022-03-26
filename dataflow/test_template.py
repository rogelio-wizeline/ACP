import apache_beam as beam
import argparse
import logging
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions, StandardOptions
from apache_beam.options.value_provider import StaticValueProvider
from apache_beam.io import WriteToText


class CustomPipelineOptions(PipelineOptions):
  @classmethod
  def _add_argparse_args(cls, parser):
    parser.add_value_provider_argument('--to_print', type=str, default='hola')

class OutputValueProviderFn(beam.DoFn):
  def __init__(self, vp):
      self.vp = vp

  def process(self, unused_elm):
      yield self.vp.get()

def run(argv=None):
  parser = argparse.ArgumentParser()
  known_args, pipeline_args = parser.parse_known_args(argv)

  global cloud_options
  global custom_options

  pipeline_options = PipelineOptions(pipeline_args)
  cloud_options = pipeline_options.view_as(GoogleCloudOptions)
  custom_options = pipeline_options.view_as(CustomPipelineOptions)

  pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
  pipeline_options.view_as(GoogleCloudOptions).project = 'shaped-icon-344520'
  pipeline_options.view_as(GoogleCloudOptions).region = 'us-central1'
  pipeline_options.view_as(GoogleCloudOptions).temp_location = 'gs://rg-acp-storage/tmp'
  pipeline_options.view_as(GoogleCloudOptions).staging_location = 'gs://rg-acp-storage/staging'

  pipeline_options.view_as(SetupOptions).save_main_session = True

  with beam.Pipeline(options=pipeline_options) as p:
      rows = (p 
      | 'Create inputs' >> beam.Create(['']) 
      | 'Get value' >> beam.ParDo(OutputValueProviderFn(custom_options.to_print))
      | 'Print value' >> beam.ParDo(lambda x: logging.info(f'-----------------\nx\n-----------------')))

if __name__ == '__main__':
  run()