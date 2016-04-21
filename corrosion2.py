import os
import re
import random


class ChainMaker:
    PATHS = os.path.join(os.path.dirname(__file__), 'static/txt')
    REG_WORD = re.compile(r'[А-Яа-я]+')
    PREP_LEN = 2
    NON_PREP = {'я', 'он', 'ты', 'вы', 'мы', 'ее', 'их', 'им', 'ей'}

    @classmethod
    def analyze_pattern(cls, pat):
        chains = dict()
        rhymes = set()
        data = cls.REG_WORD.findall(pat)
        for num, w in enumerate(data[:-1]):
            w = w.lower()
            if len(w) <= cls.PREP_LEN and w not in cls.NON_PREP:
                data[num + 1] = w + ' ' + data[num + 1].lower()
        words = [d for d in data if len(d) > cls.PREP_LEN]
        if words:
            p = len(words)
            for num, word in enumerate(words[:1:-1], 1):
                if word not in chains:
                    chains[word] = set()
                word0 = words[p - num - 1]
                if word0 != word:
                    chains[word].add(word0)
            last_word = words[-1]
            if len(last_word) > 2:
                rhymes.add(words[-1])
        return rhymes, chains

    @classmethod
    def analyze(cls):
        files = os.listdir(cls.PATHS)
        rhymes = set()
        chains = dict()
        for file in files:
            path = os.path.join(cls.PATHS, file)
            with open(path, 'r') as f:
                for line in f:
                    r, c = cls.analyze_pattern(line)
                    rhymes = rhymes.union(r)
                    for k in c:
                        if k not in chains:
                            chains[k] = set()
                        chains[k] = chains[k].union(c[k])
        return rhymes, chains


class Constructor:
    SONG_PATTERNS = {'VVCC', 'VCVC', 'VCVCC'}
    VERSE_LENGTH = 4
    RHYME_PATTERNS, CHAIN_PATTERNS = ChainMaker.analyze()
    RHYME_DICT_MIN_SIZE = 3
    SIGNS = {'.', '!', '...', '!!!'}
    CHORUS_LENGTH_MIN = 1
    CHORUS_LENGTH_MAX = 3
    VERSE_LENGTH_MIN = 2
    VERSE_LENGTH_MAX = 5

    @staticmethod
    def _random_from_set(data):
        return random.sample(data, 1)[0]

    @classmethod
    def construct_pattern(cls, pattern, rhyme):

        def __construct_rhyme():

            def __rhyme_dict():
                if not counter:
                    c = None
                else:
                    c = counter
                d = [r for r in cls.RHYME_PATTERNS if
                     len(r) > -counter + 2 and
                     rhyme not in r and
                     r[-2+counter:c] == rhyme[-2+counter:c]]
                return d

            if rhyme:
                counter = 0
                r_dict = []
                while len(r_dict) < cls.RHYME_DICT_MIN_SIZE:
                    r_dict = __rhyme_dict()
                    counter -= 2
                    if -counter > len(rhyme):
                        r_dict = cls.RHYME_PATTERNS
                        break
            else:
                r_dict = cls.RHYME_PATTERNS
            return cls._random_from_set(r_dict)

        line = [__construct_rhyme()]
        for v in range(pattern - 1):
            word = cls.CHAIN_PATTERNS.get(line[-1])
            if word:
                word = random.sample(word, 1)
            else:
                word = random.sample(cls.CHAIN_PATTERNS.keys(), 1)
            line += word
        return line[::-1]

    @classmethod
    def construct_verse(cls, pat):
        verse = []
        rhyme = None
        for _ in range(cls.VERSE_LENGTH):
            if verse:
                rhyme = verse[-1][-1]
            verse.append(cls.construct_pattern(pat, rhyme))
        for num, line in enumerate(verse):
            verse[num] = ' '.join(line).capitalize()
            verse[num] += cls._random_from_set(cls.SIGNS)
        return '\n'.join(verse)

    @classmethod
    def construct(cls):
        song_pattern = cls._random_from_set(cls.SONG_PATTERNS)
        chorus_pat = random.randint(cls.CHORUS_LENGTH_MIN, cls.CHORUS_LENGTH_MAX)
        verse_pat = random.randint(cls.VERSE_LENGTH_MIN, cls.VERSE_LENGTH_MAX)
        chorus = cls.construct_verse(chorus_pat)
        song = []
        for v in song_pattern:
            if v == 'V':
                song.append(cls.construct_verse(verse_pat))
            elif v == 'C':
                song.append(chorus)
        return '\n\n'.join(song)


if __name__ == "__main__":
    text = Constructor.construct()
    print(text)
