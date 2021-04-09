import pandas as pd

responses =[[0,-1], [1, -1], [2, -1], [3, -1], [4, -1], [5, -1], [6, -1], [7, -1], [8, -1], [9, -1], [10, -1], [11, -1], [12, -1]]

df_responses = pd.DataFrame(responses, columns = ['Question', 'Response'])

df_responses.to_csv("Responses.csv")

print(df_responses['Response'][1])
df_responses['Response'][1] = 2
print(df_responses)