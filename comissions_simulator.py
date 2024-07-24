import streamlit as st
import pandas as pd

# Define commission rates for different categories
commission_rates = {
    'Electronics': 0.05,
    'Clothing': 0.06,
    'Furniture': 0.07,
    'Toys': 0.04
}

# Function to calculate commission
def calculate_commission(sales, gm_percent, category):
    commission_rate = commission_rates.get(category, 0.05)
    bonus = 0
    
    # Example rule: Higher commission rate for sales above $10,000
    if sales > 10000:
        commission_rate += 0.02

    # Example rule: Additional bonus for GM% above 30%
    if gm_percent > 30:
        bonus = 500

    # Example rule: Minimum GM% to qualify for commission
    if gm_percent < 10:
        return 0.0

    gross_margin = sales * (gm_percent / 100)
    commission = gross_margin * commission_rate + bonus
    
    # Example rule: Cap commission at $5,000
    if commission > 5000:
        commission = 5000
    
    return commission

# Load or initialize the results table
def load_results():
    try:
        return pd.read_csv('commission_results.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Categoría','Venta','Margen (%)','Comisión'])

def save_result(sales, gm_percent, category, commission):
    new_row = pd.DataFrame({
        'Categoría': [category],        
        'Venta': [sales],
        'Margen (%)': [gm_percent],
        'Comisión': [commission]
    })
    results = load_results()
    results = pd.concat([results, new_row], ignore_index=True)
    results.to_csv('commission_results.csv', index=False)

# Clear the results table
def clear_results():
    results = pd.DataFrame(columns=['Categoría','Venta','Margen (%)','Comisión'])
    results.to_csv('commission_results.csv', index=False)

# Streamlit app UI
st.title('Simulador de Comisiones')

# User inputs for sales, GM%, and category
category = st.selectbox('Selecciona la categoria', options=list(commission_rates.keys()))
sales = st.number_input('Ingresa Venta estimada ($)', min_value=0.0, value=1000.0, step=100.0)
gm_percent = st.number_input('Ingresa el porcentaje de margen (%)', min_value=0.0, value=20.0, step=1.0)

# Calculate the commission
commission = calculate_commission(sales, gm_percent, category)

# Display the results
st.write(f'Categoría: {category}')
st.write(f'Venta: ${sales:.2f}')
st.write(f'Margen (%): {gm_percent:.2f}%')
st.write(f'Comisión estimada: ${commission:.2f}')

# Save the results when button is clicked
if st.button('Guardar calculo'):
    save_result(sales, gm_percent, category, commission)
    st.success('Calculo guardado!')
    results = load_results()  # Reload results after saving
    total_commissions = results['Comisión'].sum()
    st.metric("Total Comisiones", f"${total_commissions:.2f}")

# Clear the results when button is clicked
if st.button('Limpiar resultados'):
    clear_results()
    st.success('Resultados limpiados!')
    total_commissions = 0
    st.metric("Total Comisiones", f"${total_commissions:.2f}")

# Display the table of results
st.subheader('Comisiones estimadas')
results = load_results()
st.table(results)
