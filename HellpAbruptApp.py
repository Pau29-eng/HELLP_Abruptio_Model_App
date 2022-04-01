###############################
# This program lets you       #
# - enter values in Streamlit #
# - get prediction            #  
###############################
import joblib 
import pandas as pd
import streamlit as st
import numpy as np
from scipy.stats import norm
from cmath import exp

# Load the model from the file
temp_joblib = joblib.load('modelHA.pkl')
#############  
# Main page #
#############                
st.title("Predicting the probability of developing HELLP or Abruptio placentae")
st.header('Exclusively used to predict the absence of risks')
st.write("""
Created by Paula Dominguez del Olmo
\nThis is a Streamlit web app created so users could explore the Support vector machine (SVM) model, which predicts the risk of developing HELLP syndrome or abruptio placentae at any point during the pregnancy 
as these are the most acute and harder to predict complications.
\nThe used data has been provided by the Hospital Universitario 12 de Octubre after conducting a single-centre, observational, retrospective cohort study
with 211 patients in singleton pregnancies diagnosed with early PE in which expectant management was at- tempted between January 2014 and December 2020.     
""")  
# AJUSTAMOS LOS VALORES MÍNIMOS Y MÁXIMOS

min_sflt1=1000
max_sflt1=85000

min_plgf=0.1
max_plgf=300.0

min_numFar=0
max_numFar=4

min_eg_eco=20.00
max_eg_eco=245.00

min_PFEecoincl=200
max_PFEecoincl=4000

min_IPAU=0.60
max_IPAU=6.90

min_tas=100.00
max_tas=200.00

min_tad=50.00
max_tad=140.00

min_IPACMeco1=0.55
max_IPACMeco1=2.90

min_IPAUti=0.05
max_IPAUti=6.00

min_IPAUtd=0.05
max_IPAUtd=6.00

min_abortos=0
max_abortos=6

min_edadMaterna=16.00
max_edadMaterna=50.00

# ENTER NUMERICAL DATA FOR PREDICTION
st.header('**Preeclampsia Episode Variables:**')
EGeco_incl_user = st.number_input('Gestational age at preeclampsia diagnosis (calculated in weeks):',
                                 min_value = min_eg_eco,
                                 max_value = max_eg_eco
                                ) 
sFlt1_user = st.number_input('Anti-angiogenic marker (sFlt-1) absolute value:',
                                 min_value = min_sflt1,
                                 max_value = max_sflt1
                                )                               
PlGF_user = st.number_input('Angiogenic marker (PlGF) absolute value:',
                                 min_value = min_plgf,
                                 max_value = max_plgf
                                )                                                                 
# usamos float porque cualquier valor introducido por el usuario es detectado como string 
# usamos int para convertirlo en numero sin decimales y que lo detecte en los distintos rangos
if (int(float(EGeco_incl_user))*7) in range(140, 146):
        PlGFMoM_user = float(PlGF_user)/220
elif (int(float(EGeco_incl_user))*7) in range(147, 153):
        PlGFMoM_user = float(PlGF_user)/240
elif (int(float(EGeco_incl_user))*7) in range(154, 160):
        PlGFMoM_user = float(PlGF_user)/275
elif (int(float(EGeco_incl_user))*7) in range(161, 167):
        PlGFMoM_user = float(PlGF_user)/300
elif (int(float(EGeco_incl_user))*7) in range(168, 274):
        PlGFMoM_user = float(PlGF_user)/420
elif (int(float(EGeco_incl_user))*7) in range(175, 181):
        PlGFMoM_user = float(PlGF_user)/460
elif (int(float(EGeco_incl_user))*7) in range(182, 188):
        PlGFMoM_user = float(PlGF_user)/475
elif (int(float(EGeco_incl_user))*7) in range(189, 216):
        PlGFMoM_user = float(PlGF_user)/480
elif (int(float(EGeco_incl_user))*7) in range(217, 223):
        PlGFMoM_user = float(PlGF_user)/470
elif (int(float(EGeco_incl_user))*7) in range(224, 230):
        PlGFMoM_user = float(PlGF_user)/430
