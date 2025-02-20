import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Przygotowanie danych
data = [
    (0, "Craniectomy", 2.163),
    (0, "Intact skull", 1.063),
    (0, "Intact skull", 2.238),
    (0, "Intact skull", 1),
    (0, "Craniotomy/large fractures", 1),
    (0, "Intact skull", 1),
    (0, "Craniectomy", 3),
    (0, "Craniotomy/large fractures", 1.167),
    (0, "Craniotomy/large fractures", 1.282),
    (0, "Craniectomy", 3),
    (0, "Craniectomy", 2.137),
    (0, "Craniotomy/large fractures", 2.75),
    (0, "Craniotomy/large fractures", 1),
    (0, "Intact skull", 2.072),
    (0, "Intact skull", 1.959),
    (0, "Craniectomy", 2.5),
    (0, "Craniectomy", 2.9),
    (0, "Craniotomy/large fractures", 3.209),
    (0, "Intact skull", 1.667),
    (0, "Craniotomy/large fractures", 1),
    (0, "Craniotomy/large fractures", 2.709),
    (0, "Craniotomy/large fractures", 2.039),
    (0, "Craniectomy", 3),
    (0, "Craniotomy/large fractures", 1),
    (1, "Craniotomy/large fractures", 3.878),
    (1, "Intact skull", 3),
    (1, "Intact skull", 2),
    (1, "Craniotomy/large fractures", 2.955),
    (1, "Craniectomy", 4),
    (1, "Intact skull", 1.5),
    (1, "Craniectomy", 3.307),
    (1, "Intact skull", 2.79),
    (1, "Intact skull", 3),
    (1, "Craniectomy", 3),
    (1, "Craniotomy/large fractures", 3.3),
    (1, "Craniectomy", 3.866),
    (1, "Intact skull", 2),
    (1, "Craniotomy/large fractures", 3.871),
    (1, "Craniectomy", 3.268),
    (1, "Intact skull", 1.8),
    (1, "Craniectomy", 3),
    (1, "Craniotomy/large fractures", 1),
    (1, "Intact skull", 2.226),
    (1, "Craniotomy/large fractures", 2.036),
    (1, "Craniotomy/large fractures", 3.909),
    (1, "Intact skull", 2.75),
    (1, "Intact skull", 2.118)
]

data = [
    (0, "Craniectomy", 2.072),
    (0, "Intact_skull", 1),
    (0, "Intact_skull", 2.818),
    (0, "Intact_skull", 1),
    (0, "Craniotomy_large_fractures", 1.462),
    (0, "Intact_skull", 1.077),
    (0, "Craniectomy", 3.882),
    (0, "Craniotomy_large_fractures", 1),
    (0, "Craniotomy_large_fractures", 1.513),
    (0, "Craniectomy", 3),
    (0, "Craniectomy", 1.75),
    (0, "Craniotomy_large_fractures", 3.111),
    (0, "Craniotomy_large_fractures", 1),
    (0, "Intact_skull", 3),
    (0, "Intact_skull", 2.944),
    (0, "Craniectomy", 3.167),
    (0, "Craniectomy", 3.834),
    (0, "Craniotomy_large_fractures", 2),
    (0, "Intact_skull", 2),
    (0, "Craniotomy_large_fractures", 1),
    (0, "Craniotomy_large_fractures", 2),
    (0, "Craniotomy_large_fractures", 1.898),
    (0, "Craniectomy", 3.944),
    (0, "Craniotomy_large_fractures", 2.737),
    (1, "Craniotomy_large_fractures", 3.667),
    (1, "Intact_skull", 2.304),
    (1, "Intact_skull", 1.5),
    (1, "Craniotomy_large_fractures", 3.871),
    (1, "Craniectomy", 4),
    (1, "Intact_skull", 2.248),
    (1, "Craniectomy", 3.467),
    (1, "Intact_skull", 1.888),
    (1, "Intact_skull", 3.607),
    (1, "Craniectomy", 4),
    (1, "Craniotomy_large_fractures", 3.923),
    (1, "Craniectomy", 3.5),
    (1, "Intact_skull", 2.147),
    (1, "Craniotomy_large_fractures", 2),
    (1, "Craniectomy", 3.271),
    (1, "Intact_skull", 1.877),
    (1, "Craniectomy", 4),
    (1, "Craniotomy_large_fractures", 2.154),
    (1, "Intact_skull", 1.66),
    (1, "Craniotomy_large_fractures", 4),
    (1, "Craniotomy_large_fractures", 4),
    (1, "Intact_skull", 2.681),
    (1, "Intact_skull", 1.25)
]

df = pd.DataFrame(data, columns=["age", "cranial_condition", "PSI_ICP"])

# Upewnij się, że zmienne kategoryczne są typu 'category'
df['age'] = df['age'].astype('category')
df['cranial_condition'] = df['cranial_condition'].astype('category')

# Definicja modelu - uwzględniamy główne efekty oraz interakcję
model = smf.ols('PSI_ICP ~ C(age) * C(cranial_condition)', data=df).fit()

# Przeprowadzenie analizy wariancji (ANOVA)
anova_table = sm.stats.anova_lm(model, typ=2)  # typ II, który często stosuje się w analizie factorial ANOVA
print(anova_table)
