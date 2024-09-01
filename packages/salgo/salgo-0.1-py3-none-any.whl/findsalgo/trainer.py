import numpy as np

def train(data):
    d = np.array(data)[:,:-1]
    target = np.array(data)[:,-1]

    print("\n The attributes are: ", d)
    print("\n The target is: ", target)

    def train(c, t):
        for i, val in enumerate(t):
            if val == "Yes":
                specific_hypothesis = c[i].copy()
                break

        for i, val in enumerate(c):
            if t[i] == "Yes":
                for x in range(len(specific_hypothesis)):
                    if val[x] != specific_hypothesis[x]:
                        specific_hypothesis[x] = '?'

        return specific_hypothesis

    print("\n The final hypothesis is:", train(d, target))