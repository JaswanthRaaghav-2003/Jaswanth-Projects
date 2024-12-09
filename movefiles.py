import os
import shutil

source_dir = "C:/telegram-bot"
dest_dir = os.path.join(source_dir, "telegram-bot")

os.makedirs(dest_dir, exist_ok=True)

for item in os.listdir(source_dir):
    if item == ".git":
        continue
    shutil.move(os.path.join(source_dir, item), os.path.join(dest_dir, item))
