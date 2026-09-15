"""Experimento revisado: MLP binária com todas as imagens únicas auditadas."""
from __future__ import annotations
import hashlib, json, os, random
from pathlib import Path
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL','2')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image, ImageOps
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

SEMENTE=42
RAIZ=Path(__file__).resolve().parents[2]
DADOS=RAIZ/'fase2/dados/visual_ampliado'
AUDITORIA=RAIZ/'fase2/auditoria/inventario_visual_ampliado.json'
RESULTADOS=RAIZ/'fase2/resultados/visual_ampliado'
TAMANHO=(96,56)

def sementes():
    random.seed(SEMENTE); np.random.seed(SEMENTE); tf.keras.utils.set_random_seed(SEMENTE)

def inventario():
    meta=json.loads(AUDITORIA.read_text())
    df=pd.DataFrame(meta['imagens'])
    if len(df)!=491 or df.hash_original.nunique()!=491:
        raise ValueError(f'Esperadas 491 imagens únicas; encontradas {len(df)}.')
    if not all((RAIZ/p).is_file() for p in df.arquivo):
        raise ValueError('Derivados ausentes; execute preparar_visual_ampliado.py.')
    return df

def pixels(df):
    dados=[]
    for p in df.arquivo:
        with Image.open(RAIZ/p) as im:
            cinza=ImageOps.autocontrast(ImageOps.grayscale(im))
            cinza.thumbnail(TAMANHO,Image.Resampling.LANCZOS)
            canvas=Image.new('L',TAMANHO,255)
            canvas.paste(cinza,((TAMANHO[0]-cinza.width)//2,(TAMANHO[1]-cinza.height)//2))
            dados.append((1-np.asarray(canvas,dtype=np.float32)/255).reshape(-1))
    return np.stack(dados)

def dividir(df,x):
    ids=np.arange(len(df)); estrato=df.classe_original
    dev,test=train_test_split(ids,test_size=.20,random_state=SEMENTE,stratify=estrato)
    train,val=train_test_split(dev,test_size=.20,random_state=SEMENTE,stratify=estrato.iloc[dev])
    conjuntos=[set(df.iloc[i].hash_original) for i in (train,val,test)]
    if any(conjuntos[i]&conjuntos[j] for i,j in ((0,1),(0,2),(1,2))): raise AssertionError('Vazamento por hash.')
    return train,val,test

def modelo(n):
    m=tf.keras.Sequential([tf.keras.Input((n,)),tf.keras.layers.Dense(64,activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4)),tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(.4),tf.keras.layers.Dense(16,activation='relu'),
        tf.keras.layers.Dropout(.2),tf.keras.layers.Dense(1,activation='sigmoid')],name='mlp_ecg_ampliada')
    m.compile(optimizer=tf.keras.optimizers.Adam(3e-4),loss='binary_crossentropy',metrics=['accuracy',tf.keras.metrics.AUC(name='auc')])
    return m

def executar():
    sementes(); df=inventario(); x=pixels(df); y=df.alvo.to_numpy(); train,val,test=dividir(df,x)
    classes=np.unique(y[train]); pesos=compute_class_weight(class_weight='balanced',classes=classes,y=y[train])
    m=modelo(x.shape[1]); hist=m.fit(x[train],y[train],validation_data=(x[val],y[val]),epochs=80,batch_size=16,
        class_weight={int(c):float(p) for c,p in zip(classes,pesos)},callbacks=[tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',patience=10,restore_best_weights=True)],verbose=0)
    pv=m.predict(x[val],verbose=0).reshape(-1)
    candidatos=np.linspace(.2,.8,61); scores=[balanced_accuracy_score(y[val],pv>=t) for t in candidatos]
    limiar=float(candidatos[int(np.argmax(scores))]); prob=m.predict(x[test],verbose=0).reshape(-1); pred=(prob>=limiar).astype(int)
    met=dict(n_total=len(df),n_treino=len(train),n_validacao=len(val),n_teste=len(test),limiar=limiar,
        epocas=len(hist.history['loss']),acuracia=float(accuracy_score(y[test],pred)),
        acuracia_balanceada=float(balanced_accuracy_score(y[test],pred)),
        precisao_anormal=float(precision_score(y[test],pred,zero_division=0)),
        recall_anormal=float(recall_score(y[test],pred,zero_division=0)),
        f1_anormal=float(f1_score(y[test],pred,zero_division=0)),roc_auc=float(roc_auc_score(y[test],prob)),
        matriz_confusao=confusion_matrix(y[test],pred,labels=[0,1]).tolist(),
        distribuicao={k:{'treino':int((df.iloc[train].classe_original==k).sum()),'validacao':int((df.iloc[val].classe_original==k).sum()),'teste':int((df.iloc[test].classe_original==k).sum())} for k in sorted(df.classe_original.unique())},
        limitacoes=['A fonte não oferece chave de paciente confirmada.','Hashes evitam duplicatas exatas, não exames do mesmo indivíduo.','Balanceamento por peso não representa prevalência clínica.'])
    RESULTADOS.mkdir(parents=True,exist_ok=True)
    (RESULTADOS/'metricas.json').write_text(json.dumps(met,ensure_ascii=False,indent=2))
    out=df.iloc[test][['arquivo','classe_original','alvo','hash_original']].copy();out['probabilidade_anormal']=prob;out['predicao']=pred;out.to_csv(RESULTADOS/'previsoes_teste.csv',index=False)
    m.save(RESULTADOS/'modelo_mlp_ecg_ampliada.keras')
    pd.DataFrame(hist.history).to_csv(RESULTADOS/'historico_treino.csv',index=False)
    fig,ax=plt.subplots();ax.imshow(np.array(met['matriz_confusao']),cmap='RdPu');ax.set(xticks=[0,1],yticks=[0,1],xticklabels=['Normal','Anormal'],yticklabels=['Normal','Anormal'],xlabel='Predição',ylabel='Real',title='MLP ampliada — matriz de confusão')
    for i in range(2):
        for j in range(2): ax.text(j,i,met['matriz_confusao'][i][j],ha='center',va='center')
    fig.tight_layout();fig.savefig(RESULTADOS/'matriz_confusao.png',dpi=160);plt.close(fig)
    print(json.dumps(met,ensure_ascii=False,indent=2));return met

if __name__=='__main__': executar()
