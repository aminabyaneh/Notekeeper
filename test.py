from Notebook import Notebook
from Note import Note
from Section import Section
from Network import Network
import time

if __name__ == '__main__':
    nt = Notebook('a')
    nt.add_section(Section('مشکلات'))
    nt.add_section(Section('مستقلات'))
    nt.sections[0].add_note(Note('مناسب', 'مهارت های ابتدایی'))
    nt.sections[1].add_note(Note('تعهد', 'به زمانه های پلید'))

    net = Network("http://127.0.0.1:8000/noteserver/")
    net.login_user('a', 'aa')
    res = net.set_timer("solei1997@live.com", "testi", time.time() + 50)