elif (int(float(EGeco_incl_user))*7) in range(231, 237):
        PlGFMoM_user = float(PlGF_user)/370
elif (int(float(EGeco_incl_user))*7) in range(238, 244):
        PlGFMoM_user = float(PlGF_user)/330
elif (int(float(EGeco_incl_user))*7) in range(245, 251):
        PlGFMoM_user = float(PlGF_user)/280
elif (int(float(EGeco_incl_user))*7) in range(252, 258):
        PlGFMoM_user = float(PlGF_user)/240
elif (int(float(EGeco_incl_user))*7) in range(259, 265):
        PlGFMoM_user = float(PlGF_user)/215
elif (int(float(EGeco_incl_user))*7) in range(266, 272):
        PlGFMoM_user = float(PlGF_user)/205
elif (int(float(EGeco_incl_user))*7) in range(273, 279):
        PlGFMoM_user = float(PlGF_user)/190
elif (int(float(EGeco_incl_user))*7) in range(280, 287):
        PlGFMoM_user = float(PlGF_user)/165
 

TAS_incl_user = st.number_input('Systolic blood pressure at diagnosis:',
                                 min_value = min_tas,
                                 max_value = max_tas
                                ) 
TAD_incl_user = st.number_input('Diastolic blood pressure at diagnosis:',
                                 min_value = min_tad,
                                 max_value = max_tad
                                )                              
PFE_ecoincl_user = st.number_input('Estimated fetal weight on the inclusion ultrasound:',
                                 min_value = min_PFEecoincl,
                                 max_value = max_PFEecoincl
                                )
IPAUti_eco_incl = st.number_input('Pulsatility index of the left uterine artery:',
                                 min_value = min_IPAUti,
                                 max_value = max_IPAUti
                                )
IPAUtd_ecoIncl_user = st.number_input('Pulsatility index of the right uterine artery:',
                                 min_value = min_IPAUtd,
                                 max_value = max_IPAUtd
                                ) 

IPACM_eco1_user = st.number_input('Pulsatility index in the middle cerebral artery:',
                                 min_value = min_IPACMeco1,
                                 max_value = max_IPACMeco1
                                )

cerebFormula = (float(IPACM_eco1_user) - (-2.7317 + 0.3335 * (float(EGeco_incl_user)) - 0.0058 * (float(EGeco_incl_user)**2)))  / (-0.88005 + 0.08182 * (float(EGeco_incl_user)) - 0.00133 * (float(EGeco_incl_user)**2))
cerebPerc=norm.cdf(cerebFormula)
IPACMpeco1_user= round(float(cerebPerc)*100)
if IPACMpeco1_user>5:
        IPACMp5_eco1 =0
elif IPACMpeco1_user<5:
        IPACMp5_eco1 =1                                

IPAU_ecoincl_user = st.number_input('Pulsatility index in the umbilical artery:',
                                 min_value = min_IPAU,
                                 max_value = max_IPAU
                                ) 
umbiFormula=(float(IPAU_ecoincl_user)-(3.55219 - 0.13558 * (float(EGeco_incl_user)) + 0.00174 * (float(EGeco_incl_user)**2)))/0.299                                               
umbiPerc=norm.cdf(umbiFormula)
IPAU_perc= round(float(umbiPerc)*100)
if IPAU_perc<95:
        IPAUp95_eco1 =0
elif IPAU_perc>95:
        IPAUp95_eco1 =1 

NumFar_user = st.slider('Number of anti-hypertensive drugs:',
                                 min_value = min_numFar,
                                 max_value = max_numFar
                                )                                                                                                                                                                                                                                                                                                                        

sexorn_user = st.selectbox('Sex of the newborn:',
                              ('Male',
                               'Female')
                             )
               
if sexorn_user=='Male':
        sexo_rn_1 =1
elif sexorn_user=='Female':
        sexo_rn_1 =0 
CirStadio = st.selectbox('Fetal Growth Restriction (FGR) stage at PE diagnosis:',
                              ('No',
                               'Stage I',
                               'Stage II',
                               'Stage III', 
                               'Stage IV')
                             )
               
if CirStadio=='No':
        CIRestadio_4 =0
