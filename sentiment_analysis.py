# Ok, so if we want to figure out how positive/negative certain characters are,
# we want to perform sentiment analysis.
# So let's import nltk's sentiment analyzer package and the sentence tokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import os
import numpy as np
import glob
import matplotlib.pyplot as plt


# Now that we've imported the required stuff, we have to get the lines spoken by
# each character. To do this using memory efficiently, let's calculate our final
# stats for each character separately.

main_characters = [
    'Phineas',
    'Ferb',
    'Candace',
    'Isabella',
    'Buford',
    'Baljeet',
    'Linda',
    'Doofenshmirtz',
    'Perry',
    'Major Monogram',
    'Carl',
    'Stacy',
    'Jeremy',
    'Lawrence',
    'Vanessa',
]

# Define data struct for storing final positivity/negativity scores
pos_neg_scores = {}

# Let's get a list of all the scripts
s1_script_paths = sorted(glob.glob('transcripts/season_1/*.txt'), key=os.path.getmtime)
s2_script_paths = sorted(glob.glob('transcripts/season_2/*.txt'), key=os.path.getmtime)
s3_script_paths = sorted(glob.glob('transcripts/season_3/*.txt'), key=os.path.getmtime)
s4_script_paths = sorted(glob.glob('transcripts/season_4/*.txt'), key=os.path.getmtime)
script_paths = [s1_script_paths, s2_script_paths, s3_script_paths, s4_script_paths]

# For each character, we want to go through each episode script from each season
# and store their lines in a list. Once we've got all their lines, we can get
# their compound scores for each line, and then take the mean of the compound
# scores to get an overall positive/negative rating for the character.
for character in main_characters:
    character_lines = []
    for season in range(0, 4):
        for episode in script_paths[season]:
            script = open(episode, 'r')
            for line in script:
                if line[:1] == '(' and line.strip()[-1:] == ')':
                    continue
                if line[:1] == '\xe2' and line.strip()[-1:] == '\xe2':
                    continue
                if line.strip() == '' or line.strip() == 'End Credits':
                    continue
                if line.strip() == 'Part I' or line.strip() == 'Part II':
                    continue
                character_name = line.split(':')[0]
                if character_name == character:
                    # tokenize line because it might be more than one actual line.
                    character_lines.extend(tokenize.sent_tokenize(line))
                # handle Major Monogram's edge case
                if character_name == 'Monogram' and character == 'Major Monogram':
                    character_lines.extend(tokenize.sent_tokenize(line))
    # now we have all the lines for a character, we can analyze
    sid = SentimentIntensityAnalyzer()  # haha i'm sid and i'm calling this sid
    pos_neg_scores[character] = []
    for sentence in character_lines:
        scores = sid.polarity_scores(sentence)
        pos_neg_scores[character].append(scores['compound'])
    pos_neg_scores[character] = np.array(pos_neg_scores[character])

# Now that each character has a numpy array associated with them for their subjectivity
# scores, I can plot their distributions.
# After plotting distributions, I see that a large chunk of lines are neutral.
# How large is that chunk, you ask? I'll answer.
for fig in range(0, len(main_characters)):
    plt.figure(fig)
    character = main_characters[fig]
    plt.hist(pos_neg_scores[character], 10, normed=1, facecolor='g', alpha=0.75)
    pos = []
    neg = []
    neu = []
    for score in np.nditer(pos_neg_scores[character]):
        if score <= -0.5:
            neg.append(score)
        elif score >= 0.5:
            pos.append(score)
        else:
            neu.append(score)
    total_len = pos_neg_scores[character].size
    pos_percent = round(len(pos)/total_len * 100, 3)
    neg_percent = round(len(neg)/total_len * 100, 3)
    neu_percent = round(len(neu)/total_len * 100, 3)
    plt.title('Histogram of {}\'s Positivity Per Line'.format(character))
    plt.xlabel('Positivity Scores\nNegative: {}%\nNeutral: {}%\nPositive: {}%'.format(neg_percent, neu_percent, pos_percent))
    plt.ylabel('Number of Lines')

plt.show()
