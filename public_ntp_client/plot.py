
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

df = pd.read_csv('public.csv')
print(df)

df['Burst_Message'] = df.apply(lambda row: f"{row['Burst No.']}, {row[' Message Pair No.']}", axis=1)

theta_values = df[' theta(i)'].values
delta_values = df[' delta(i)'].values
oi = df[' o(i)'].values
di = df[' d(i)'].values

x = np.arange(len(df))

plt.figure(figsize=(14, 8))

plt.plot(x, theta_values, label='theta(i)', marker='o')
plt.plot(x, delta_values, label='delta(i)', marker='x')
plt.plot(x, oi, label='o(i)', marker='o')
plt.plot(x, di, label='d(i)', marker='x')


plt.xticks(x, df['Burst_Message'].values, rotation=45, ha="right")

plt.xlabel('Burst No., Message Pair No.')
plt.ylabel('Value')
plt.title('Theta(i) and Delta(i) for each Burst and Message Pair')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#plt.savefig('lan.png', dpi=300)
