# lithium_ion_battery_degradation_models

## Degradationmodels

degradationmodels is a Python library for calculing the degradations the battery.

## Description

This code is part of a thesis work. With the objective of developing a Python library to evaluate the degradation of lithium-ion batteries, therefore, the battery degradation models that were used are from the following article, called "Modeling of Lithium-Ion Battery Degradation", by the authors Bolum Xu, Alexandre Oudalov, Andreas Ulbing, Göran Andersson and Daniel Kirschen.

### Cite Papers

[Article](https://ieeexplore.ieee.org/document/7488267/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install degradationmodels
```

## Usage

```python
import degradationmodels as degm

# returns 'stc'
degm.stc(e, kT, T, Tref)

# returns 'ssoc'   
degm.ssoc(e, kSigma, sigma, sigmaRef)

# returns 'st'     
degm.st(kt, t)

# returns 'sd'
degm.sd(kdelta1, delta, kdelta2, kdelta3)

# returns 'F_d1'
degm.F_d1(Sd, St, Ssoc, STc)
    
# returns 'f_dt'    
degm.f_dt(St, Ssoc, STc)
    
# returns 'L_cyc'
degm.L_cyc(AlphaSei, N, BetaSei, fd1, e)
   
# returns 'L_cal'
degm.L_cal(AlphaSei, e, t, BetaSei, f_dt)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU v3.0](https://choosealicense.com/licenses/gpl-3.0/)






