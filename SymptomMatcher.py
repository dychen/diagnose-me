import itertools

def load_stop_words(filename='stop_words.txt'):
    stop_words_set = set([])
    stop_words_file = open(filename, 'r')
    for line in stop_words_file:
        stop_words_set.add(line.strip().lower())
    stop_words_file.close()
    return stop_words_set

def load_symptom_list(filename):
    symptom_list = []
    symptom_file = open(filename, 'r')
    for line in symptom_file:
        symptom_list.append(line.strip().lower())
    symptom_file.close()
    return symptom_list

def parse_stop_words(input_string):
    input_list = input_string.strip().split()
    input_list[:] = (word for word in input_list if word not in STOP_WORDS)
    return ' '.join(input_list)

def take_out_long_symptoms(symptom_list):
    max_number_of_words = 3
    symptom_list[:] = (symptom for symptom in symptom_list if len(symptom.split()) <= max_number_of_words)
    return symptom_list

# Currently unused
def take_out_stop_words(input_list):
    for i, value in enumerate(input_list):
        input_list[i] = parse_stop_words(value)
    return input_list

def string_ignores_ing_suffix(input_string):
    input_string.replace('ing ', '')
    input_string = input_string[:-3] if input_string[-3:] == 'ing' else input_string
    return input_string

def levenshtein(s1, s2, limit=100):
    #testing
    s1 = string_ignores_ing_suffix(parse_stop_words(s1))
    s2 = string_ignores_ing_suffix(parse_stop_words(s2))
    #/testing
    previous_row = range(len(s1) + 1)
    for j, c2 in enumerate(s2):
        current_row = [j + 1]
        for i, c1 in enumerate(s1):
            i += 1
            insert = previous_row[i] + 0.75 # Treat inserts and deletes as better than replacements
            delete = current_row[i - 1] + 0.75
            replace = previous_row[i - 1] + (c1 != c2)
            current_row.append(min(insert, delete, replace))
        if min(current_row) > limit:
            return limit
        previous_row = current_row
    return previous_row[-1]

def permute_levenshtein(s1, s2, limit=100):
    min_distance = max(len(s1), len(s2))
    for s1_perm in itertools.permutations(s1.split()):
        for s2_perm in itertools.permutations(s2.split()):
            distance = levenshtein(' '.join(s1_perm), ' '.join(s2_perm), limit)
            min_distance = distance if distance < min_distance else min_distance
    return min_distance

def test(symptom_list):
    input = ''
    number_of_results = 10
    while input != 'quit':
        input = parse_stop_words(raw_input("Enter symptom: "))
        closest_matches = []
        for symptom in symptom_list:
            #distance = levenshtein(input, symptom)
            if len(closest_matches) < number_of_results:
                distance = permute_levenshtein(input, symptom)
                closest_matches.append((distance, symptom))
                closest_matches.sort()
            else:
                distance = permute_levenshtein(input, symptom, closest_matches[-1][0])
                if distance < closest_matches[-1][0]:
                    closest_matches[-1] = (distance, symptom)
                    closest_matches.sort()
        for d, symptom in closest_matches:
            print "%1.2f: %s" % (d, symptom)

if __name__ == '__main__':
    STOP_WORDS = load_stop_words()
    input_file = 'symptom_list.txt'
    symptom_list = take_out_long_symptoms(load_symptom_list(input_file))
    print "Number of symptoms in database: %d" % len(symptom_list)
    test(symptom_list)
