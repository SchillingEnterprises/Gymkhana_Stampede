import re


with open("names.txt") as names_file:
    data = names_file.read()
    names_file.close()


last_name = r'Love'
first_name = r'Kenneth'


# print(re.match(last_name, data))
# print(re.search(first_name, data))
# print(re.findall(r'\(?\d{3}\)?-?\s?\d{3}-\d{4}', data))
# print(re.findall(r'\w*, \w+', data))
# print(re.findall(r'[-\w\d+.]+@[-\w\d.]+', data))             # r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" according to EmailRegex.com gets 99.99%
# print(re.findall(r'\b[trehous]{9}\b', data, re.IGNORECASE))  # re.IGNORECASE shorthands to re.I
# print(re.findall(r'''
#     \b@[-\w\d.]*                                             # First a word boundary, an @, and then any number of characters.
#     [^gov\t]+                                                # Ignore 1+ instances of the letters 'g', 'o', or 'v' and a tab.
#     \b                                                       # Match another word boundary.
# ''', data, re.VERBOSE | re.IGNORECASE))                      # re.VERBOSE shorthands to re.X
# print(re.findall(r'''
#     \b[-\w]+,                                                # Find word boundary, 1+ hyphen(s) or word characters, and a comma.
#     \s                                                       # Find 1 whitespace.
#     [-\w ]+                                                  # Find 1+ hyphen(s) or word characters, and explicit spaces.
#     [^\t\n]                                                  # Ignore tabs and new lines.
# ''', data, re.VERBOSE))
line = re.compile(r'''
    ^(?P<name>(?P<last>[-\w ]*),\s(?P<first>[-\w]+))\t         # Last and First Names
    (?P<email>[-\w\d.+]+@[-\w\d.]+)\t                          # Email Addresses
    (?P<phone>\(?\d{3}\)?-?\s?\d{3}-\d{4})?\t                  # Phone Numbers
    (?P<job>[\w\s]+,\s[\w\s.]+)\t?                             # Job & Company
    (?P<twitter>@[\w\d]+)?$                                    # Twitter
''', re.VERBOSE | re.MULTILINE | re.IGNORECASE)                # re.MULTILINE shorthands to re.M


# print(line.search(data).groupdict())
for match in line.finditer(data):
    print('{first} {last} <{email}>'.format(**match.groupdict()))