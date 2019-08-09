# -*- coding: utf-8 -*-

import os
import time
import copy
import re
from shutil import copyfile
from optparse import OptionParser

import markdown
import jinja2
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from docdata.mmddata import get_data


class MyHandler(FileSystemEventHandler):
    def __init__(self, infile):
        self.infile = infile

    def dispatch(self, event):
        slides(self.infile)
        print "updated slides"

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input",
        dest="filename",
        help="markdown file holding your slides and configs",
        default='slides.md',
        metavar="SLIDES.md")
    parser.add_option("-w", "--watch", action="store_true", dest="watch", default=False)

    (options, args) = parser.parse_args()

    print 'processing:', options.filename
    #try:
    S = slides(options.filename)
    htmlfile = S.outputPath
    print 'done writing to html:', htmlfile
    #pdffile = S.pdffile
    #if S.to_pdf:
    #    export_topdf(htmlfile, pdffile)

    if options.watch:
        print "start watching changes"
        print "to stop watching, press ctrl+c"
        observer = Observer()
        event_handler = MyHandler(options.filename)
        path =  os.path.dirname(os.path.abspath(options.filename))
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        print ""
        print "watching stop"
    #print "checking"
    #if S.to_pdf:
    #    export_topdf(htmlfile, pdffile)

def check_mkdir(outpath):
    directory = os.path.dirname(outpath)
    if not os.path.exists(directory):
        print 'creating dir:', directory
        os.makedirs(directory)

def text_export(outputText, outputPath):
    check_mkdir(outputPath)
    #print 'writing file to:', outputPath
    f = open(outputPath, 'w')
    f.write(outputText.encode("utf-8"))
    f.close()

def copy_directories(static_path_in, static_path_out):
    for dirName, subdirList, fileList in os.walk(static_path_in):
        for fname in fileList:
            inf = os.path.join(dirName,fname)
            relf = os.path.relpath(inf, static_path_in)
            outf = os.path.join(static_path_out, relf)
            check_mkdir(outf)
            copyfile(inf, outf)

"""
def export_topdf(htmlfile, pdffile):
    #print htmlfile
    pyrev_path = os.path.dirname(__file__)
    deckloc = os.path.join(pyrev_path, 'decktape')
    print deckloc
    bashCommand = "phantomjs %s/decktape.js reveal %s %s"%(deckloc, htmlfile, pdffile)
    print 'writing slides to ', pdffile
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print 'Error message:', error
"""

