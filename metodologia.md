# 3.2 Métodos da Literatura

Para fundamentar as escolhas metodológicas deste estudo, foi analisada a
abordagem proposta por Arishi (2025), que desenvolveu um sistema automatizado
de detecção e classificação de resíduos domésticos em tempo real utilizando
deep learning.

#### 3.2.1 Arquitetura e Dataset

Arishi (2025) propôs uma solução baseada na arquitetura YOLOv8 (You Only
Look Once, versão 8), utilizando Darknet-53 como backbone estrutural - uma
rede neural convolucional profunda de 53 camadas otimizada para extração de
características e detecção de objetos. O autor foi além da arquitetura original,
integrando mecanismos de atenção no "neck" da rede (especificamente após
cada camada C2f) para aumentar a precisão na detecção de resíduos pequenos
e reduzir interferências do fundo da imagem.

Duas variações customizadas foram testadas:
- **YOLOv8-SE:** Integração do módulo Squeeze-and-Excitation (SE)
- **YOLOv8-CBAM:** Integração do Convolutional Block Attention Module (CBAM),
  que apresentou o melhor desempenho geral

O dataset construído para o estudo continha inicialmente **3.775 imagens**
distribuídas em **17 classes** de resíduos domésticos, organizadas em três
categorias principais:

**Resíduos Recicláveis (5 classes):** Lata, Garrafa de vidro, Papel,
Garrafa de plástico e Papelão.

**Resíduos Não Recicláveis (7 classes):** Fragmentos de plástico, Prato
de plástico, Copo de plástico, Lâmpada, Embalagem de comida, Canudo de
plástico e Tampa de plástico.

**Resíduos Perigosos (5 classes):** Garrafa de produto químico, Lata de
produto químico, Bateria, Balde de tinta e Medicamentos.

O dataset foi particionado aleatoriamente em **70% para treinamento, 20%
para teste e 10% para validação**, garantindo que a distribuição das
categorias em cada subconjunto refletisse a distribuição geral.

#### 3.2.2 Pré-processamento e Balanceamento de Classes

O pré-processamento das imagens foi realizado na plataforma Roboflow,
aplicando:
- Redimensionamento (Resizing)
- Normalização (Normalization)
- Redução de ruído (Noise Reduction)

Um desafio significativo do dataset original era o **desbalanceamento de
classes**, com variação de 168 a 315 imagens por classe. Para mitigar
esse problema, Arishi (2025) aplicou extensivas técnicas de **data
augmentation**:

- Rotação (Rotating)
- Espelhamento (Flipping)
- Desfoque (Blurring)
- Corte aleatório (Random Cropping)
- Escurecimento (Darkening)

Através da combinação dessas técnicas, o dataset foi expandido para **5.695
imagens**, garantindo que cada uma das 17 classes passasse a ter exatamente
**335 imagens**, eliminando completamente o desbalanceamento.

#### 3.2.3 Treinamento e Hiperparâmetros

O modelo foi treinado ao longo de **200 épocas** diretamente sobre o dataset
customizado. Embora o estudo não especifique explicitamente o uso de transfer
learning com pesos pré-treinados (como ImageNet ou COCO), a metodologia
descreveu um processo iterativo de refinamento do modelo, consistindo em
treinar, testar e, caso a acurácia desejada não fosse atingida, realizar
ajustes nos dados ou no modelo e retreiná-lo.

#### 3.2.4 Resultados e Comparação com Estado da Arte

O modelo final aprimorado (**YOLOv8-CBAM com data augmentation**) alcançou
resultados expressivos:

**Métricas agregadas (3 categorias principais):**
- **Acurácia:** 92,73%
- **Precision, Recall, F1-Score:** Superiores a 90%

**Métricas detalhadas (17 classes):**
- **Acurácia:** 89,85%
- **mAP (Mean Average Precision):** 89,5%

