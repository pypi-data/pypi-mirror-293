import os
from argparse import ArgumentParser

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser(description='DFY Pusher')
  parser.add_argument('--dfy-sql', **env('DFY_SQL'), help='DFY SQL connection string')
  parser.add_argument('--dfy-blobs', **env('DFY_BLOBS'), help='DFY Blobs KV connection string')
  parser.add_argument('--pipeline', **env('PIPELINE_ENDPOINT'), help='Pipeline endpoint')
  parser.add_argument('--token', **env('PIPELINE_TOKEN'), help='Pipeline token')
  parser.add_argument('--core-meta', **env('CORE_META'), help='Core metadata KV connection string')
  parser.add_argument('--core-blobs', **env('CORE_BLOBS'), help='Core blobs KV connection string')


  args = parser.parse_args()
  endpoint = args.pipeline.rstrip('/')

  from dslog import Logger
  logger = Logger.click().prefix('[PUSHER]')
  logger(f'Starting pusher...')
  logger(f'- Endpoint: {args.pipeline}')

  import asyncio
  from kv import KV, ClientKV
  from sqlmodel import create_engine
  from pipeteer import http
  from moveread.core import Core
  from moveread.pipelines.dfy import DFYPipeline
  from moveread.dfy_connector import Pusher

  HEADERS = { 'Authorization': f'Bearer {args.token}' }
  req = http.bound_request(headers=HEADERS)
  pipe = DFYPipeline()
  _, Qout, *_ = http.clients(pipe, f'{endpoint}/queues', request=req)
  blobs = ClientKV(f'{endpoint}/images', request=req)
  online_blobs = KV.of(args.dfy_blobs)
  engine = create_engine(args.dfy_sql)
  core = Core.of(args.core_meta, args.core_blobs)

  pusher = Pusher(
    Qout=Qout, pipeline_blobs=blobs, dfy_blobs=online_blobs,
    dfy_engine=engine, core=core, logger=logger
  )
  asyncio.run(pusher.loop())

if __name__ == '__main__':
  print('Executing as main')
  from dotenv import load_dotenv
  load_dotenv()
  main()