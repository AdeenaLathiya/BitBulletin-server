import json
from summarizeFunc import text_summarizer

# with open('webScraping.json') as f:
#    data = json.load(f)

# print(json.dumps(data, indent=4, sort_keys=True))

# loaded_json = json.loads(f)
# for x in loaded_json:
# 	print("%s: %d" % (x, loaded_json[x]))

# class Test(object):
#     def __init__(self, data):
# 	    self.__dict__ = json.loads(data)

# test1 = Test(json_data)
# print(test1.a)
with open('webScraping.json', 'r') as f:
    distros_dict = json.load(f)

for distro in distros_dict:
    print(distro['content'])
    # text_summarizer(distro['content'])
