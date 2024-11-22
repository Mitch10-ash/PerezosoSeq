# -*- coding: utf-8 -*-
"""Untitled23.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1USSIS20g8rJMHAybrlrXmUNix-1HF86z
"""
import streamlit as st 
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import matplotlib.pyplot as plt
from collections import Counter
import plotly.graph_objs as go

st.set_page_config(page_title="SECUENCIA DE PEREZOSO DE TRES DEDOS BRADYPUS", layout="wide")

st.header("SECUENCIA DE PEREZOSO DE TRES DEDOS BRADYPUS")


st.write("")
"Informacion sobre la secuencia genetica del perezoso"
st.write("")

image_path = "C:/Users/admin/OneDrive/Documentos/A UNISON/3er SEMESTRE/Bioinformatica/Copia de semana10_examen.ipynb - Colab_files/Perezoso.jpg"  
st.image(image_path, caption="Perezoso de tres dedos", use_column_width=True)

fasta_file = "C:/Users/admin/OneDrive/Documentos/A UNISON/3er SEMESTRE/Bioinformatica/Copia de semana10_examen.ipynb - Colab_files\sequence (1) Sloth.fasta"
seqfile = next(SeqIO.parse(fasta_file, "fasta"))
seqadn = str(seqfile.seq)

# Información de la secuencia
st.markdown("### INFORMACION DE LA SECUENCIA")
st.write(f"**ID:** {seqfile.id}")
st.write(f"**Secuencia:** {repr(seqadn)}")
st.write(f"**Longitud:** {len(seqadn)}")

# Contenido de GC
st.markdown("### CONTENIDO DE GC")
gc_content = gc_fraction(seqadn) * 100
st.write(f"**GC %:** {gc_content:.2f}%")

# Composición de nucleótidos
st.markdown("### COMPOSICION DE NUCLEOTIDOS")
def nucleotides_composition(seq):
    nucleotides = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for n in nucleotides:
        nucleotides[n] = seq.count(n) / len(seq) * 100
    return nucleotides

nucleotide_composition = nucleotides_composition(seqadn)

st.write("**Composición de nucleótidos:**")
st.write(nucleotide_composition)

# Gráfico de composición de nucleótidos usando Plotly
labels = list(nucleotide_composition.keys())
sizes = list(nucleotide_composition.values())
colors = ['#ff7f7f', '#9b0000', '#dc143c', '#ff6347']  # Colores personalizados

# Crear gráfico de pastel con Plotly
fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker=dict(colors=colors))])
fig_pie.update_layout(title="Composición de Nucleótidos del ADN")
st.plotly_chart(fig_pie)

# Frecuencia de codones
st.markdown("### FRECUENCIA DE CODONES")
def get_codons(sequence):
    return [sequence[i:i+3] for i in range(0, len(sequence), 3) if len(sequence[i:i+3]) == 3]

codons = get_codons(seqadn)
codon_counts = Counter(codons)

# Preparar datos para la visualización 3D de codones
st.markdown("### VISUALIZACION 3D")
x, y, z, values, codon_info = [], [], [], [], []

for codon, count in codon_counts.items():
    x_index = 'ACGT'.index(codon[0])
    y_index = 'ACGT'.index(codon[1])
    z_index = 'ACGT'.index(codon[2])

    x.append(x_index)
    y.append(y_index)
    z.append(z_index)
    values.append(count)
    codon_info.append(f'Codón: {codon}, Frecuencia: {count}')

# Crear gráfico 3D con Plotly
trace_3d = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=12,
        color=values,
        colorscale='Viridis',
        colorbar=dict(title="Frecuencia de Codón"),
        opacity=0.8
    ),
    text=codon_info,
    hovertemplate=(
        '<b>%{text}</b><br>'
        'Coordenadas: (%{x}, %{y}, %{z})<br>'
        'Frecuencia: %{marker.color}<br>'
        '<extra></extra>'
    )
)

layout_3d = go.Layout(
    title='Dispersión 3D de Codones de ADN',
    scene=dict(
        xaxis=dict(title='Primer Nucleótido'),
        yaxis=dict(title='Segundo Nucleótido'),
        zaxis=dict(title='Tercer Nucleótido'),
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    width=600,  # Ancho de la figura
    height=600  # Alto de la figura
)

fig_3d = go.Figure(data=[trace_3d], layout=layout_3d)
st.plotly_chart(fig_3d)