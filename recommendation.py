import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
import pulp

df = pd.read_csv('data/nutrition.csv')
df = df[['name', 'calories', 'total_fat', 'protein', 'water', 'carbohydrate', 'fiber']]
# print(df)
lists = ['protein', 'water', 'carbohydrate','fiber']
for col in lists:
    df[col] = df[col].str.replace(' g', '', regex=False)
    df[col] = df[col].astype('float')
    
week_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
split_values = np.linspace(0,len(df),8).astype(int)
split_values[-1] = split_values[-1]-1
def random_dataset():
    frac_data = df.sample(frac=1).reset_index().drop('index',axis=1)
    day_data = []
    for s in range(len(split_values)-1):
        day_data.append(frac_data.loc[split_values[s]:split_values[s+1]])
    return dict(zip(week_days,day_data))

# print(random_dataset()['Monday'])

def build_nutritional_values(kg,calories):
    protein_calories = kg*4
    res_calories = calories-protein_calories
    carb_calories = calories/2.
    fat_calories = calories-carb_calories-protein_calories
    res = {'Protein Calories':protein_calories,'Carbohydrates Calories':carb_calories,'Fat Calories':fat_calories}
    return res

def extract_gram(table):
    protein_grams = table['Protein Calories']/4.
    carbs_grams = table['Carbohydrates Calories']/4.
    fat_grams = table['Fat Calories']/9.
    res = {'Protein Grams':protein_grams, 'Carbohydrates Grams':carbs_grams,'Fat Grams':fat_grams}
    return res


def diet_reccomend(weight, calories):
  return (build_nutritional_values(weight,calories))

# days_data = random_dataset()
# def model(day,kg,calories):
#     G = extract_gram(build_nutritional_values(kg,calories))
#     E = G['Carbohydrates Grams']
#     F = G['Fat Grams']
#     P = G['Protein Grams']
#     day_data = days_data[day]
#     day_data = day_data[day_data.calories!=0]
#     food = day_data.name.tolist()
#     c  = day_data.calories.tolist()
#     x  = pulp.LpVariable.dicts( "x", indices = food, lowBound=0, upBound=1.5, cat='Continuous', indexStart=[] )
#     e = day_data.carbohydrate.tolist()
#     f = day_data.total_fat.tolist()
#     p = day_data.protein.tolist()
#     prob  = pulp.LpProblem( "Diet", pulp.LpMinimize )
#     prob += pulp.lpSum( [x[food[i]]*c[i] for i in range(len(food))]  )
#     prob += pulp.lpSum( [x[food[i]]*e[i] for i in range(len(x)) ] )>=E
#     prob += pulp.lpSum( [x[food[i]]*f[i] for i in range(len(x)) ] )>=F
#     prob += pulp.lpSum( [x[food[i]]*p[i] for i in range(len(x)) ] )>=P
#     prob.solve()
#     variables = []
#     values = []
#     for v in prob.variables():
#         variable = v.name
#         value = v.varValue
#         variables.append(variable)
#         values.append(value)
#     values = np.array(values).round(2).astype(float)
#     sol = pd.DataFrame(np.array([food,values]).T, columns = ['Food','Quantity'])
#     sol['Quantity'] = sol.Quantity.astype(float)
#     return sol


# # sol_monday = model(2,70,1500)
# # print(sol_monday)
# def total_model(kg,calories):
#     result = []
#     for day in week_days:
#         prob  = pulp.LpProblem( "Diet", pulp.LpMinimize )
#         print('Building a model for day %s \n'%(day))
#         result.append(model(prob,day,kg,calories))
#     return dict(zip(week_days,result))


# print(model('Monday',70,1500))
# def total_model(kg,calories):
#     result = []
#     for day in week_days:
#         prob  = pulp.LpProblem( "Diet", pulp.LpMinimize )
#         print('Building a model for day %s \n'%(day))
#         result.append(model(prob,day,kg,calories))
#     return dict(zip(week_days,result))

# # diet = total_model(70,3000)