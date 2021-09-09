from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, with_polymorphic, relationship
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select

#################
# DB Connection #
#################

engine = create_engine('sqlite:///game.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Battle:

    def __init__(self, hero, monster):
        self.hero = hero
        self.monster = monster

    def is_finished(self):
        finished = self.hero.health <= 0 or self.monster.health <= 0
        if finished:
            self.winner()
        return finished

    def winner(self):
        if self.hero.health > 0:
            self.hero.exp += self.monster.exp
            self.monster.health = self.monster.constant_hp
            print(f'{self.hero.name} won the battle')
            print(f'{self.hero.name} won {self.monster.exp} exp')
            if self.hero.exp >= 200 * self.hero.level:
                self.hero.level += 1
                print(f'LVL UP!!\n{self.hero.name} is lvl {self.hero.level}.')
        else:
            print(f'{self.monster.name} won the battle\n You died.')

    def execute_turn(self, attack):
        print('+----------------------------------------------------------------------------------+')
        print(f'|            {self.hero.name} attacks {self.monster.name} with {attack.ability_name}|')
        self.monster.health -= ((2 * self.hero.level / 5) * self.hero.atack * attack.damage / self.monster.defense)
        print(f'|            {self.monster.name} attacks {self.hero.name}|')
        self.hero.health -= ((2 * self.monster.difficulty / 5) * self.monster.atack * 4 / self.hero.defense)
        print('+----------------------------------------------------------------------------------+')
        print('\n')

    def current_status(self):
        monster_hp_lost = int(self.monster.constant_hp - self.monster.health)
        monster_current_hp = int(self.monster.constant_hp - monster_hp_lost)

        hero_hp_lost = int(self.hero.constant_hp - self.hero.health)
        hero_current_hp = int(self.hero.constant_hp - hero_hp_lost)

        print(self.hero.name + '\n|' + '■' * hero_current_hp + ' ' * hero_hp_lost + '|')
        print('\n')
        print(self.monster.name + '\n|' + '■' * monster_current_hp + ' ' * monster_hp_lost + '|')


##########
# Models #
##########

creature_attack = Table('creatureAttack',
                        Base.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('CreatureId', Integer, ForeignKey('creatures.id')),
                        Column('AttackId', Integer, ForeignKey('attacks.id')),
                        )


class Attack(Base):
    __tablename__ = 'attacks'

    id = Column(Integer(), primary_key=True)
    ability_name = Column(String(20), nullable=False, unique=True)
    damage = Column(Integer(), nullable=False)
    attack_level = Column(Integer(), nullable=False)


class Creature(Base):
    __tablename__ = 'creatures'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    health = Column(Integer(), nullable=False)
    constant_hp = Column(Integer, nullable=False)
    atack = Column(Integer(), nullable=False)
    defense = Column(Integer(), nullable=False)
    exp = Column(Integer(), nullable=False)
    gold = Column(Integer(), nullable=False)
    attacks = relationship('Attack', secondary=creature_attack)

    __mapper_args__ = {
        'polymorphic_identity': 'creatures',
    }


class Hero(Creature):
    __tablename__ = 'heroes'

    id = Column(Integer, ForeignKey('creatures.id'), primary_key=True)
    level = Column(Integer(), nullable=False)
    class_hero = Column(String(), nullable=False, unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'heroes',
    }


class Monster(Creature):
    __tablename__ = 'monsters'

    id = Column(Integer, ForeignKey('creatures.id'), primary_key=True)
    difficulty = Column(Integer(), nullable=False)
    sentence = Column(String(20))

    def talk(self):
        print(self.sentence)

    __mapper_args__ = {
        'polymorphic_identity': 'monster',
    }
