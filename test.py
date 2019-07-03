from Notebook import Notebook
import pickle

if __name__ == '__main__':
    nb = Notebook('aminabyaneh')
    str_nb = pickle.dumps(nb)
    print(str_nb)
    nb_new = pickle.loads(str_nb)

