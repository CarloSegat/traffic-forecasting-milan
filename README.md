# Traffic prediction with Milan Dataset
This is a project on time-series forecasting in the context of the 
CELL module (cellular networks), EIT Digital CNI 2nd year.

## Data 
The data is not included with the repo.
The original files where tab separated.
The columns are: cell id, timestamp, country code, [5 traffic measurments: call, sms, internet]
It should have the following shape (some records as example):
```
1	1386198000000	0	0.10454969705714641				
1	1386198000000	39	0.1928905642458027	0.24766249074477537	0.0017873101054994376	0.052274848528573205	10.90482850078159
1	1386198000000	46					0.026137424264286602
1	1386198600000	39	0.22393664607858804	0.35757411811842005	0.029087774982685617	0.05343788914147278	10.318297799757286
1	1386199200000	39	0.19476337272360228	0.09271075363685531	0.026137424264286602		10.665478291071713
```