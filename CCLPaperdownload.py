#!/usr/bin/env python3
# coding:utf-8
# File:CCLdownload.py
# Author:lhy<lhy_in_blcu@126.com>
# Date:2018/10/18

import urllib.request
import os
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class CCL2018:
    def __init__(self):
        self.cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.paper_dir = os.path.join(self.cur_dir, 'papers')
        if not os.path.exists(self.paper_dir):
            os.makedirs(self.paper_dir)

    '''下载主函数，将下载的论文存储在papers文件当中'''
    def download_paper(self):
        for page in range(1, 103):
            if page < 10:
                _page = '00' + str(page)
            elif page < 100:
                _page = '0' + str(page)
            else:
                _page = str(page)
            try:
                url = 'http://cips-cl.org/static/anthology/CCL-2018/CCL-18-{}.pdf'.format(_page)
                file_name = os.path.join(self.paper_dir, _page+'.pdf')
                print(url)
                urllib.request.urlretrieve(url,file_name )
            except Exception as e:
                print(e)
        return

    '''解析论文名称，对下载的论文进行重命名'''
    def extract_papaername(self, path):
        title = ''
        contents = []
        fp = open(path, 'rb')
        praser = PDFParser(fp)
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
            for page in doc.get_pages():
                try:
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for x in layout:
                        if (isinstance(x, LTTextBoxHorizontal)):
                            content = x.get_text().replace('\n','')
                            contents.append(content)
                except Exception as e:
                    print(e)
                    print('document error...')
        if not contents:
            return
        else:
            id_index = 11
            for indx, line in enumerate(contents[:10]):
                if '文章编号' in line:
                    id_index = indx
                    break
            if id_index == 11:
                title_indx = 0
            else:
                title_indx = id_index + 1
            title = contents[:10][title_indx]
            if len(title.replace(' ', '')) < 4:
                title = contents[:10][title_indx+1]

        return title.replace('\uf02a', '').replace('*', '')

    '''对文档进行重命名'''
    def rename_papers(self):
        for root, dirs, files in os.walk(self.paper_dir):
            for file in files:
                filepath = os.path.join(root, file)
                print(filepath)
                title = self.extract_papaername(filepath)
                if not title:
                    title = file
                new_filepath = os.path.join(self.paper_dir, title + '.pdf')
                try:
                    os.renames(filepath, new_filepath)
                except Exception as e:
                    print('file error')
        return


handler = CCL2018()
handler.download_paper()
handler.rename_papers()