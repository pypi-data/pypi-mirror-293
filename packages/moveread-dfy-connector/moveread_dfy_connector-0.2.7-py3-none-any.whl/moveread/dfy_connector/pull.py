from typing import NamedTuple, Sequence
from dataclasses import dataclass, field
import asyncio
from uuid import uuid4
from sqlmodel import Session
from sqlalchemy import Engine
from haskellian import either as E, dicts as D
from kv import KV
import pure_cv as vc
from pipeteer import WriteQueue
from moveread.tnmt import Game, Upload, queries
from moveread.pipelines.dfy import Input
from dslog import Logger
import robust_extraction2 as re
import scoresheet_models as sm

def inputId(tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId}/{group}/{round}/{board}_{uuid4()}'

def title(game: Game, tournId: str, group: str, round: str, board: str) -> str:
  s = f'{tournId} {group}/{round}/{board} {game.white} - {game.black}'
  if game.result:
    s += f' {game.result}'
  return s

class NewInput(NamedTuple):
  input: Input
  """Pipeline input"""
  from_urls: Sequence[str]
  to_urls: Sequence[str]

def new_input(uuid: str, game: Game, upload: Upload, *, model_name: str, model: re.ExtendedModel):
  gid = game.gameId()
  from_urls = [img.url for img in upload.imgs]
  to_urls = [f'{uuid}/{i}.jpg' for i in range(len(from_urls))]
  endpoint = f'/v1/models/{gid["tournId"]}-{gid["group"]}:predict'
  task = Input(gameId=gid, model=model, model_name=model_name, imgs=to_urls, title=title(game, **gid), serving_endpoint=endpoint)
  return NewInput(input=task, from_urls=from_urls, to_urls=to_urls)

@dataclass
class Puller:
  Qpush: WriteQueue[Input]
  pipeline_blobs: KV[bytes]
  dfy_blobs: KV[bytes]
  models: sm.ModelsCache = field(default_factory=sm.ModelsCache)
  logger: Logger = field(default_factory=lambda: Logger.click().prefix('[PULLER]'))

  @E.do()
  async def jpg_copy(self, url_from: str, url_to: str):
    """Copies the image by downloading it first, encoding it as JPG, then inserting"""
    img = (await self.dfy_blobs.read(url_from)).mapl(lambda e: f'Error reading dfy blob "{url_from}": {e}').unsafe()
    jpg = vc.encode(vc.decode(img), '.jpg')
    return (await self.pipeline_blobs.insert(url_to, jpg)).mapl(lambda e: f'Error inserting blob "{url_to}": {e}').unsafe()

  async def copy_images(self, from_urls: Sequence[str], to_urls: Sequence[str]):
    tasks = [self.jpg_copy(from_, to) for from_, to in zip(from_urls, to_urls)]
    results = await asyncio.gather(*tasks)
    return E.sequence(results)

  @E.do()
  async def pull_one(self, game: Game, upload: Upload, model_name: str):
    model = (await self.models.fetch(model_name)).mapl(lambda e: f'Error fetching model "{model_name}: {e}"').unsafe()
    id = upload.id
    x = new_input(id, game, upload, model=model, model_name=model_name)
    (await self.copy_images(x.from_urls, x.to_urls)).mapl(lambda e: f'Error copying images: {e}').unsafe()
    (await self.Qpush.push(id, x.input)).mapl(lambda e: f'Error pushing task: {e}').unsafe()


  async def pull_games(self, session: Session, uploads: Sequence[tuple[Game, Upload]]):
    tnmt_games = D.group_by(lambda g: g[0].tournId, uploads)
    for tournId, games in tnmt_games.items():
      if not (model := queries.Select(session).model(tournId)):
        self.logger(f'No model for tournament "{tournId}"', level='WARNING')
        continue

      for game, upload in games:
        r = await self.pull_one(game, upload, model)
        if r.tag == 'left':
          self.logger(f'Error pulling game {game.gameId()}: {r.value}', level='ERROR')
        else:
          upload.status = 'doing'
          session.add(upload)
          session.commit()
          self.logger(f'Pulled game {game.gameId()}')

  async def loop(self, dfy_engine: Engine, interval: float = 300):
    while True:
      with Session(dfy_engine) as session:
        uploads = queries.Select(session).game_uploads()
        if uploads:
          self.logger(f'Pulling {len(uploads)} games...')
          await self.pull_games(session, uploads)
        else:
          self.logger('No games to pull', level='DEBUG')
          
      await asyncio.sleep(interval)