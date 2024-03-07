from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from collections import defaultdict, deque
from itertools import count

def aho_corasick():
    G = defaultdict(count(1).__next__)  # transitions
    W = defaultdict(set)                # alphabet
    F = defaultdict(lambda: 0)          # fallbacks
    O = defaultdict(set)                # outputs
    
    # automaton
    return G, W, F, O

def add_word(word, G, W, F, O):
    state = 0
    # add transitions between states
    for w in word:
        W[state].add(w)
        state = G[state, w]
        
    # add output
    O[state].add(word)

def build_fsa(G, W, F, O):
    # initial states
    queue = deque(G[0, w] for w in W[0])
    
    while queue:
        state = queue.popleft()
        
        # for each letter in alphabet
        for w in W[state]:
            # find fallback state
            t = F[state]
            while t and (t, w) not in G:
                t = F[t]
                
            # for next state define its fallback and output
            s = G[state, w]
            F[s] = G[t, w] if (t, w) in G else 0
            O[s] |= O[F[s]]
            
            queue.append(s)

def search_in_pdf(text, G, W, F, O):
    state = 0
    
    for i, t in enumerate(text):
        # fallback
        while state and (state, t) not in G:
            state = F[state]
            
        # transition
        state = G[state, t] if (state, t) in G else 0
        
        # output
        if O[state]:
            print('@', i, O[state])

# PDF文档解析
path = r"D:\Documents\WeChat Files\wxid_lsootbrkhf4x22\FileStorage\File\2024-01\录入文献\录入文献\袁梦石以天地转气汤为主治疗中重度阿尔茨海默病经验总结_罗慧.pdf"

praser = PDFParser(open(path, 'rb'))
doc = PDFDocument()
praser.set_document(doc)
doc.set_parser(praser)
doc.initialize()

if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
else:
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # 获取PDF中的文本内容
    pdf_text = ""
    for page in doc.get_pages():
        interpreter.process_page(page)                        
        layout = device.get_result()
        for x in layout:
            if isinstance(x, LTTextBox):
                pdf_text += x.get_text()

    # 示例中药名称搜索
    G, W, F, O = aho_corasick()
    add_word("远志", G, W, F, O)
    add_word("石菖蒲", G, W, F, O)
    add_word("川芎", G, W, F, O)

    build_fsa(G, W, F, O)

    # 在PDF文本中搜索中药名称
    search_in_pdf(pdf_text, G, W, F, O)
    print(pdf_text)
