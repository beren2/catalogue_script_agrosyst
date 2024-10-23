### Organisation du config.ini

Pour le mode de fonctionnement local, donc avec les tables csv sur sa machine, modifier uniquement le data_path

#### metadata
- type=local
- data_path=C:/Users/x


### Pour le cas d'utilisation de type distant modifier ces connexions

#### entrepot_local : BDD de l'entrepot autre que local -> test
- host=localhost
- database=x
- user=x
- port=
- password=x

#### entrepot : BDD de l'entrepot autre que local
- host=x
- database=x
- user=x
- port=x
- password=x

#### datagrosyst : BDD opérationnelle de l'application Datagrosyst
- host=x
- database=x
- user=x
- port=x
- password=xx