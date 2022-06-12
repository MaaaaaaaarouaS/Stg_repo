import numpy as np
from scipy.stats import norm

#Calculate delta of an option
def delta(r, S, K, T, sigma,type):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    if type == "c":
        delta = norm.cdf(d1, 0, 1)
    elif type == "p":
        delta = norm.cdf(d1, 0, 1)-1
    else:
        raise Exception("Veuillez vérifier le type de l'option,'c' pour une option call et 'p' pour une option put !")
    return delta

#Calculate gamma of a option
def gamma(r, S, K, T, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    return norm.pdf(d1, 0, 1)/(S*sigma*np.sqrt(T))


#Calculate vega of an option
def vega(r, S, K, T, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    return S*norm.pdf(d1, 0, 1)*np.sqrt(T)*0.01

#Calculate theta of an option
def theta(r, S, K, T, sigma, type="c"):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if type == "c":
        theta = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
    elif type == "p":
        theta= -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
    else:
        raise Exception("Veuillez vérifier le type de l'option,'c' pour une option call et 'p' pour une option put !")
    return theta/365

#Calculate option price of call/put
def prime(r, S, K, T, sigma, type="c"):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if type == "c":
        price = S*delta(r, S, K, T, sigma, type="c") - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
    elif type == "p":
        price = S*delta(r, S, K, T, sigma, type="p")+ K*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
    else:
        raise Exception("Veuillez vérifier le type de l'option,'c' pour une option call et 'p' pour une option put !")
    return price