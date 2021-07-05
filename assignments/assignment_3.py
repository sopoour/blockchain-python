# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
people = [{'name': 'Sophia', 'age': 24, 'hobbies': ['skiing', 'piano', 'tennis']}, {'name': 'Alex', 'age': 27, 'hobbies': ['football', 'gym', 'dancing']}, {'name': 'Sarah', 'age': 21, 'hobbies': ['drawing', 'running']}]
print(people)
# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).
people_names = [person['name'] for person in people]
print(people_names)
# 3) Use a list comprehension to check whether all persons are older than 20.
check_age = all([person['age'] > 20 for person in people])
print(check_age)
# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
#Wrong since only shallow copy and it doesn't copy the dictionaries inside:
#copied_people = people[:]
#with the following the above copy is enough and it works fine but in case you want to change something inside of one of the persons then that won't do
#copied_people.append({'name': 'Julia', 'age': 17, 'hobbies': ['guitar', 'volleyball']})
copied_people = [person.copy() for person in people]
copied_people[0]['name'] = 'Sopo'
print(copied_people)
print(people)
# 5) Unpack the persons of the original list into different variables and output these variables.
sophia, alex, sarah = people

print(' Person1:', sophia,'\n','Person2:', alex,'\n', 'Person3:', sarah)
