# -*- coding: utf-8 -*-
from optparse import OptionParser
import sys
import os
import subprocess
from shutil import copyfile
import copy
import markdown
from docdata.mmddata import get_data
import jinja2


def main():
    parser = OptionParser()
    parser.add_option("-i", "--input",
        dest="filename",
        help="markdown file holding your slides and configs",
        default='slides.md',
        metavar="SLIDES.md")
    (options, args) = parser.parse_args()
    print 'processing:', options.filename
    #try:
    S = slides(options.filename)
    print 'to html done'
    htmlfile = S.outputPath
    pdffile = S.pdffile
    print htmlfile, pdffile
    if S.to_pdf:
        #try:
        export_topdf(htmlfile, pdffile)
        #except:
        #    print 'export pdf failed somehow'
    #except:
    #    print 'Error opening markdown file'
    #    sys.exit()

def check_mkdir(outpath):
    directory = os.path.dirname(outpath)
    if not os.path.exists(directory):
        print 'creating dir:', directory
        os.makedirs(directory)

def text_export(outputText, outputPath):
    check_mkdir(outputPath)
    print 'writing file to:', outputPath
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

class slides():
    def __init__(self, afile):
        doc, config = self.process_md(afile)
        slides_content = self.process_slides(doc)
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
            if not 'cr_color' in config:
                config['cr_color'] = 'rgba(205,205,205,0.0)'

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


        maindic = {}
        maindic['slides_contents'] = slides_content
        maindic.update(config)

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
        self.pdffile = outputPath.replace('.html','.pdf')
        if not pdf_filename is None:
            self.pdffile = pdf_filename

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
        for asetofslide in slides:
            slide_strs = ''
            #print len(asetofslide)
            for s in asetofslide:
                slide_str = self.process_a_slide(s)
                slide_strs += slide_str
            if len(asetofslide)>1:
                slide_strs = '<section>\n'+slide_strs+'</section>\n'
            slides_strs_list.append(slide_strs)
        contents_str = ' '.join(slides_strs_list)
        return contents_str

    def process_a_slide(self, slide_list):
        #print slide_list
        bg = []
        main_text = []
        notes = []
        maintx = True
        frag_now = False
        for l in slide_list:
            #print l
            if l[:7]=='---data':
                bg.append(l[3:])
            elif l[:8]=='---style':
                bg.append(l[3:])
            elif l[:11]=='---fragment':
                if frag_now:
                    main_text.append('</p>')
                else:
                    frag_now = True
                f_str = l[3:].replace('_',' ')
                main_text.append('<p class="%s">'%f_str)
            elif l[:8]=='---notes':
                maintx = False
            else:
                if maintx:
                    main_text.append(l)
                else:
                    notes.append(l)
        if frag_now:
            main_text.append('</p>')

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
        return html

if __name__ == '__main__':
    afile = 'testing/test.md'
    S = slides(afile)
