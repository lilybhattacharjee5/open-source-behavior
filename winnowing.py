import sys
import math

def global_pos(min_idx, window_right_end, window_size):
	return 0

def record(winnowed_hashes, hash_val, global_pos):
	winnowed_hashes.append((hash_val, global_pos))
	# return

def winnow(w, hash_list):
	winnowed_hashes = []
	# circular buffer implementing window of size w
	h = {}

	for i in range(w):
		h[i] = sys.maxsize
		# h[i] = hash_list[0]
		# hash_list = hash_list[1:]
	# h[w - 1] = sys.maxsize

	r = 0 # window right end
	min_idx = 0 # index of min hash
	shift = 0
	# at the end of each iteration, min holds the position of the rightmost min hash in the curr window
	# record(x) is called only the 1st time an instance of x is selected as the rightmost min hash of a window
	while True:
		r = (r + 1) % w # shift the window by 1
		try:
			h[r] = hash_list[0] # and add 1 new hash
			hash_list = hash_list[1:]
			shift += 1
		except:
			break
		if min_idx == r:
			# the prev min is not in this window anymore
			# scan h left starting from r for the rightmost min hash
			# note min starts with the idx of the rightmost hash
			i = (r - 1) % w
			while i != r:
				if h[i] < h[min_idx]:
					min_idx = i
				i = (i - 1 + w) % w
			record(winnowed_hashes, h[min_idx], shift + min_idx - (r + 1) % 4)
		else:
			# otherwise, the prev min is still in this window
			# compare against the new val & update min if necessary
			if h[r] <= h[min_idx]:
				min_idx = r
				record(winnowed_hashes, h[min_idx], shift - 1)
	return winnowed_hashes[w - 1:]

def clean_text_english(text):
	# remove whitespace
	new_text = text.replace(' ', '')
	# remove capitalization
	new_text = new_text.lower()
	# remove punctuation
	new_text = new_text.replace(',', '')
	return new_text

def create_n_grams(cleaned_text, n):
	n_gram_list = [cleaned_text[:n]]
	count = 1
	while count <= len(cleaned_text) - n:
		new_n_gram = cleaned_text[count:count + n]
		n_gram_list.append(new_n_gram)
		count += 1
	return n_gram_list

def yield_next_hash(n_grams):
	count = 0
	while len(n_grams):
		curr_n_gram = n_grams[0]
		if count:
			hash_val = next_hash(prev_hash_val, prev_n_gram, curr_n_gram[len(curr_n_gram) - 1])
		else:
			hash_val = calculate_hash(curr_n_gram)
		yield hash_val
		prev_hash_val = hash_val
		prev_n_gram = curr_n_gram
		count += 1
		n_grams = n_grams[1:]

def generate_hashes(cleaned_text, n):
	hash_list = [calculate_hash(cleaned_text[:n])]
	count = 1
	while count <= len(cleaned_text) - n:
		new_char = cleaned_text[count + n - 1]
		new_hash = next_hash(hash_list[len(hash_list) - 1], cleaned_text[count - 1:count + n - 1], new_char)
		hash_list.append(new_hash)
		count += 1
	return hash_list

def calculate_hash(n_gram):
	val = 0
	count = 1
	while len(n_gram) > 0:
		curr_char = n_gram[len(n_gram) - 1]
		val += ord(curr_char) * count
		n_gram = n_gram[:len(n_gram) - 1]
		count *= 10
	return val

def next_hash(prev_hash, prev_n_gram, new_char):
	first_char = prev_n_gram[0]
	return int((prev_hash - ord(first_char) * math.pow(10, len(prev_n_gram) - 1)) * 10 + ord(new_char))

# can be changed by user
n = 5
window_size = 4

sample_text = "A do run run run, a do run run"

expected_cleaned_text = "adorunrunrunadorunrun"

# cleaning function may differ between languages
actual_cleaned_text = clean_text_english(sample_text)

assert actual_cleaned_text == expected_cleaned_text

# sequence of n-grams
expected_n_grams = [
	"adoru", "dorun", "orunr", "runru", "unrun", "nrunr", "runru", "unrun", "nruna", "runad", 
	"unado", "nador", "adoru", "dorun", "orunr", "runru", "unrun"
]

actual_n_grams = create_n_grams(actual_cleaned_text, n)

assert actual_n_grams == expected_n_grams

# compare the vals outputted by next_hash (dep) and calculate_hash (indep)
first_hash = calculate_hash(actual_n_grams[0]) # hashed "adoru"
# print(next_hash(first_hash, actual_n_grams[0], "d"))
# print(calculate_hash(actual_n_grams[1]))

# print(generate_hashes(actual_cleaned_text, n))

# try on test input
x = [77, 74, 42, 17, 98, 50, 17, 98, 8, 88, 67, 39, 77, 74, 42, 17, 98]
actual_winnowed_x = winnow(window_size, x)
expected_winnowed_x = [(17, 3), (17, 6), (8, 8), (39, 11), (17, 15)]

assert actual_winnowed_x == expected_winnowed_x

# print(winnow(window_size, generate_hashes(actual_cleaned_text, n)))
