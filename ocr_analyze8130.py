import json 


# JSON file 
f = open ('processed_8130-1output-1-to-1.json', "r") 
  
# Reading from file 
data = json.loads(f.read()) 


# print(data['responses'])
# document = response.full_text_annotation


for i in range(len(data['responses'][0]['fullTextAnnotation']['pages'][0]['blocks'])): 
    print(data['responses'][0]['fullTextAnnotation']['pages'][0]['blocks'][i])
    input()
