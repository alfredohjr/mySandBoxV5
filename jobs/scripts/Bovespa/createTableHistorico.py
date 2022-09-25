import sqlite3

from jobs.scripts.conf import bovespa_db

def run():
    con = sqlite3.connect(bovespa_db)
    cur = con.cursor()

    cur.execute(''' 
    CREATE TABLE "bovespa_historico" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                    "tipreg" varchar(2) NOT NULL, 
                                    "data" date NOT NULL, 
                                    "codbdi" varchar(2) NOT NULL, 
                                    "codneg" varchar(12) NOT NULL, 
                                    "tpmerc" varchar(3) NOT NULL, 
                                    "nomres" varchar(12) NOT NULL, 
                                    "especi" varchar(10) NOT NULL, 
                                    "prazot" varchar(3) NOT NULL, 
                                    "modref" varchar(4) NOT NULL, 
                                    "preabe" decimal NOT NULL, 
                                    "premax" decimal NOT NULL, 
                                    "premin" decimal NOT NULL, 
                                    "premed" decimal NOT NULL, 
                                    "preult" decimal NOT NULL, 
                                    "preofc" decimal NOT NULL, 
                                    "preofv" decimal NOT NULL, 
                                    "quatot" bigint NOT NULL, 
                                    "voltot" bigint NOT NULL, 
                                    "preexe" decimal NOT NULL, 
                                    "indopc" integer NOT NULL, 
                                    "datven" date NOT NULL, 
                                    "fatcot" integer NOT NULL, 
                                    "ptoexe" bigint NOT NULL, 
                                    "codisi" varchar(2) NOT NULL, 
                                    "dismes" bigint NOT NULL, 
                                    "totneg" integer NOT NULL)''')

    cur.execute('''CREATE UNIQUE INDEX ibovespahistorico001 ON bovespa_historico (id ASC, data DESC, codneg ASC)''')
    cur.execute('''CREATE INDEX bovespa_historico_data_IDX ON bovespa_historico ("data" DESC,codneg)''')
    cur.execute('''CREATE INDEX bovespa_historico_codneg_IDX ON bovespa_historico (codneg)''')

    con.commit()
    con.close()

if __name__ == '__main__':

    run()