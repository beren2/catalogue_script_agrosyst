DROP TABLE IF EXISTS entrepot_levier_filiere CASCADE;
CREATE TABLE entrepot_levier_filiere AS
select
r.owner as levier_id,
r.sector as filiere
from refstrategylever_sector r;