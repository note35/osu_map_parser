import re

from collections import OrderedDict


class MapParser:

    def __init__(self, target_path):
        self.parse_ret = {
            'version': -1,
            'general': {},
            'editor': {},
            'metadata': {},
            'difficulty': {},
            'events': {},
            'timingpoints': {},
            'colours': {},
            'hitobjects': {},
        }

        # data preparation
        self.__load_file(target_path)
        self.__cut_section()
        self.__get_section()
        self.__transform_sections()
        self.__get_version()

    def __load_file(self, path):
        with open(path, 'r') as fptr:
            lines = fptr.readlines()
        self.lines = [line.strip() for line in lines]

    def __cut_section(self):
        section_idx_list = []
        key_list = []

        # get cutting point O(n)
        is_first_match = True
        for idx, line in enumerate(self.lines):
            match = re.compile(r'^\[(.*)\]$').match(line)
            if is_first_match and match:
                section_idx_list.append(idx)
                key_list.append(match.group(1).lower())
                is_first_match = False
            elif match:
                section_idx_list.append(idx)
                section_idx_list.append(idx)
                key_list.append(match.group(1).lower())
            elif idx == len(self.lines)-1:
                section_idx_list.append(idx+1)

        if len(key_list) != len(section_idx_list)/2:
            Exception('Failed to load')

        # [1,2,3,4] -> zip([1,3],[2,4]) -> [(1,2), (3,4)]
        idx_pair_list = list(zip(section_idx_list[0:][::2], section_idx_list[1:][::2]))
        # zip(['key1','key2'], [(1,2), (3,4)]) -> [('key1', (1,2)), ('key2', (3,4))]
        key_pair_list = list(zip(key_list, idx_pair_list))

        self.key_list = key_list
        self.sections = OrderedDict(key_pair_list)
        """
            OrderedDict::
            {
                str::'section_a': tuple::(int::start_line, int::end_line),
                ...
            }
        """

    @staticmethod
    def transform_pair_line(line):
        line_split = line.split(':')
        key = line_split[0].strip()
        value = line_split[1].strip()
        return (key, value)

    @staticmethod
    def transform_colour_line(line):
        line_split = line.split(':')
        key = line_split[0].strip()
        value = tuple(line_split[1].strip().split(','))
        return (key, value)

    @staticmethod
    def transform_event_line(line):
        # TODO: handle file name such as "aaa,bbb.txt"
        line_split = line.split(',')
        return (line_split[0], line_split[1:])

    @staticmethod
    def transform_timingpoints_line(line):
        line_split = line.split(',')
        return (line_split[0], line_split[1:])

    @staticmethod
    def transform_hitobjects_line(line):
        line_split = line.split(',')
        return (line_split[2], line_split[0:2]+line_split[3:])

    def __transform_section(self, key):
        if key in ['general', 'editor', 'metadata', 'difficulty']:
            tmp_dict = {}
            for item in [MapParser.transform_pair_line(line) for line in self.parse_ret[key] if line != '']:
                tmp_dict[item[0]] = item[1]
            return tmp_dict
        elif key == 'colours':
            tmp_dict = {}
            for item in [MapParser.transform_colour_line(line) for line in self.parse_ret[key] if line != '']:
                tmp_dict[item[0]] = item[1]
            return tmp_dict
        elif key == 'events':
            # TODO: define a OrderedDict with meaningful key, value
            tmp_list = []
            for line in self.parse_ret[key]:
                if '//' in line:
                    if line.split('//')[0]:
                        tmp_list.append(MapParser.transform_event_line(line))
                elif line:
                    tmp_list.append(MapParser.transform_event_line(line))
            return OrderedDict(tmp_list)
        elif key ==  'timingpoints':
            # TODO: define a OrderedDict with meaningful key, value
            return OrderedDict([MapParser.transform_timingpoints_line(line) for line in self.parse_ret[key] if line != ''])
        elif key == 'hitobjects':
            # TODO: define a OrderedDict with meaningful key, value
            return OrderedDict([MapParser.transform_hitobjects_line(line) for line in self.parse_ret[key] if line != ''])
        else:
            raise KeyError('{} is not a valid key'.format(key))

    def __get_section(self, key=None):
        sections = self.sections
        # ignore first line eg: [General] of section => [1:]
        if key:
            self.parse_ret[key] = [self.lines[line] for line in range(sections[key][0], sections[key][1])][1:]
        elif not key:
            for key in self.key_list:
                self.parse_ret[key] = [self.lines[line] for line in range(sections[key][0], sections[key][1])][1:]

    def __transform_sections(self, key=None):
        if key:
            self.parse_ret[key] = self.__transform_section(key)
        elif not key:
            for key in self.key_list:
                self.parse_ret[key] = self.__transform_section(key)

    def __get_version(self):
        match = re.compile(r'osu file format v([0-9]*)').match(self.lines[0])
        if match:
            self.parse_ret['version'] = match.group(1)

    @property
    def version(self):
        return self.parse_ret['version']

    @property
    def general(self):
        return self.parse_ret['general']

    @property
    def editor(self):
        return self.parse_ret['editor']

    @property
    def metadata(self):
        return self.parse_ret['metadata']

    @property
    def difficulty(self):
        return self.parse_ret['difficulty']

    @property
    def events(self):
        return self.parse_ret['events']

    @property
    def timingpoints(self):
        return self.parse_ret['timingpoints']

    @property
    def colours(self):
        return self.parse_ret['colours']

    @property
    def hitobjects(self):
        return self.parse_ret['hitobjects']
