import blurhash
import json
from PIL import Image
from pathlib import Path
from itertools import chain

REF_WIDTH = 300
JSON_PATH = 'images.json'

def run(folder='.'):
  processed = {}

  images_json_path = Path(JSON_PATH)
  if images_json_path.exists():
    with open(JSON_PATH, 'rt', encoding='utf-8') as f:
      processed = json.load(f)
  
  folder_path = Path(folder)
  for img_path in list(chain.from_iterable([folder_path.glob(f'**/*.{i}') for i in ['png', 'jpg', 'jpeg']])):
    path_str = str(img_path)
    if path_str not in processed:
      img = Image.open(img_path)
      w, h = img.size
      img.thumbnail((300, round(300/w*h)))

      thumbnail_folder = img_path.parent / 'thumbnail'
      thumbnail_folder.mkdir(exist_ok=True, parents=True)
      img.save(thumbnail_folder / img_path.name)

      hash = blurhash.encode(img, 4, 4)
      processed[path_str] = {
        'hash': hash,
        'size': [w, h]
      }
  
  with open(JSON_PATH, 'wt', encoding='utf-8') as f:
    f.write(json.dumps(processed))
    
if __name__ == '__main__':
  run()