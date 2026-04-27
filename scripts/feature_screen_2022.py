import pandas as pd
import numpy as np
from pathlib import Path

path = Path('/Users/salmaibrahim/EDWaitTime/data/ed2022_sas.sas7bdat')
df = pd.read_sas(path, format='sas7bdat', encoding='latin1')

df['WAITTIME'] = pd.to_numeric(df['WAITTIME'], errors='coerce')
df = df[df['WAITTIME'].between(0, 480)].copy()

sentinels = {-9, -8, -7, 7, 8, 9, 97, 98, 99, 997, 998, 999, 9997, 9998, 9999}
num_scores = []
cat_scores = []

for col in df.columns:
    if col == 'WAITTIME':
        continue

    s = df[col]
    if s.dtype == object:
        s = s.apply(lambda x: x.decode('latin1') if isinstance(x, (bytes, bytearray)) else x)

    s_num = pd.to_numeric(s, errors='coerce')

    if s_num.notna().sum() >= 500 and s_num.nunique(dropna=True) > 20:
        x = s_num.mask(s_num.isin(sentinels))
        mask = x.notna() & df['WAITTIME'].notna()
        if mask.sum() >= 500:
            corr = x[mask].corr(df.loc[mask, 'WAITTIME'], method='spearman')
            if pd.notna(corr):
                num_scores.append((col, abs(float(corr)), float(corr), int(mask.sum()), int(x.nunique(dropna=True))))
    else:
        x = s.astype('string').replace({
            '-9': pd.NA, '-8': pd.NA, '-7': pd.NA,
            '97': pd.NA, '98': pd.NA, '99': pd.NA,
            '998': pd.NA, '999': pd.NA,
        })
        tmp = pd.DataFrame({'x': x, 'y': df['WAITTIME']}).dropna()
        if len(tmp) < 500:
            continue
        vc = tmp['x'].value_counts()
        keep = vc[vc >= 100].index
        tmp = tmp[tmp['x'].isin(keep)]
        if tmp['x'].nunique() < 2:
            continue
        grand = tmp['y'].mean()
        grp = tmp.groupby('x')['y'].agg(['mean', 'count'])
        ss_between = ((grp['mean'] - grand) ** 2 * grp['count']).sum()
        ss_total = ((tmp['y'] - grand) ** 2).sum()
        if ss_total > 0:
            eta2 = float(ss_between / ss_total)
            cat_scores.append((col, eta2, int(len(tmp)), int(tmp['x'].nunique())))

num_top = pd.DataFrame(num_scores, columns=['feature', 'abs_spearman', 'spearman', 'n', 'n_unique']).sort_values('abs_spearman', ascending=False).head(20)
cat_top = pd.DataFrame(cat_scores, columns=['feature', 'eta2', 'n', 'n_levels']).sort_values('eta2', ascending=False).head(20)

current_features = {
    'ARRIVAL_HOUR', 'VMONTH', 'VDAYR', 'AGE', 'SEX', 'RACEUN', 'ETHUN', 'IMMEDR',
    'PAINSCALE', 'BPSYS', 'BPDIAS', 'TEMPF', 'PULSE', 'RESPR', 'POPCT',
}

if not num_top.empty:
    num_top['in_current_model'] = num_top['feature'].isin(current_features)
if not cat_top.empty:
    cat_top['in_current_model'] = cat_top['feature'].isin(current_features)

print('rows_after_wait_filter', len(df), 'cols', len(df.columns))
print('\nTOP NUMERIC (Spearman):')
print(num_top.to_string(index=False))
print('\nTOP CATEGORICAL (eta^2):')
print(cat_top.to_string(index=False))
