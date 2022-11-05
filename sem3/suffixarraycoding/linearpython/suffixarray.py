import hypothesis as hp
import hypothesis.strategies as st

def sais(string : str) -> list[int]:
    if len(string) < 2:
        return []
    types, lms_chars, lms_strings = get_types_and_lms_characters(string)

    sa = passes(string, types, lms_chars)


    lms_order = []
    for i in sa:
        if i in lms_chars:
            lms_order.append(i)

    fingerprint_count = 0
    lms_fingerprints = {}

    for lms_suf in lms_order:
        lms_string = lms_strings[lms_suf]
        if lms_string not in lms_fingerprints:
            lms_fingerprints[lms_string] = fingerprint_count
            fingerprint_count += 1

    s1 = []
    for lms_char in reversed(lms_chars):
        s1.append(lms_fingerprints[lms_strings[lms_char]])

    sa1 = reference_sais(s1)

    if len(lms_chars) < len(sa1):
        sa1 = sa1[1:]

    lms_sorted = []
    for i in sa1:
        lms_sorted.append(lms_chars[(len(lms_chars)-1) - i])
    # print(lms_sorted)
    
    second = passes(string, types, lms_sorted, reverse_first_pass=True)
    return second

def reference_sais(reduced : list[int]):
    encountered = {}
    for c in reduced:
        if c in encountered:
            indirect = sais("".join([str(x) for x in reduced]) + "$")[1:]
            return indirect
        encountered[c] = True
    return build_suffix_directly(reduced)[1:]

def build_suffix_directly(reduced : list[int]):
    sa = [-1]*(len(reduced)+1)
    sa[0] = len(reduced)
    for i in range(len(reduced)):
        sa[reduced[i] + 1] = i;
    return sa



def get_types_and_lms_characters(string):
    types = ['']*len(string)
    lms_chars = []
    lms_strings = {len(string)-1: "$"}

    types[-1] = "S"

    for i in range(len(string)-2, -1, -1):
        c = string[i]

        # Determine type
        if string[i] == string[i+1]:
            types[i] = types[i+1]
        else:
            types[i] = 'L' if string[i] > string[i+1] else 'S'

        # Determine if LMS
        if types[i] == 'L' and types[i+1] == 'S':
            lms_chars.append(i+1)
            if len(lms_chars) > 1:
                lms_strings[i+1] = (string[lms_chars[-1]:lms_chars[-2]+1])

    return types, lms_chars, lms_strings

def get_bucket_pointers(string):
    buckets = {}
    for c in string:
        buckets[c] = buckets.get(c, 0) + 1
    pointers = [0]*len(buckets.keys())
    sorted_chars = sorted(buckets.keys())
    for i,c in enumerate(sorted_chars):
        if i == len(sorted_chars)-1:
            break
        pointers[i+1] = pointers[i] + buckets[c]


    # Get end pointers
    pointers_end = []
    for p in pointers[1:]:
        pointers_end.append(p-1)
    pointers_end.append(len(string)-1)

    sorted_char_mapping = {sorted_chars[i]: i for i in range(len(sorted_chars))}


    return pointers, pointers_end, sorted_char_mapping


def passes(string, types, lms_chars, reverse_first_pass=False):
    start,end,sorted_char_mapping = get_bucket_pointers(string)

    sa = [-1]*(len(string))

    # First pass
    first_pass_lms = reversed(lms_chars) if reverse_first_pass else lms_chars
    end_copy = end.copy()
    for lms_i in first_pass_lms:
        bucket = sorted_char_mapping[string[lms_i]]
        index = end_copy[bucket]
        sa[index] = lms_i
        end_copy[bucket] -= 1


    # Second pass
    for suf in sa:
        suf_to_consider = suf-1
        if suf_to_consider >= 0 and types[suf_to_consider] == 'L':
            bucket = sorted_char_mapping[string[suf_to_consider]]
            index = start[bucket]
            sa[index] = suf_to_consider
            start[bucket] += 1

    # Third pass
    for i in range(len(sa)-1, -1, -1):
        suf = sa[i]
        suf_to_consider = suf-1
        if suf_to_consider >= 0 and types[suf_to_consider] == 'S':
            bucket = sorted_char_mapping[string[suf_to_consider]]
            index = end[bucket]
            sa[index] = suf_to_consider
            end[bucket] -= 1
    return sa

def main():
    # test = "BANANA$"
    # test = "mmiissiissiippii$"
    # test = "ACGTGCCTAGCCTACCGTGCC$"


    # Failing
    # test = "tatcgacaagacagaacagctatac$"
    test = "baacacaababbadacbcabaacbcab$"
    suf = sais(test)
    print(suf)

@hp.given(st.text(alphabet=['a', 'b', 'c', 'd']))
@hp.settings(max_examples=10000)
def hyp_test(inp_string):
    inp_string = inp_string + "$"
    suf = sais(inp_string)

    assert -1 not in suf

if __name__ == "__main__":
    # hyp_test()
    main()
