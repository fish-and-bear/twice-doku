import os
import aiofiles
import json
import asyncio

try:
    import js
    IS_WEB = True
except ImportError:
    IS_WEB = False

async def json_open(file):
    if IS_WEB:
        try:
            with open(file, mode='r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error opening JSON file {file}: {e}")
            return {}
    else:
        try:
            async with aiofiles.open(file, mode='r') as f:
                return json.loads(await f.read())
        except Exception as e:
            print(f"Error opening JSON file {file}: {e}")
            return {}

async def json_save(file, data):
    if IS_WEB:
        try:
            with open(file, mode='w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving JSON file {file}: {e}")
    else:
        try:
            async with aiofiles.open(file, mode='w') as f:
                await f.write(json.dumps(data))
        except Exception as e:
            print(f"Error saving JSON file {file}: {e}")

def text_open(fp):
    with open(fp, 'r') as f:
        d = [line.replace('\n', '') for line in f.readlines()]
    return d

def text_save(fp, d):
    with open(fp, 'w+') as f:
        f.writelines(d)

async def remove_file(file):
    def remove():
        try:
            os.remove(file)
        except FileNotFoundError:
            pass  # File doesn't exist, so no need to remove it
    
    await asyncio.to_thread(remove)

async def score_save(file, level, seconds, dt):
    try:
        # Load existing scores
        try:
            scores = await json_open(file)
            if not isinstance(scores, dict):
                print(f"Unexpected scores format. Resetting scores.")
                scores = {}
        except FileNotFoundError:
            print(f"Scores file not found. Creating new scores dictionary.")
            scores = {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in scores file. Resetting scores.")
            scores = {}

        # Ensure level exists in scores
        if level not in scores:
            scores[level] = []

        # Append new score
        new_score = f"{seconds}-({dt})"
        scores[level].append(new_score)

        # Save updated scores
        await json_save(file, scores)
        print(f"Score saved successfully: {level} - {seconds}s - {dt}")
        return True

    except Exception as e:
        print(f"Error saving score: {e}")
        import traceback
        traceback.print_exc()
        return False

async def settings_save(file, theme, resolution, volume):
    settings = await json_open(file)
    settings['theme'] = theme
    settings['resolution'] = resolution
    settings['volume'] = volume
    await json_save(file, settings)

async def quit_save(puzzlefile, timefile, level, grid, seconds, guesses, dt_string):
    stats = {
        "level": level,
        "currenttime": seconds,
        "guesses": guesses,
        "dateandtime": dt_string
    }
    await json_save(puzzlefile, grid)
    await json_save(timefile, stats)
