# ![hostasphere](https://avatars.githubusercontent.com/u/164780978?s=30 "logo") hand-e.fr

## Hostasphere - Profiler API

### Description
L'API de Profilage permet de mesurer le temps d'exécution, l'utilisation de la 
mémoire, et d'autres métriques autours d'OpenHosta pour les fonctions Python. 
Les données collectées sont envoyées sur votre interface de monitoring Hostasphere.

### Installation
Installez les dépendances requises avec pip :
```schell
pip install hostasphere-profiler==0.0.4
```

### Utilisation
#### Utilisation de base
Pour profiler une fonction, utilisez le décorateur `@profiler.probe()` :

```python
from profiler.core import Profiler

profiler = Profiler(
    endpoint_url='http://localhost:5000',
    license_id='1234',
    license_secret='567'
)

@profiler.probe()
def ma_fonction():
    # Logique de la fonction
    pass
```
