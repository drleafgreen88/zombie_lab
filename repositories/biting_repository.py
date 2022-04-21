from db.run_sql import run_sql

from models.human import Human
from models.zombie import Zombie
from models.zombie_type import ZombieType
from models.biting import Biting

import repositories.zombie_repository as zombie_repository
import repositories.human_repository as human_repository

def save(biting):
    sql = "INSERT INTO bitings (zombie_id, human_id) VALUES (%s, %s) RETURNING id"
    values = [biting.zombie.id, biting.human.id]
    results = run_sql(sql, values)
    biting.id = results[0]['id']
    return biting

def select_all():
    bitings = []
    
    sql = "SELECT * FROM bitings"
    results = run_sql(sql)

    for row in results:
        zombie = zombie_repository.select(row['zombie_id'])
        human = human_repository.select(row['human_id'])
        biting = Biting(zombie, human, row['id'])
        bitings.append(biting)

    return bitings

def select(id):
    biting = None
    sql = "SELECT * FROM bitings WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)

    if result is not None:
        result = result[0]
        zombie = zombie_repository.select(result['zombie_id'])
        human = human_repository.select(result['human_id'])
        biting = Biting(zombie, human, result['id'])

    return biting

def delete(id):
    sql = "DELETE FROM bitings WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def delete_all():
    sql = "DELETE FROM bitings"
    run_sql(sql)

def update(biting):
    sql = "UPDATE bitings SET (zombie_id, human_id) VALUES (%s, %s) WHERE id = %s"
    values = [biting.zombie.id, biting.human.id]
    run_sql(sql, values)