Este mAP de 89,5% representou um **aumento de 4,2%** em relação ao modelo
YOLOv8 original (85,3%), demonstrando a eficácia da integração de mecanismos
de atenção e data augmentation.

Arishi (2025) comparou o YOLOv8 com outras seis arquiteturas de deep learning:

| Modelo | mAP (%) | Categoria |
|--------|---------|-----------|
| **YOLOv8** | **85,3** | One-stage |
| YOLOv7 | 82,1 | One-stage |
| RetinaNet | 81,6 | One-stage |
| EfficientDet | 80,4 | One-stage |
| SSD | 78,2 | One-stage |
| Fast R-CNN | 77,3 | Two-stage |
| Mask R-CNN | 74,1 | Two-stage |

Os resultados demonstraram a **superioridade dos modelos de estágio único**
(one-stage) em relação aos modelos baseados em regiões (two-stage), que
apresentaram os piores desempenhos e dificuldades para operar em tempo real
devido às suas arquiteturas de múltiplos estágios.

#### 3.2.5 Desafios e Limitações Identificadas

O estudo identificou desafios importantes que são relevantes para este trabalho:

1. **Semelhança visual entre classes:** O modelo frequentemente confundiu
   itens visualmente parecidos, como fragmentos de plástico com copos e
   tampas de plástico. As classes com pior desempenho foram:
   - Fragmentos de plástico (mAP: 0,74)
   - Embalagem de comida (Precision: 0,80)
   - Lâmpada (confundida com tampa de plástico)

2. **Detecção de objetos pequenos:** Modelos de estágio único têm dificuldade
   inerente para detectar objetos pequenos em cenas complexas, motivando a
   adição dos mecanismos de atenção SE e CBAM.

3. **Escassez de dados de qualidade:** Datasets públicos amplamente usados
   (como TrashNet com apenas 6 categorias e TACO com anotações pouco
   confiáveis) foram considerados insuficientes, motivando a criação de um
   dataset customizado.

#### 3.2.6 Relevância para este Estudo

O trabalho de Arishi (2025) é particularmente relevante pois:

1. **Domínio similar:** Ambos focam em classificação de resíduos recicláveis
   e domésticos
2. **Técnicas comparáveis:** Data augmentation extensivo para balanceamento
   e prevenção de overfitting
3. **Métricas alinhadas:** Uso de mAP, Precision, Recall e F1-Score como
   métricas principais
4. **Benchmarks estabelecidos:** Fornece valores de referência para
   comparação de resultados

**Diferenças metodológicas deste trabalho em relação a Arishi (2025):**

1. **Dataset:** Este estudo utiliza o dataset público "Recyclable and
   Household Waste Classification" do Kaggle, enquanto Arishi construiu
   um dataset customizado com 17 classes específicas.

2. **Arquiteturas:** Enquanto Arishi focou em variações do YOLOv8 com
   mecanismos de atenção, este trabalho compara **múltiplas arquiteturas**
   de classificação baseadas em CNNs com transfer learning (ResNet50,
   EfficientNetB0, MobileNetV2), explorando também **ensemble de modelos**.

3. **Abordagem:** Arishi utilizou detecção de objetos (bounding boxes),
   enquanto este trabalho foca em **classificação de imagem completa**,
   assumindo uma imagem por resíduo.

4. **Transfer Learning:** Este estudo utiliza explicitamente pesos
   pré-treinados do ImageNet e estratégias de fine-tuning, aspecto não
   detalhado por Arishi.

A abordagem de Arishi (2025) demonstra a viabilidade e eficácia de deep
learning para classificação de resíduos, fornecendo benchmarks sólidos
e validando a importância de técnicas como data augmentation e balanceamento
de classes, que serão amplamente exploradas neste trabalho.

---

# **CITAÇÃO COMPLETA PARA REFERÊNCIAS**

```ARISHI, A. Real-Time Household Waste Detection and Classification for
Sustainable Recycling: A Deep Learning Approach. Sustainability, v. 17,
MDPI, 24 fev. 2025.
```
