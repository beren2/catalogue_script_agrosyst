### Organisation du config.ini

Pour le mode de fonctionnement local, donc avec les tables csv sur sa machine, une seule connection est nécessaire : metadata

#### metadata
```
[metadata]
type=local
data_path=C:/Users/x
```

### Pour le cas d'utilisation de type distant modifier ces connexions

#### Entrepot_local : BDD de l'entrepot autre que local -> test

```
[entrepot_local]
host=localhost
database=x
user=x
port=x
password=x
```

#### Entrepot : BDD de l'entrepot autre que local

```
[entrepot]
host=x
database=x
user=x
port=x
password=x
```

#### Datagrosyst : BDD opérationnelle de l'application Datagrosyst

```
[datagrosyst]
host=x
database=x
user=x
port=x
password=x
```