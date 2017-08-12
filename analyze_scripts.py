# import required stuff
import os
import csv
import glob
import operator
import matplotlib.pyplot as plt


# First, we want to get a list of all the scripts
s1_script_paths = sorted(glob.glob('transcripts/season_1/*.txt'), key=os.path.getmtime)
s2_script_paths = sorted(glob.glob('transcripts/season_2/*.txt'), key=os.path.getmtime)
s3_script_paths = sorted(glob.glob('transcripts/season_3/*.txt'), key=os.path.getmtime)
s4_script_paths = sorted(glob.glob('transcripts/season_4/*.txt'), key=os.path.getmtime)
script_paths = [s1_script_paths, s2_script_paths, s3_script_paths, s4_script_paths]


# Now we need to define our main characters:
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
    'Monogram',
    'Major Monogram',
    'Carl',
    'Stacy',
    'Jeremy',
    'Lawrence',
    'Vanessa',
]


# Next, we want to iterate through all the scripts for each season,
# keeping count of how many lines each of the main characters have in each episode
# So each season data will have an episode dict, that look like
# {
  # Character: {
  #     Lines: ,
  #     Words: ,
  # } [...],
  # total_lines: ,
  # episode_number: ,
# }
def get_lines_words_data(main_characters):
    character_data = {
        'season_1': [],
        'season_2': [],
        'season_3': [],
        'season_4': [],
    }
    # so now, for each line in each episode file in each season folder,
    for season in range(0, 4):
        season_number = 'season_' + str(season+1)
        episode_number = 1
        for episode in script_paths[season]:
            script = open(episode, 'r')
            # create a episode object
            episode_data = {
                'metadata': {
                    'total_lines': 0,
                    'episode_number': episode_number
                }
            }
            total_lines = 0
            for line in script:
                if line[:1] == '(' and line.strip()[-1:] == ')':
                    continue
                if line[:1] == '\xe2' and line.strip()[-1:] == '\xe2':
                    continue
                if line.strip() == '' or line.strip() == 'End Credits':
                    continue
                if line.strip() == 'Part I' or line.strip() == 'Part II':
                    continue
                total_lines += 1
                character_name = line.split(':')[0]
                if character_name in main_characters:
                    if character_name not in episode_data:
                        episode_data[character_name] = {
                            'lines': 0,
                            'words': 0,
                        }
                    episode_data[character_name]['lines'] += 1
                    episode_data[character_name]['words'] += len(line.split()) - 1
            episode_data['metadata']['total_lines'] = total_lines
            character_data[season_number].append(episode_data)
            episode_number += 1
        episode_number = 1
    return character_data


def find_line_word_frequency(character_data):
    most_lines = {
        'Phineas': 0,
        'Ferb': 0,
        'Candace': 0,
        'Isabella': 0,
        'Buford': 0,
        'Baljeet': 0,
        'Linda': 0,
        'Doofenshmirtz': 0,
        'Perry': 0,
        'Major Monogram': 0,
        'Carl': 0,
        'Stacy': 0,
        'Jeremy': 0,
        'Lawrence': 0,
        'Vanessa': 0,
    }
    most_words = {
        'Phineas': 0,
        'Ferb': 0,
        'Candace': 0,
        'Isabella': 0,
        'Buford': 0,
        'Baljeet': 0,
        'Linda': 0,
        'Doofenshmirtz': 0,
        'Perry': 0,
        'Major Monogram': 0,
        'Carl': 0,
        'Stacy': 0,
        'Jeremy': 0,
        'Lawrence': 0,
        'Vanessa': 0,
    }
    # Calculate frequency of lines and words spoken by each major character
    for season in character_data.keys():
        for episode in character_data[season]:
            for character in episode.keys():
                if character == 'metadata':
                    continue
                if character == 'Monogram':
                    most_words['Major Monogram'] += episode[character]['words']
                    most_lines['Major Monogram'] += episode[character]['lines']
                    continue
                most_words[character] += episode[character]['words']
                most_lines[character] += episode[character]['lines']
    return (most_lines, most_words)


def find_line_length(lines_words):
    most_lines = lines_words[0]
    most_words = lines_words[1]
    average_line_length = {}
    for character in most_lines:
        average_line_length[character] = round(most_words[character] / most_lines[character], 0)
    return average_line_length


def plot_lines_words(most_lines, most_words, line_length):
    # Now plot stuff.
    plt.figure(1)
    plt.barh(range(len(most_lines)), most_lines.values(), align='center')
    plt.yticks(range(len(most_lines)), list(most_lines.keys()))
    plt.ylabel('Characters')
    plt.xlabel('Lines')
    plt.title('Lines Spoken By Character')
    plt.figure(2)
    plt.barh(range(len(most_words)), most_words.values(), align='center')
    plt.yticks(range(len(most_words)), list(most_words.keys()))
    plt.ylabel('Characters')
    plt.xlabel('Words')
    plt.title('Words Spoken By Character')
    plt.figure(3)
    plt.bar(range(len(line_length)), line_length.values(), align='center')
    plt.xticks(range(len(line_length)), list(line_length.keys()), rotation=90)
    plt.ylabel('Words')
    plt.xlabel('Characters')
    plt.title('Average Words Per Line')
    plt.show()


character_data = get_lines_words_data(main_characters)
lines_words = find_line_word_frequency(character_data)
line_length = find_line_length(lines_words)
plot_lines_words(lines_words[0], lines_words[1], line_length)

# Now, find all occurences of "Where's Perry"
# Now, sentiment analysis of each characters line to find the Debbie Downer
