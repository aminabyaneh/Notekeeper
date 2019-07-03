from Notebook import Notebook
from Note import Note
from Section import Section
from Network import Network

if __name__ == '__main__':
    nb = Notebook('aminabyaneh')
    nb.add_section(Section('مهمات'))
    nb.sections[0].add_note(Note('مناسب', 'مهارت های ابتدایی'))

    net = Network("http://127.0.0.1:8000/noteserver/")
    print(net.token)
    a = net.login_user('a', 'aa')
    print(a[0])
    a = net.logout_user()
    print(a[0])