class slides():
    def __init__(self, afile):
        doc, config = self.process_md(afile)
        slides_content, chapter_list = self.process_slides(doc)
        #print doc, config

        base_dir = os.path.abspath(os.path.dirname(afile))
        base_name = os.path.basename(afile)

        output_dir = ''
        if 'output_dir' in config:
            output_dir = config['output_dir']
            del config['output_dir']

        output_fname = '%s.slides.html'%base_name.replace('.md','')
        if 'output_filename' in config:
            output_fname = config['output_filename']
            del config['output_filename']

        if 'toc' in config:
            if config['toc'].lower().replace(' ','')=='true':
                config['toc'] = True
            else:
                config['toc'] = False

        if 'use_katex' in config:
            if config['use_katex'].lower().replace(' ','')=='true':
                config['use_katex'] = True
            else:
                config['use_katex'] = False

        if 'reveal_path' in config:
            reveal_path = config['reveal_path']
            #del config['reveal_path']
        else:
            reveal_path = 'reveal.js'
            config['reveal_path'] = reveal_path

        if not 'transition' in config:
            config['transition'] = 'none'

        if not 'theme' in config:
            config['theme'] = 'black'

        if 'cr_word' in config:
            if config['cr_word']=='--':
                config['cr_word'] = None
            if not 'cr_color' in config:
                config['cr_color'] = 'rgba(205,205,205,0.0)'

        if not 'background' in config:
            config['background'] = None
            if ('bgrepeat' in config) and (config['bgrepeat'].lower()=='true'):
                config['bgrepeat'] = True
            else:
                config['bgrepeat'] = False
            if not 'bgsize' in config:
                config['bgsize'] = None

        """
        pdf_filename = None
        to_pdf = False
        if 'pdf_filename' in config:
            pdf_filename = config['pdf_filename']
            del config['pdf_filename']
        elif 'to_pdf' in config:
            if config['to_pdf'].lower()=='true':
                to_pdf = True
            else:
                to_pdf = False
            del config['to_pdf']
        self.to_pdf = to_pdf
        """

        if 'use_katex' in config and (config['use_katex'].lower()=='true'):
            config['use_katex'] = True
        else:
            config['use_katex'] = False

        if 'menu_bottom' in config and (config['menu_bottom'].lower()=='true'):
            config['menu_bottom'] = True
        else:
            config['menu_bottom'] = False

        maindic = {}
        maindic['slides_contents'] = slides_content
        maindic.update(config)

        if len(chapter_list)>0:
            maindic.update({'chapters': chapter_list})
            if not('use_simplemenu' in config):
                maindic.update({'use_simplemenu': True})
            else:
                if config['use_simplemenu'].lower()=='true':
                    maindic.update({'use_simplemenu': True})
                else:
                    maindic.update({'use_simplemenu': False})
        else:
            maindic.update({'use_simplemenu': False})


        pyrev_path = os.path.dirname(__file__)
        template_path = os.path.join(pyrev_path,'templates')
        templateLoader = jinja2.FileSystemLoader( searchpath=template_path )
        templateEnv = jinja2.Environment( loader=templateLoader )
        TEMPLATE_FILE = "base.html"
        template = templateEnv.get_template( TEMPLATE_FILE )
        outputText = template.render( maindic )
        #print outputText

        outputPath = os.path.join(base_dir, output_dir, output_fname)
        self.outputPath = outputPath
        #self.pdffile = outputPath.replace('.html','.pdf')
        #if not pdf_filename is None:
        #    self.pdffile = pdf_filename

        text_export(outputText, outputPath)

        #print reveal_path
        if not reveal_path[:4]=='http':
            reveal_path_f = os.path.abspath(os.path.join(base_dir, reveal_path))
            if not os.path.exists(reveal_path_f):
                src = os.path.join(pyrev_path,'reveal_js')
                copy_directories(src, reveal_path_f)
        #base_dir_f = os.path.abspath(base_dir)
        #reveal_path0 = os.path.relpath(reveal_path_f, base_dir_f)
        #reveal_path0 = os.path.join(base_dir, reveal_path)
        #print reveal_path_f
        #print base_dir_f

        if config['use_katex']:
            katex_path = os.path.join(base_dir, output_dir, 'plugin', 'katex')
            if not os.path.exists(katex_path):
                katex_src = os.path.join(pyrev_path,'reveal_js', 'plugin', 'katex')
                copy_directories(katex_src, katex_path)


    def process_md(self, afile):
        with open(afile, 'r') as f:
            doc = f.read()
        doc, config = get_data(doc)
        doc = doc.decode('utf-8')
        #print doc
        config2 = {}
        for k,v in config.iteritems():
            config2[k] = ' '.join(v)
        return doc, config2

    def process_slides(self, doc):
        lines = doc.split('\n')

        sections = []
        asection = []
        for l in lines:
            if l!='---right':
                asection.append(l)
            else:
                #print asection
                sections.append(asection)
                asection = []
            #print l
        if len(asection)>0:
            sections.append(asection)
            asection = []
        #print sections

        slides = []
        for asection in sections:
            asetofslide = []
            aslide = []
            #print asection
            for l in asection:
                if l!='---down':
                    aslide.append(l)
                else:
                    #asetofslide.append('\n'.join(aslide))
                    asetofslide.append(aslide)
                    aslide = []
            if len(aslide)>0:
                #asetofslide.append('\n'.join(aslide))
                asetofslide.append(aslide)
                aslide = []
            slides.append(asetofslide)

        slides_strs_list = []
        chapter_list = []
        for asetofslide in slides:
            slide_strs = ''
            #print len(asetofslide)
            chap_name = ''
            chap_id = ''
            for s in asetofslide:
                slide_str, chap_item = self.process_a_slide(s)
                slide_strs += slide_str
                if len(chap_name)==0: chap_name = chap_item
            if len(chap_name)>0:
                chap_id = chap_name.replace(' ','-')
                chapter_list.append((chap_id, chap_name))
                if len(asetofslide)>1:
                    ## add menu things in section tags
                    slide_strs = slide_strs.replace('<section', '<section id="'+chap_id+'"', 1)
                    slide_strs = '<section data-menu-title="'+chap_id+'">\n'+slide_strs+'</section>\n'
                else:
                    # got chapter name but only one slide
                    slide_strs = slide_strs.replace('<section', '<section id="'+chap_id+'" data-menu-title="'+chap_id+'"', 1)
            else:
                # no chapter name
                if len(asetofslide)>1:
                    slide_strs = '<section>\n'+slide_strs+'</section>\n'

            slides_strs_list.append(slide_strs)
        contents_str = ' '.join(slides_strs_list)
        chapter_list2 = []
        for chap_id, chap_name in chapter_list:
            if not((chap_id,chap_name) in chapter_list2):
                chapter_list2.append((chap_id, chap_name))
        return contents_str, chapter_list2

    def process_a_slide(self, slide_list):
        #print slide_list
        bg = []
        main_text = []
        notes = []
        chap_item = ''
        maintx = True
        #frag_now = False
        frag_type = None
        frag_div = ['---fragment_current-visible', '---fragment_fade-up', '---fragment_fade-down', '---fragment_fade-left', '---fragment_fade-right', '---fragment_fade-out', '---fragment_grow', '---fragment_shrink']
        frag_span = ['---fragment_highlight-red', '---fragment_highlight-blue', '---fragment_highlight-green', '---fragment']
        frag_close = '---fragment_close'
        for l in slide_list:
            #print l
            if l[:7]=='---data':
                bg.append(l[3:])
            elif l[:8]=='---style':
                bg.append(l[3:])
            elif l[:11]=='---fragment':
                if l==frag_close:
                    if frag_type=='div':
                        main_text.append('</div>')
                    else:
                        main_text.append('</span>')
                    frag_type = None
                else:
                    if not frag_type is None:
                        if frag_type=='div':
                            main_text.append('</div>')
                        else:
                            main_text.append('</span>')
                        frag_type = None
                    #else:
                    #    frag_now = True
                    if l in frag_div:
                        f_str = l[3:].replace('_',' ')
                        main_text.append('<div class="%s">'%f_str)
                        frag_type = 'div'
                    else:
                        f_str = l[3:].replace('_',' ')
                        main_text.append('<span class="%s">'%f_str)
                        frag_type = 'span'
            elif l[:8]=='---notes':
                maintx = False
            elif l[:11]=='---chapter=':
                chap_item = l[11:]
            else:
                if maintx:
                    main_text.append(l)
                else:
                    notes.append(l)


        if not frag_type is None:
            if frag_type=='div':
                main_text.append('</div>')
            else:
                main_text.append('</span>')
            frag_type = None

        ## should be here for check_icons
        main_text2 = []
        for line in main_text:
            main_text2.append(self.check_icons(line))
        main_text = main_text2

        main_text_str = '\n'.join(main_text)
        #print main_text_str

        if len(bg)>0:
            bg_str = ' '+' '.join(bg)
            #print bg_str
        else:
            bg_str = ''

        md = markdown.Markdown()
        html = md.convert(main_text_str)

        if len(notes)>0:
            notes_str = ''
            for n in notes:
                notes_str = notes_str + '<p>'+n+'</p>\n'
            notes_str = '<aside class="notes">\n' + notes_str + '</aside>\n'
            html = html + notes_str

        html = '<section'+bg_str+'>\n'+html+'\n</section>\n'
        return html, chap_item

    def check_icons(self, astring):
        sets = ['fab', 'fas', 'fal', 'far', 'fad']
        patterns = [ '\:{}-(.*?)\:'.format(setname) for setname in sets ]
        matches = [ re.findall(pat, astring) for pat in patterns ]
        bstring = copy.copy(astring)
        for mat, setname in zip(matches, sets):
            for m1 in mat:
                tag = '<i class="{} fa-{}"></i>'.format(setname, m1)
                target = ':{}-{}:'.format(setname, m1)
                bstring = bstring.replace(target, tag)

        pat_typcn = '\:typcn-(.*?)\:'
        mat = re.findall(pat_typcn, bstring)
        for m1 in mat:
            tag = '<span class="typcn typcn-{}"></span>'.format(m1)
            target = ':typcn-{}:'.format(m1)
            bstring = bstring.replace(target, tag)
        return bstring

if __name__ == '__main__':
    afile = 'testing/test.md'
    S = slides(afile)
