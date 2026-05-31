#Interface (o que você vai ver na tela)
import streamlit as st
import pandas as pd
from engine import run_rules
import rules

st.title('Risk Simulator 🚀')

data = pd.read_csv('data.csv')

rules_dict = {
    'High Value': rules.high_value,
    'Risky country': rules.risky_country
}

results = run_rules(data, rules_dict)

st.write(pd.DataFrame(results))