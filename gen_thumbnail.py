import blurhash
import json
from PIL import Image
from pathlib import Path
from itertools import chain

REF_WIDTH = 600
JSON_NAME = 'images.json'
ARCHIVES = ['blog', 'chaotic', 'fine-weather']

def run():
  for archive in ARCHIVES:
    folder_path = Path(archive)
    processed = {}

    images_json_path = folder_path / JSON_NAME
    if images_json_path.exists():
      with open(images_json_path, 'rt', encoding='utf-8') as f:
        processed = json.load(f)
    
    for img_path in list(chain.from_iterable([folder_path.glob(f'**/*.{i}') for i in ['png', 'jpg', 'jpeg']])):
      path_str = str(img_path)
      if path_str not in processed:
        img = Image.open(img_path)
        w, h = img.size
        img.thumbnail((REF_WIDTH, round(REF_WIDTH/w*h)))

        thumbnail_folder = folder_path / 'thumbnail'
        thumbnail_folder.mkdir(exist_ok=True, parents=True)
        img.save(thumbnail_folder / img_path.name)

        hash = blurhash.encode(img, 4, 4)
        processed[path_str] = {
          'hash': hash,
          'size': [w, h],
        }
  
    with open(images_json_path, 'wt', encoding='utf-8') as f:
      f.write(json.dumps(processed))
    
if __name__ == '__main__':
  run()