import json 


# JSON file 
f = open ('./ch1.json', "r") 
  
# Reading from file 
data = json.loads(f.read()) 


print(data['fullTextAnnotation']['text'])
# document = response.full_text_annotation

# print(data)
# for i in range(len(data['responses'])): 
#     print(i)
#     input()
