from dataclasses import dataclass, field
import asyncio
from sqlmodel import Session
from sqlalchemy import Engine
from haskellian import either as E
from kv import KV
from pipeteer import ReadQueue
from dslog import Logger
from moveread.core import Core
from moveread.tnmt import PGN, Upload
from moveread.pipelines import dfy

@dataclass
class Pusher:
  Qout: ReadQueue[dfy.Output]
  pipeline_blobs: KV[bytes]
  dfy_blobs: KV[bytes]
  dfy_engine: Engine
  core: Core
  logger: Logger = field(default_factory=lambda: Logger.click().prefix('[PUSHER]'))

  async def push_game(self, id: str, output: dfy.Output):
    e = await dfy.core.output_one(self.core, id, output, blobs=self.pipeline_blobs)
    if e.tag == 'left':
      self.logger(f'Error pushing output for game {output.gameId}:', e.value, level='ERROR')
      return False

    with Session(self.dfy_engine) as ses:
      upload = ses.get(Upload, id)
      if upload is None:
        self.logger(f'Upload not found: {id}', level='ERROR')
        return False
      
      upload.pgn = PGN(moves=output.pgn, early=output.early)
      upload.status = 'done'
      ses.add(upload)
      ses.commit()
      self.logger(f'Pushed game: {id}')
      return True
  
  @E.do()
  async def push_one(self):
    id, output = (await self.Qout.read()).unsafe()
    self.logger(f'Pushing "{id}"')
    r = await self.push_game(id, output)
    if r:
      (await self.Qout.pop(id)).unsafe()
      self.logger(f'Popped "{id}"')
      (await self.pipeline_blobs.prefix(id).clear()).unsafe()
      self.logger(f'Cleaned blobs of "{id}"')

  async def loop(self):
    while True:
      try:
        r = await self.push_one()
        if r.tag == 'left':
          self.logger('Error pushing:', r.value, level='ERROR')
          await asyncio.sleep(5)
      except Exception as e:
        self.logger('Unexpected exception:', e, level='ERROR')
        await asyncio.sleep(5)