elif CirStadio=='Stage I':
        CIRestadio_4 =0
elif CirStadio=='Stage II':
        CIRestadio_4 =0
elif CirStadio=='Stage III':
        CIRestadio_4 =0
elif CirStadio=='Stage IV':
        CIRestadio_4 =1
  
st.write("""
    The different FGR stages are defined as:
    \nStage I: antegrade umbilical artery flow
    \nStage II: absent end-diastolic umbilical artery flow
    \nStage III: reversed umbilical artery flow or ductus venosus pulsatility index >95th centile
    \nStage IV: reversed a wave in ductus venosus, unprovoked decelerations
    """)         

# CALCULAMOS EL RATIO A PARTIR DE LOS VALORES DE SFLT-1 Y PIGF
ratio_user=(float(sFlt1_user)/float(PlGF_user))
TAM_incl_user=(float(TAS_incl_user)+float(TAD_incl_user)+float(TAD_incl_user))/3
IPmAUt_ecoincl_user=(float(IPAUtd_ecoIncl_user)+float(IPAUti_eco_incl))/2
mean_UtA_PI = exp(1.39-0.012*(float(EGeco_incl_user)*7)+(float(EGeco_incl_user)*7)**2*0.0000198)
IPmAUtMoMeco1_user=round(IPmAUt_ecoincl_user/mean_UtA_PI.real)
# NORMALIZANDO LOS VALORES INTRODUCIDOS POR EL USUARIO PARA QUE SE CORRESPONDAN CON LOS VALORES ENTRENADOS (VARIABLES DIAGNOSTICO)
ratio =(float(ratio_user))/(1975.73)
NumFar=(int(NumFar_user))/(4)
EG_eco_incl=(float(EGeco_incl_user)-20.86)/(242.43-20.86)
TAM_Incl=(float(TAM_incl_user)-83.00)/(140.00-83.00)
IPAUtd_eco_incl=(float(IPAUtd_ecoIncl_user)-0.09)/(4.19-0.09)
PFE_eco_incl=(float(PFE_ecoincl_user)-192)/(3459-192)
IPmAUtMoM_eco1=(IPmAUtMoMeco1_user-1)/(4)
IPACM_eco1=(float(IPACM_eco1_user)-0.63)/(2.70-0.63)
IPACMp_eco1=(int(IPACMpeco1_user))/(99)
IPAU_eco_incl=(float(IPAU_ecoincl_user)-0.65)/(6.83-0.65)
PlGFMoM =(float(PlGFMoM_user)-0.01)/(1.44-0.01)

# ENTER CATEGORICAL DATA FOR PREDICTION (aparecerán a la izquierda de la aplicación)
st.sidebar.header('**Pregestational or first trimester variables**:')
edadMaterna_user = st.sidebar.number_input('Age at pregnancy onset (variable calculated with respect to the date of the last menstrual period):',
                                 min_value = min_edadMaterna,
                                 max_value = max_edadMaterna
                                ) 
abortos_user = st.sidebar.slider('Number of previous abortions:',
                                 min_value = min_abortos,
                                 max_value = max_abortos
                                )
                               
concepcion_user = st.sidebar.selectbox('Conception method:',
                              ('Spontaneous',
                               'Artificial insemination',
                               'In vitro fertilization')
                             )
               
if concepcion_user=='Spontaneous':
        concepcion_0 =1
        concepcion_1 =0
        concepcion_2 =0
elif concepcion_user=='Artificial insemination':
        concepcion_0 =0
        concepcion_1 =1
        concepcion_2 =0
elif concepcion_user=='In vitro fertilization':
        concepcion_0 =0
        concepcion_1 =0
        concepcion_2 =1

pePrevia_user = st.sidebar.selectbox('Preeclampsia in previous gestation:',
                              ('No',
                               'Yes',
                               'Unknown')
                             )
               
if pePrevia_user=='No':
        PE_previa_2= 0
elif pePrevia_user=='Yes':
        PE_previa_2= 0
elif pePrevia_user=='Unknown':
        PE_previa_2= 1

