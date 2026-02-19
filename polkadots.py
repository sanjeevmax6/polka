# FINAL REASONING: 
# Before starting, I did use LLMs to write code, because that has been my usual flow all along, and I am always the captain steering it. The idea was entirely mine though, and please find the explanation below
# I tried a wa in which I could reverse engineer the pupils and lips
# First I tried just computing the unique_chars just for my reference to see if I can find a way to categorize
# Next I split the lines, and my idea was to get global polkadots number and then local count inside each range I find from he forbidden characters
# So my reasoning was answer = (global_polka - local_polka) + (local_polka * pupil_count) -> and pupil_count was my later worry
# So once i did the above, I wanted to find all ranges where the forbidden chars were not there, and to my surprise it was 175
# My idea then was to count the frequency of the patterns, I was thinking if I can narrow down one pattern with freq = 2 and other with freq = 1, then those are my pupils and lips respectively
# To my surprise I found 6 choices for each and hence I dropped the idea
# Meanwhile I was trying to look at the ascii art and try t find a girl out of it, but I couldnt because I couldnt agreee with the fact that a girls head could be that big
# Then I google 'angelica the brat', to my surprise it was a cartoon character
# Finally since I did not have enough data, I narrowed down the pupils to be the circular characters
# ,'' ~ ,       • ; •          "      "„
#             """";      ' - , ,  ; , , , - '' ' ' -,_ ', ',
#            , -' ' ',           ,'    ,'             ',~', ',
#          ,'         ' - , ,()' /\    ',          (),'¯ ,'   `¸`;
#          ',                            ` ` ` ` ` `      ,-,,,-'
# I remember that the chars shouldnt have forbidden ones, but going deep you meant chars shouldnt be inside the pupil or lips, and I only count the pupils borders and not the ones inside, so that satisfies this condition
# This doesnt matter anyway because according to the same logic, lips had to be somewhere below, but the Polka character is nowhere to be found apart from dress
# SO Obviously in second term the count of polka inside lips is 0, therefore answer = polka dots in dress = 41

# I am assuming the 0 or O like characters are the only ones that are polkadots, and they are the only ones I need to calculate with ot without the formula (inside or outside lips)
FORBIDDEN = {"'", "`", ",", "-"}
POLKA = "O"

# First let me get the intervals where there are no chars - ['] [`] [,] [-]
# so for each row maybe I can keep track of the range where these chars dont appear at all
# These ranges can either be lips or pupils
# So inside each lips I need to count the number of polkadots separately, and then subtract this number from overall polkadots
# But the question is how can I differentiate pupils and lips, maybe the largest range?
# To maybe reduce time complexity I can have a global and local counter to track the polkadots inside and outside kind of like local and global counters
# So I can store this in a hashmap first, and then figure out a way to count the number of chars making up a pupil

def build_ranges(lines, forbidden=FORBIDDEN, polka_char=POLKA):
    """
    Build maximal contiguous ranges per row that contain no forbidden characters.
    Track local O count per range + global O count.
    Returns:
      ranges: list of (row, start_x, end_x, pattern, local_O)
      global_O: int
    """
    ranges = []
    global_O = 0

    for r, row in enumerate(lines):
        global_O += row.count(polka_char)

        start = None
        local_O = 0

        for x, ch in enumerate(row):
            if ch in forbidden:
                if start is not None:
                    end = x - 1
                    pattern = row[start:end + 1]
                    ranges.append((r, start, end, pattern, local_O))
                    start = None
                    local_O = 0
                continue

            if start is None:
                start = x
                local_O = 0

            if ch == polka_char:
                local_O += 1

        if start is not None:
            end = len(row) - 1
            pattern = row[start:end + 1]
            ranges.append((r, start, end, pattern, local_O))

    return ranges, global_O


def find_candidate_ranges(ranges, lines):
    """
    Heuristics (adjustable):
    - Pupils candidates: patterns with exactly 2 occurrences, short length
    - Lips candidates: patterns with 1 occurrence, longer length
    """
    grouped = {}
    for (r, start, end, pattern, local_O) in ranges:
        if pattern.strip() == "":
            continue
        grouped.setdefault(pattern, []).append((r, start, end))

    pupils_groups = {
        p: occ for p, occ in grouped.items()
        if len(occ) == 2 and len(p) <= 15
    }

    lips_candidates = []
    for p, occ in grouped.items():
        if len(occ) == 1 and len(p) >= 10:
            r, start, end = occ[0]
            lips_candidates.append((r, start, end, p))

    lips_candidates.sort(key=lambda t: len(t[3]), reverse=True)

    return pupils_groups, lips_candidates


if __name__ == "__main__":
    file_path = "ascii_art_dress.txt"

    # Load ASCII art lines (preserve indentation!)
    dress = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            processed_line = line.rstrip("\n")
            if processed_line.strip() == "":
                continue
            dress.append(processed_line)

    unique_chars = set()
    for row in dress:
        for ch in row:
            unique_chars.add(ch)

    print(unique_chars)

    # Build ranges + global polkadot count
    ranges, global_O = build_ranges(dress)

    print("Global 'O' polkadots:", global_O)
    print("Total ranges found:", len(ranges))

    # pupils_groups, lips_candidates = find_candidate_ranges(ranges, dress)