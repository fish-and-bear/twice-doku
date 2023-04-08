from json import dump, load
import os


def json_open(fp):
    with open(fp, 'r') as f:
        d = load(f)
    return d


def json_save(fp, d):
    with open(fp, 'w+') as f:
        dump(d, f)


def text_open(fp):
    with open(fp, 'r') as f:
        d = [line.replace('\n', '') for line in f.readlines()]
    return d


def text_save(fp, d):
    with open(fp, 'w+') as f:
        f.writelines(d)


def remove_file(fp):
    if os.path.exists(fp):
        os.remove(fp)


def score_save(fp, level, seconds, dt):
    try:
        if os.stat(fp).st_size > 0:
            try:
                scores = json_open(fp)
                scores[level].append(str(seconds) + "-(" + dt + ")")
                json_save(fp, scores)
            except KeyError:
                scores = json_open(fp)
                subscores = []
                scores[level] = subscores
                scores[level].append(str(seconds) + "-(" + dt + ")")
                json_save(fp, scores)
        else:
            scores = {}
            subscores = []
            scores[level] = subscores
            scores[level].append(str(seconds) + "-(" + dt + ")")
            json_save(fp, scores)
    except OSError:
        scores = {}
        subscores = []
        scores[level] = subscores
        scores[level].append(str(seconds) + "-(" + dt + ")")
        json_save(fp, scores)


def settings_save(fp, theme, resolution, volume):
    try:
        if os.stat(fp).st_size > 0:
            settings = json_open(fp)
            settings['theme'] = theme
            settings['resolution'] = resolution
            settings['volume'] = volume
            json_save(fp, settings)
        else:
            settings = {}
            settings['theme'] = theme
            settings['resolution'] = resolution
            settings['volume'] = volume
            json_save(fp, settings)
    except OSError:
        settings = {}
        settings['theme'] = theme
        settings['resolution'] = resolution
        settings['volume'] = volume
        json_save(fp, settings)


def quit_save(puzzlefile, timefile, level, grid, seconds, guesses, dt):
    json_save(puzzlefile, grid)
    stats = {}
    stats['level'] = level
    stats['currenttime'] = seconds
    stats['guesses'] = guesses
    stats['dateandtime'] = dt
    json_save(timefile, stats)
