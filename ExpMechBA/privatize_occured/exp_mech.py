import numpy as np

GS_SCORE = 1  # score has sensitivity of 1


def score(output_universes):
    return [x for x in np.flip(output_universes)]


def exp_mech(output_universes, epsilon):
    scores = score(output_universes)
    #print(scores, flush=True) #Debugging statement to catch NaN error
    raw_prob = [np.exp((epsilon * x) / (2 * GS_SCORE)) for x in scores]
    #print(raw_prob, flush=True) #Debugging statement to catch NaN error
    max_value = np.sum(raw_prob)
    #print(max_value, flush=True) #Debugging statement to catch NaN error
    prob = [x / max_value for x in raw_prob]
    #print(prob, flush=True)
    #print(output_universes, flush=True) #Debugging statement to catch NaN error
    return np.random.choice(output_universes, p=prob)
