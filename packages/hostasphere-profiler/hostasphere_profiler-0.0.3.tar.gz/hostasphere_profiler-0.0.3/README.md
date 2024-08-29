# ![hostasphere](https://avatars.githubusercontent.com/u/164780978?s=30 "logo") hand-e.fr

## Hostasphere - Profiler API

### Description
L'API de Profilage permet de mesurer le temps d'exécution, l'utilisation de la 
mémoire, et d'autres métriques autours d'OpenHosta pour les fonctions Python. 
Les données collectées sont envoyées sur votre interface de monitoring Hostasphere.

### Installation
Installez les dépendances requises avec pip :
```schell
pip install hostasphere-profiler==0.0.2
```

### Utilisation
#### Utilisation de base
Pour profiler une fonction, utilisez le décorateur `@probe()` :

```python
from profiler import probe

@probe()
def ma_fonction():
    # Logique de la fonction
    pass
```

### Configuration
#### Configuration File: `config.json`
The `config.json` file is used to configure the profiler application. 
It allows you to specify settings such as the endpoint URL where profiling data will be sent, 
and your license id and secret key for authentication.
This file is automatically created in the directory from which the application is launched,
if it does not already exist.

#### Structure
The config.json file is a JSON-formatted file containing key-value pairs for various configuration settings. Below is an example of its structure:
```json
{
    "endpoint_url": "http://your-default-endpoint-url.com/data",
    "license_id": "your-license-id",
    "license_secret": "your-license-secret"
}
```