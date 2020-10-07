def strip_punctuation(in_str):
    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
    for stp in punctuation_chars:
        in_str = in_str.replace(stp, '')
    return in_str


def get_neg(in_str):
    splt_str = strip_punctuation(in_str.lower()).split()
    bad_count = 0
    for word in splt_str:
        if word in negative_words:
            bad_count += 1
    return bad_count


def get_pos(in_str):
    splt_str = strip_punctuation(in_str.lower()).split()
    pos_count = 0
    for word in splt_str:
        if word in positive_words:
            pos_count += 1
    return pos_count


punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']


positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())


with open("project_twitter_data.csv","r") as tt_data, open("resulting_data.csv","w") as tt_out:
    tt_out.write('Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n')
    for line in tt_data.readlines()[1:]:
        line = line.strip().split(',')
        tt_wrds, tt_retweets, tt_replies = line[0], line[-2], line[-1]
        tt_out.write('{}, {}, {}, {}, {}\n'.format(tt_retweets, tt_replies, get_pos(tt_wrds), get_neg(tt_wrds), get_pos(tt_wrds) - get_neg(tt_wrds)))    