htcronica_user = st.sidebar.selectbox('Chronic maternal hypertension:',
                              ('No',
                               'Yes')
                             )
               
if htcronica_user=='No':
        ht_cronica =0
elif htcronica_user=='Yes':
        ht_cronica =1

les_user = st.sidebar.selectbox('Maternal lupus:',
                              ('No',
                               'Yes')
                             )
               
if les_user=='No':
        LES =0
elif les_user=='Yes':
        LES =1

imc35 = st.sidebar.selectbox('Body Mass Index > 35 kg/m²:',
                              ('No',
                               'Yes')
                             )
               
if imc35=='No':
        IMCmayor35 =0
elif imc35=='Yes':
        IMCmayor35 =1

af_PE = st.sidebar.selectbox('PE family history:',
                              ('No',
                               'Yes, her mother',
                               'Yes, her sister',
                               'Yes, both the mother and the sister')
                             )
               
if af_PE=='No':
        af_pe_3 =0
elif af_PE=='Yes, her mother':
        af_pe_3 =0
elif af_PE=='Yes, her sister':
        af_pe_3 =0
elif af_PE=='Yes, both the mother and the sister':
        af_pe_3 =1

AAS = st.sidebar.selectbox('Aspirin intake:',
                              ('No',
                               'Yes, before 16 weeks',
                               'Yes, after 16 weeks')
                             )               
if AAS=='No':
        AAS_2 =0
elif AAS=='Yes, before 16 weeks':
        AAS_2 =0
elif AAS=='Yes, after 16 weeks':
        AAS_2 =1

heparina_user = st.sidebar.selectbox('Administration of low molecular weight heparin:',
                              ('No',
                               'Yes')
                             )
               
if heparina_user=='No':
        Heparina =0
elif heparina_user=='Yes':
        Heparina =1


# NORMALIZANDO LOS VALORES INTRODUCIDOS POR EL USUARIO PARA QUE SE CORRESPONDAN CON LOS VALORES ENTRENADOS (VARIABLES DIAGNOSTICO)
edad_materna =(float(edadMaterna_user)-17.62)/(47.56-17.62)
abortos=(int(abortos_user))/(3)

# when 'Predict' is clicked, make the prediction and store it 
if st.button('Get Your Prediction'): 
    
    X = pd.DataFrame({'EG_eco_incl':[EG_eco_incl],
                      'PFE_eco_incl':[PFE_eco_incl], 
                      'PE_previa_2':[PE_previa_2],
                      'IPACMp5_eco1':[IPACMp5_eco1],
                      'concepcion_2':[concepcion_2], 
                      'AAS_2':[AAS_2],
                      'TAM_Incl':[TAM_Incl],
                      'IPACM_eco1':[IPACM_eco1], 
                      'IMCmayor35':[IMCmayor35],
                      'CIRestadio_4':[CIRestadio_4], 
                      'af_pe_3':[af_pe_3],
                      'IPAUtd_eco_incl':[IPAUtd_eco_incl],
                      'LES':[LES],
                      'sexo_rn_1':[sexo_rn_1],
                      'concepcion_1':[concepcion_1],
                      'concepcion_0':[concepcion_0],
                      'IPAU_eco_incl':[IPAU_eco_incl],
                      'PlGFMoM':[PlGFMoM],
                      'ratio':[ratio],
                      'IPAUp95_eco1':[IPAUp95_eco1],
                      'abortos':[abortos],
                      'edad_materna':[edad_materna],
                      'NumFar':[NumFar],
                      'IPACMp_eco1':[IPACMp_eco1],
                      'Heparina':[Heparina],
                      'ht_cronica':[ht_cronica],
                      'IPmAUtMoM_eco1':[IPmAUtMoM_eco1]
                     })
               

    # Making predictions            
    prediction = temp_joblib.predict(X)
    prediction_proba = temp_joblib.predict_proba(X) 

    
    st.subheader('**Prediction Output**')
    st.write("""
    This is a binary classification model. Options are:
    \n0: The patient does not present either HELLP risk or Abruptio risk 
    \n1: The patient presents HELLP risk or Abruptio risk (or both)
    """)
    st.write(prediction)
    

