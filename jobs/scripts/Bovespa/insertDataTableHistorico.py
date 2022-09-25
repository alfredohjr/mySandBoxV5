import sqlite3
import datetime
import pandas as pd

from jobs.core.main import setup_logger, f_periodo_v6
from jobs.scripts.conf import bovespa_db

log = setup_logger('insertDataTableHistorico')

columns = [
	'tipreg', 
	'data', 
	'codbdi', 
	'codneg', 
	'tpmerc', 
	'nomres', 
	'especi', 
	'prazot', 
	'modref', 
	'preabe', 
	'premax', 
	'premin', 
	'premed', 
	'preult', 
	'preofc', 
	'preofv', 
	'quatot', 
	'voltot', 
	'preexe', 
	'indopc', 
	'datven', 
	'fatcot', 
	'ptoexe', 
	'codisi', 
	'dismes', 
	'totneg'
]

def convert_to_decimals(x):
	return float(x) / 100

def read_Bovespa(File,data):
	
	deli = [2, 8, 2, 12, 3, 12, 10, 3, 4, 13, 13, 13, 13, 13, 13, 13, 5, 18, 18, 13, 1, 8, 7, 13, 11, 4]
	
	df = pd.read_fwf(File, 
	                 widths=deli, 
					 header=None,
					 encoding='latin1', 
					 converters={9: convert_to_decimals,
								10: convert_to_decimals,
								11: convert_to_decimals,
								12: convert_to_decimals,
								13: convert_to_decimals,
								14: convert_to_decimals,
								15: convert_to_decimals,
								18: convert_to_decimals,
								19: convert_to_decimals,
								})

	df = df.rename(columns={0: 'tipreg', 1: 'data', 2: 'codbdi', 3: 'codneg', 4: 'tpmerc', 5: 'nomres'
		, 6: 'especi', 7: 'prazot', 8: 'modref', 9: 'preabe', 10: 'premax', 11: 'premin', 12: 'premed'
		, 13: 'preult', 14: 'preofc', 15: 'preofv', 16: 'totneg', 17: 'quatot', 18: 'voltot', 19: 'preexe'
		, 20: 'indopc', 21: 'datven', 22: 'fatcot', 23: 'ptoexe', 24: 'codisi', 25: 'dismes'
				})

	
	df = df.drop(df.index[[0, df.index.max()]])
	
	df['data'] = pd.to_datetime(df['data'])
	df['datven'] = pd.to_datetime(df['datven'])
	df['preabe'] = pd.to_numeric(df['preabe'])
	df['premax'] = pd.to_numeric(df['premax'])
	df['premin'] = pd.to_numeric(df['premin'])
	df['premed'] = pd.to_numeric(df['premed'])
	df['preult'] = pd.to_numeric(df['preult'])
	df['preofc'] = pd.to_numeric(df['preofc'])
	df['preofv'] = pd.to_numeric(df['preofv'])
	df['voltot'] = pd.to_numeric(df['voltot'])
	df['preexe'] = pd.to_numeric(df['preexe'])
	
	log.info(df.shape)

	return df


def load(dias):

	con = sqlite3.connect(bovespa_db)

	df = pd.read_sql('''
		select max(data) as data from bovespa_historico
	''',con=con)['data'][0]
	con.close()
	
	log.info(f'max date found {df}')

	data = datetime.datetime(1990,1,1)
	if df is not None:
		data = datetime.datetime.strptime(df.split()[0],'%Y-%m-%d')
	
	anos = f_periodo_v6('%Y',dias)
	anos.reverse()

	for ano in anos:

		if int(ano) < data.year:
			log.info(f'ano solicitado({ano}) é menor que o da base({data.year})')
			continue

		con = sqlite3.connect(bovespa_db)
		cur = con.cursor()

		log.info(ano)
	
		file = 'tmp/COTAHIST_A{}.TXT'.format(ano)
		historicos = read_Bovespa(file,data)

		if not historicos[historicos['data'] > data].empty:
			historicos = historicos[historicos['data'] > data]
		
		list_historico = []
		for historico in historicos[historicos['data'] > data].values:
			v = ( str(historico[0])
				, str(historico[1])
				, str(historico[2])
				, str(historico[3])
				, str(historico[4])
				, str(historico[5])
				, str(historico[6])
				, str(historico[7])
				, str(historico[8])
				, historico[9]
				, historico[10]
				, historico[11]
				, historico[12]
				, historico[13]
				, historico[14]
				, historico[15]
				, historico[16]
				, historico[17]
				, historico[18]
				, historico[19]
				, historico[20]
				, str(historico[21])
				, historico[22]
				, str(historico[23])
				, historico[24]
				, historico[25])

			list_historico.append(v)
		
		del historicos

		cur.executemany('''
		insert into bovespa_historico({COLUMNS}) values ({VALUES})
		'''.format(COLUMNS=','.join(columns),VALUES=','.join(['?' for x in range(len(columns))])),list_historico)

		del list_historico

		con.commit()
		con.close()

if __name__ == '__main__':

	load(7500)		
