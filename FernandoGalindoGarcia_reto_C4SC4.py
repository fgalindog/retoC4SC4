# 0. Librerias, datos y configuracion de pagina
import streamlit as st
import pandas as pd
import altair as alt

# Datos
url = "https://raw.githubusercontent.com/fgalindog/retoC4SC4/main/Employee_data.csv"
df = pd.read_csv(url)
df['gender'] = df['gender'].astype(str).str.strip()

# Config
st.set_page_config(layout="wide")
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

# 1. Títulos y descripción del dashboard (mas control con markdown que con st.header o title)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('''## Reto Fernando Galindo C4SC4 :+1:
### Streamlit Dashboard
##### Análisis de la base de datos de empleados de la empresa Socialize your Knowledge''') # sth.subheader
st.divider()

# 2. Logo de la empresa
image_url = "https://github.com/fgalindog/retoC4SC4/blob/main/img/logo_.jpeg?raw=true"
st.sidebar.image(image_url, 
         caption='Social Knowledge', 
         use_container_width=False) 

# 3. Control para seleccionar género del empleado
st.sidebar.header('Filtros:')
genero = st.sidebar.radio(
    "Selección de género:",
    options = ['Femenino','Masculino','Todos'],
    index=None  # sin seleccion por defecto
)
with col2:
    if genero == 'Femenino':
        st.write('Genero seleccionado: Femenino')
    elif genero == 'Masculino':
        st.write('Genero seleccionado: Masculino')
    else:
        st.write('Genero seleccionado: Todos')


# 4. Seleccion de rango de puntaje de desempeno del empleado
calMin, calMax = st.sidebar.slider(
    'Seleccione un rango de calificaciones:',
    min_value=df['performance_score'].min(), 
    max_value=df['performance_score'].max(),
    value=(1,4),
    step=1)
with col2:
    st.write('Rango de calificacion seleccionado:', calMin, ' - ', calMax)


# 5. Seleccion de estado civil del empleado
civil = st.sidebar.selectbox(
        "Seleccione estado civil de los Empleados",
        df['marital_status'].unique(),
        index=None,
        placeholder="Estatus...",
        )
with col2:
    st.write('Estado civil:', civil)


# Resumen de indicadores
df2Filtro = df.copy()
if genero and genero != 'Todos': # condicion para unicamente M o F Filtro para genero
    df2Filtro = df2Filtro[df2Filtro['gender'] == genero[0]]  # 1a letra
if (calMin, calMax):  # filtro de score
    df2Filtro = df2Filtro[
        (df2Filtro['performance_score'] >= calMin) & 
        (df2Filtro['performance_score'] <= calMax)
    ]
if civil: #filtro estado civil
    df2Filtro = df2Filtro[df2Filtro['marital_status'] == civil]

with col3: # agregado
    #st.metric("Empleados:", len(df2Filtro)) # se obtiene cantidad de registros
    s = f"<p style='font-size:120px;'>{len(df2Filtro)}</p>"
    #st.text('empleados')
    st.markdown(s, unsafe_allow_html=True) 
    #st.title(len(df2Filtro))


# 6. Distribución de los puntajes de desempeño
col1, col2, col3 = st.columns(3)
with col1:
    desempenoFreq = alt.Chart(df).mark_bar().encode(
        alt.X('performance_score:N',
            title='Evaluacion de desempeno',
            axis=alt.Axis(labelAngle=0)),
        alt.Y('count():Q',title='Cantidad de empleados')).properties(
        title='Distribución de Puntajes de Desempeño'
    )
    st.altair_chart(desempenoFreq, use_container_width=True)


# 7. Promedio de horas trabajadas por el género del empleado
with col2:
    horasGenero = alt.Chart(df).mark_point(size=200,filled=True).encode(
        alt.X('gender:N',
            title='Género',
            axis=alt.Axis(labelAngle=0)),
        alt.Y('mean(average_work_hours):Q',
            title='Horas promedio trabajadas',
            scale=alt.Scale(zero=False)),
        color=alt.Color('gender:N',
                        legend=None,
                        scale=alt.Scale(
                            domain=['F', 'M'],  # ojo M contiene espacio, falta limpieza de la bdd
                            range=['#FF6B6B', "#27DD0F"]))).properties(
        title='Horas trabajadas promedio y Género'
    )
    st.altair_chart(horasGenero, use_container_width=True)


# 8. Edad de los empleados con respecto al salario
col1, col2 = st.columns(2)
with col1:
    edadSalario = alt.Chart(df).mark_circle().encode(
        alt.X('age:Q',
            title='Edad de empleado',
            axis=alt.Axis(labelAngle=0),
            scale=alt.Scale(zero=False)),
        alt.Y('salary:Q',title='Salario',scale=alt.Scale(zero=False))).properties(
        title='Distribución de Salarios por Edad de Empleado'
    )
    st.altair_chart(edadSalario, use_container_width=True)

# Grafico adiconal
with col2:
    edadSalario2 = alt.Chart(df).mark_line().encode(
        x=alt.X('age:Q',
                bin=alt.Bin(step=10), 
                title='Edad',
                scale=alt.Scale(zero=False)),
        y=alt.Y('mean(salary):Q', 
                title='Salario Promedio',
                scale=alt.Scale(zero=False))).properties(
        title='Media Salarial por Rangos de Edad'
    )
    st.altair_chart(edadSalario2, use_container_width=True)


# 9. Relación del promedio de horas trabajadas versus el puntaje de desempeño
with col3:
    line_chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(
        alt.X('performance_score:N',
              title='Grado de desempeño',
              axis=alt.Axis(labelAngle=0)),
        alt.Y('mean(average_work_hours):Q',
              title='Horas promedio trabajadas',
              scale=alt.Scale(zero=False)),        
    ).properties(
        title='Horas trabajadas promedio por Nivel de Rendimiento',
        width=500
    ).configure_point(
        size=200,
        filled=True
    )    
    st.altair_chart(line_chart, use_container_width=True)


# 10. Conclusión sobre el reporte
st.markdown("""
            <div style="
            border-left: 5px solid #4e73df;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);">
            <h4 style="color: #4e73df; margin-top: 0;">Análisis Final</h4>
            <p style="margin-bottom: 0;">
            Se analizaron 311 registros correspondientes a la base de datos de Recursos Humanos de la empresa Social Knowledge. De estos 176 son mujeres y 135 hombres. Se muestran las relaciones entre diversas variables, como horas trabajadas promedio, grado de desempeño, edad, género y salarios. En cuanto a rendimiento, casi 250 empleados se encuentran en una calificación de 3 (Fully completion), este rendimiento se ve afectado por la cantidad promedio de horas trabajdas, donde desempeños bajos (1 y 2) podrían corresponder a pocas o demasiadas horas. El género también es un diferenciador entre la cantidad de horas promedio, resultando en que las mujeres trabajan en promedio una semana extra al año con respecto a los hombres. Por último, para salarios entre 60,000 y 100,000, parece haber una relación positiva con la edad del trabajador; se recomiendan validar estas deducciones estadísticamente.
            </p>
            </div>""", unsafe_allow_html=True)