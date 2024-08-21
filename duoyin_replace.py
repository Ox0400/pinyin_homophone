pinyin_words_map = {} # cháo: [朝, 潮]
duoyin_words_map = {} # 朝: [cháo, zháo]

with open('pinyin.txt') as f:
    for i in f.read().splitlines():
        if i.startswith('#'): continue
        k, v = i.split(':');
        _ = pinyin_words_map.setdefault(k,[]).append(v)
        duoyin_words_map.setdefault(v, []).append(k)


words_size_pinyin_map = {} # 3: {朝阳区: cháo yáng qū}
with open('large_pinyin.txt') as f:
    for line in f.read().splitlines():
        if line.startswith('#'): continue
        w, p = line.split(': ')
        words_size_pinyin_map.setdefault(len(w), {})[w] = p


def replace_duoyin_aword(text, pinyin):
    # 朝, cháo
    if len(duoyin_words_map.get(text, [])) <= 1:
        # 非多音字, 不做替换, 直接返回
        return text
    for w in pinyin_words_map.get(pinyin, []):
        if len(duoyin_words_map.get(w, [])) > 1:
            # 当前字也是多音字
            continue
        if w == text:
            # 等于当前字
            continue
        return w
    return text

# replace_duoyin_aword('朝', 'cháo')

def replace_duoyin_words(texts, pinyins):
    #朝阳区: cháo yáng qū
    text = ""
    for idx, w in enumerate(texts):
        p = pinyins[idx]
        nw = replace_duoyin_aword(w, p)
        text += nw
    return text
# replace_duoyin_words('朝阳区', 'cháo yáng qū'.split(' '))

def replace_duoyin(text, ): # 这里是朝阳区
    matched_pinyin_map = {} # 朝阳区: cháo yáng qū
    for w_len in reversed(sorted(list(words_size_pinyin_map.keys()))):
        word_pinyin_map = words_size_pinyin_map[w_len]
        for w, p in word_pinyin_map.items():
            if w in text:
                matched_pinyin_map[w] = p
                text = text.replace(w, replace_duoyin_words(w,p.split(' ')))
    print('matched', matched_pinyin_map)
    return text

# replace_duoyin('这里是朝阳区, 今天天气25摄氏度, 阻塞模式, 塞住漏洞')
# '浙里是潮阳屈, 今天天气25设是杜, 阻色魔式, 塞住漏洞'
