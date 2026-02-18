import difflib, json, re, itertools

# Split words into lines
def text_to_wordlist(text):
    final_word_list = []
    words_list = text.replace(" ", "\n").split("\n")
    
    for element in words_list: 
        if len(element) >= 2: 
            final_word_list.append(element)
    
    return final_word_list

# Get regex data
def get_regexes():
    with open('definitions.json', "r", encoding='utf-8') as json_file:
        rules = json.load(json_file)
        return rules

# Match similarity
def similarity(a, b): return difflib.SequenceMatcher(None, a, b).ratio() * 100

# Identify email PIIs
def email_pii(rules, text):
    email_rules = rules["Email"]["regex"]
    email_addresses = re.findall(email_rules, text)
    email_addresses = list(set(filter(None, email_addresses)))
    return email_addresses

# Identify phone PIIs
def phone_pii(rules, text):
    phone_rules = rules["Phone Number"]["regex"]
    phone_numbers = re.findall(phone_rules, text)
    phone_numbers = list(itertools.chain(*phone_numbers))
    phone_numbers = list(set(filter(None, phone_numbers)))
    return phone_numbers

# Identify keyword PIIs
def keyword_pii(rules, text):
    results = []

    wordlist = text_to_wordlist(text)
    for key, rule in rules.items():
        keywords = rule.get("keywords", [])
        if keywords is not None:
            for word in wordlist:
                for keyword in keywords:
                    if similarity(word.lower()
                                  .replace(".", "")
                                  .replace("'", "")
                                  .replace("-", "")
                                  .replace("_", "")
                                  .replace(",", ""), keyword.lower()) > 80:
                        results.append(word)


    return results
