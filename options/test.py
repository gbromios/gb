from parser import parse
from odict import ODict
from option import Options

import sys

def deep_cmp(a, b, wsl=0, name='', delim='  '):
	# definitely need to be the same type of thing!
	if type(a) != type(b):
		print(
			"{0}can't compare {1}({2}) and ({3})\n{0}'{4}'\n{0}'{5}'\n{0}//\n"
			.format((delim * wsl), name, type(a), type(b), str(a)[:50], str(b)[:50])
		)
		return False

	if isinstance(a, list):
		# lists should be in order as well as contain the same items!
		if len(a) != len(b):
			print(
				"{0}{1}a() and b() are unequal length!\n{0}a: '{2}'\n{0}b: '{3}'"
				.format((delim * wsl) , name, str(a)[:50], str(b)[:50])
			)
			return False

		same = True
		for i in range(len(a)):
			ai = a[i]
			bi = b[i]

			if not deep_cmp(ai, bi, wsl=wsl+1, name=("{0}[{1}]".format(name, i)), delim=delim):
				same = False

		return same

	elif isinstance(a, dict):
		same = True
		for k in set(a.keys()).union(set(b.keys())):
			try:
				av = a[k]

			except KeyError:
				print(
				"{0}{1}.{2} not in a! (b.{2}: '{3}')"
				.format((delim * wsl), name, k, str(b[k])[:50])
				)
				same = False
				continue

			try:
				bv = b[k]

			except KeyError:
				print(
				"{0}{1}.{2} not in b! (a.{2}: '{3}')"
				.format((delim * wsl), name, k, str(a[k])[:50])
				)
				same = False
				continue

			if not deep_cmp(av, bv, wsl=wsl+1, name=("{0}.{1}".format(name, k)), delim=delim):
				same = False

		return same

	# anything that's not a list or a dict:
	else:
		if a != b:
			print(
				"{0}{1}: [[ \033[1;31m!=\033[0m ]]\n{0}a: '{2}'\n{0}b: '{3}'"
				.format((delim * wsl) , name, str(a)[:100], str(b)[:100])
			);
			return False

	return True

try:
	filename = sys.argv[1]
	deep = False

except IndexError:
	filename = 'sample.conf'
	deep = True

a = parse(open(filename).read())
if deep:
	deep_cmp(a, ODict(
		cool_dude = "wat",
		steven = "collins",
		hello = "kitty,\" ?",
		puppies ='\\n\\n cute',
		puppies_2 = "even more PuPpIeS",
		tony_pepperony = "522",
		bloopers = "5120\nasdsaf\n\tblah blah. there's quoites, so it doesn't care about \"white\" space???",
		query = "avg # of number of head kicks per karate tournament (this isn't a comment btw)",
		things = [
			"1",
			"2",
			"watlol",
			"xen_is_best",
			"no",
			"kvm",
			"me",
			"too",
			"thanks",
			"whatever",
			"dude"
		],
		umm = [
			"ahem",
			"excuse me",
			"thank's",
			"your welcome",
			"beg your pardon"
		],
		perfect_system = dict(
			ayy = "lmao",
			can_hold = "0",
			why = "????",
			temperature = "100.04",
			those_one_guys_ya_know = [
				dict(
					name = "doge",
					mean = "sometimes",
					rules = "venice",
					tryhard = "0"
				),
				dict(
					name = "tony",
					mean = "very",
					kicks = "frequently",
					tryhard = "45"
				),
				dict(
					name = "Unicorn Rodeo",
					occupation = "JAMES C. UNICORN",
					tryhard = "999",
					mean = "never",
				)
			]
		)
	))

o = Options(a)

