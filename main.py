from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_excel("https://github.com/CottoneEnrico/Verifica-Pandas-Geopandas-Flask/blob/main/milano_housing_02_2_23.xlsx?raw=true")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/appartamenti', methods=['GET', 'POST'])
def appartamenti():
    if request.method == 'POST':
        quartiere = request.form['quartiere']
        df_quartiere = df[df['quartiere'] == quartiere].sort_values('data')
        return render_template('appartamenti.html', appartamenti=df_quartiere.to_html())
    else:
        return render_template('appartamenti.html')

@app.route('/quartieri')
def quartieri():
    quartieri = df['neighborhood'].sort_values().unique()

    return render_template('quartieri.html', quartieri=quartieri)

@app.route('/prezzo-medio-quartiere')
def prezzo_medio_quartiere():
    quartieri = df['neighborhood'].sort_values().unique()

    quartiere = request.args.get('quartiere')

    if quartiere:
        prezzo_medio = df[df['neighborhood'] == quartiere]['price'].mean()

        return render_template('prezzo-medio-quartiere.html', quartiere=quartiere, prezzo_medio=prezzo_medio)
    else:
        return render_template('prezzo-medio-quartiere.html', quartieri=quartieri)

@app.route('/prezzo-medio-quartieri')
def prezzo_medio_quartieri():
    prezzi_medi = df.groupby('neighborhood')['price'].mean().sort_values(ascending = False)

    tasso_conversione = request.args.get('tasso_conversione')

    def convertiValuta(prezzoInEuro, tasso_conversione):
        prezzo_altra_valuta = prezzoInEuro * tasso_conversione
        return prezzo_altra_valuta

    if tasso_conversione:
        prezzi_medi_altra_valuta = prezzi_medi.apply(lambda x: convertiValuta(x, float(tasso_conversione)))

        return render_template('prezzo-medio-quartieri.html', prezzi_medi=prezzi_medi_altra_valuta, tasso_conversione=tasso_conversione)
    else:
        return render_template('prezzo-medio-quartieri.html', prezzi_medi=prezzi_medi)

if __name__ == '__main__':
    app.run(debug=True)