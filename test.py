from Notebook import Notebook
from Note import Note
from Section import Section
import json
from Network import Network
import base64


def json_to_notebook(nb):
    notebook = Notebook()
    nb = json.loads(nb)

    for s in nb:
        print(s[0])
        notebook.add_section(Section(s[0]))
        for n in s[1]:
            print(n)
            notebook.sections[-1].add_note(Note(n[0], n[1]))
    return notebook


def notebook_to_json(notebook):
    nb = []
    for s in notebook.sections:
        nb.append((s.name, [(n.name, n.data) for n in s.notes]))
    return json.dumps(nb)


if __name__ == '__main__':
    nt = Notebook('a')
    nt.add_section(Section('مشکلات'))
    nt.add_section(Section('مستقلات'))
    nt.sections[0].add_note(Note('مناسب', 'مهارت های ابتدایی'))
    nt.sections[1].add_note(Note('تعهد', 'به زمانه های پلید'))

    net = Network("http://127.0.0.1:8000/noteserver/")
    net.login_user('a', 'aa')
    res = net.update_notebook(nt)
