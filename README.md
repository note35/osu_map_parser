Osu Map Parser
==============

Osu Map Parser is a library written in **Python3** for parsing map in [osu](https://osu.ppy.sh).

Currently, it only support **standard** mode. For additional requirement, you can extend it if needed, there is no solid schedule for providing feature for supporting other modes.

Osu Map Parser is an **unofficial** tool, thus the author can not promise it works 100% correctly for all maps. Also, for newer map format, this tool might not be able to parse them. Besides, this tools only retreive the info from map file, the meaning of those info could be found from osu official website. 


Usage
=====

**Load Map**

```python
from map_parser import MapParser
mp = MapParser('path/to/map')
```

**Read Map**

```python
# general information (eg: music file name)
mp.general
{...}

# editor's configuration (eg: distance space)
mp.editor
{...}

# metadata of the map (eg: song information)
mp.metadata
{...}

# map's difficulty (eg: hp, ar, od...)
mp.difficulty
{...}

# events of map (storyboard)
mp.events
OrderedDict([
    'time': [events]
])

# colours of circles
mp.colours
{
    'ComboX': ('R', 'G', 'B'),
}

# objects of map
mp.hitobjects
[
    '...',
]
```


Development
===========

**test**

```bash
$ python3.6 -m unittest test_parse_standard_map
```


**mypy/flake8**

```bash
$ virtualenv -p /usr/local/bin/python3.6 env3
$ . env3/bin/activate.fish
$ pip install -r requirement.txt

$ mypy {python_filename} # current only write well for hitobject_parser.py
# *No Error means good*

$ flake8 {python_filename
# *No Error means good*
```



TODO
====

- Parse `events` with detailed information
- Documentation of return of `hitobject_parser.py`
- Integrate `hitobject_parser.py` into `map_parser.py`
- Integrate with Travis CI
