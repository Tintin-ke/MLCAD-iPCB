import Levenshtein

def similarity(word1, word2):
    return jaroWinklerSim(word1, word2)

def jaroWinklerSim(word1, word2):
    """
    计算Jaro–Winkler距离，而Jaro-Winkler则给予了起始部分就相同的字符串更高的分数
    :param word1: 词
    :param word2: 词
    :return: Jaro–Winkler距离
    """
    return Levenshtein.jaro_winkler(word1, word2)