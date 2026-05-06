import json

def sum_array(array):
    sum = 0
    for item in array:
        sum += item
    return sum

data = json.load(open("stats.json", "r"))
var_array = sorted(data["variance"], reverse=True)
i=0
sum = 0
while(sum < 0.95 * sum_array(var_array)):
    sum += var_array[i]
    i += 1
print(f"sum:{sum}, N_Items:{i}")

#ci sono tante dimensioni con varianza estremamente bassa ==> inutili, sono feature che vengono attivate in modo quasi identico per ogni font