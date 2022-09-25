import requests
import zipfile
import os
import argparse

from jobs.core.main import setup_logger, f_periodo_v6

log = setup_logger('BovespaDownloadFile')

def f_bovhist(dias):
	for ano in f_periodo_v6(dias=dias, fmt='%Y'):

		log.info(f'fazendo download do ano {ano}')
		site = 'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{}.ZIP'.format(str(ano))
		file = 'tmp/' + site.split('/')[-1]
		
		s = requests.get(site, verify=False)
		
		with open(file, 'wb') as f:
			f.write(s.content)
		
		Zip = zipfile.ZipFile(file, 'r')
		
		with zipfile.ZipFile(file, 'r') as f:
			f.extractall(file.split('/')[0])
		
		Zip.close()
		
		os.remove(file)
		log.info(f'download finalizado')

if __name__ == '__main__':

	dias = 10000
	log.info(f'Dias:{dias}')
	f_bovhist(dias)