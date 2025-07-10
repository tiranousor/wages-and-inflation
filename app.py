import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Анализ зарплат и инфляции", layout="wide")
st.title("Анализ динамики зарплат и инфляции в России (2000–2016)")

salaries = pd.read_excel('salaries.xlsx')
inflation = pd.read_excel('infliation.xlsx')

with st.expander("📄 Посмотреть таблицу зарплат"):
    st.dataframe(salaries)

with st.expander("📄 Посмотреть таблицу инфляции"):
    st.dataframe(inflation)

selected = ['Образование', 'Операции с недвижимым имуществом, аренда и предоставление услуг', 'Рыболовство, рыбоводство']
st.markdown("### 📌 Выбранные отрасли для анализа:")
st.write("/ ".join(selected))
salaries_selected = salaries[salaries['вид деятельности'].isin(selected)]
# st.write(salaries_selected)
years = salaries.columns[1:].astype(int)


filter_inf = inflation.loc[:, ['Год','Всего']]
# st.dataframe(filter_inf)
inf_dict = dict(zip(filter_inf['Год'], filter_inf['Всего']))
cumulative_inf = {}
multiplier = 1.0
for year in sorted(inf_dict.keys()):
    multiplier *= (1 + inf_dict[year] / 100)
    cumulative_inf[year] = multiplier

salaries_real = salaries.copy()
for year in salaries.columns[1:]:
    coeff = cumulative_inf.get(year, 1)
    salaries_real[year] = salaries[year]/coeff
with st.expander("📄 Посмотреть таблицу реальной зарплатны(с учётом инфляции)"):
    st.dataframe(salaries_real)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Номинальные зарплаты (без учёта инфляции)")
    fig1, ax1 = plt.subplots(figsize=(5, 3.5))
    for i in selected:
        ax1.plot(years, salaries_selected[salaries_selected['вид деятельности'] == i].values[0][1:], label=i)
    ax1.set_title('Номинальные зарплаты')
    ax1.set_xlabel('Год')
    ax1.set_ylabel('₽')
    ax1.legend()
    ax1.grid()
    st.pyplot(fig1)

with col2:
    st.subheader("Реальные зарплаты (с учётом инфляции)")
    salaries_real_selected = salaries_real[salaries_real['вид деятельности'].isin(selected)]

    fig2, ax2 =plt.subplots(figsize=(5, 3.5))
    for i in selected:
        ax2.plot(years, salaries_real_selected[salaries_real_selected['вид деятельности'] == i].values[0][1:], label=i)
    ax2.set_title('Реальные зарплаты в ценах 2000 года')
    ax2.set_xlabel('Год')
    ax2.set_ylabel('₽')

    ax2.legend()
    ax2.grid()
    st.pyplot(fig2)


