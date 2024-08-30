from typing import List

from sqlalchemy import BigInteger, Column, DateTime, ForeignKeyConstraint, Identity, Integer, JSON, PrimaryKeyConstraint, Sequence, Table, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


class Funtionality(Base):
    __tablename__ = 'funtionality'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='funtion_pk'),
        UniqueConstraint('name', 'table', 'database',
                         'crud_type', name='funtionality_unique')
    )

    id = mapped_column(Integer, Sequence('id_funtionality_seq'))
    name = mapped_column(Text)
    status = mapped_column(Integer)
    table = mapped_column(Text)
    database = mapped_column(Text)
    crud_type = mapped_column(Text)

    permission: Mapped[List['Permission']] = relationship(
        'Permission', uselist=True, secondary='funtionality_need_permission', back_populates='funtionality')


class Permission(Base):
    __tablename__ = 'permission'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='permission_pk'),
    )

    id = mapped_column(Integer)
    name = mapped_column(Text)

    funtionality: Mapped[List['Funtionality']] = relationship(
        'Funtionality', uselist=True, secondary='funtionality_need_permission', back_populates='permission')
    role: Mapped[List['Role']] = relationship(
        'Role', uselist=True, secondary='role_has_permission', back_populates='permission')
    user: Mapped[List['User']] = relationship(
        'User', uselist=True, secondary='user_has_permission', back_populates='permission')


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='role_pk'),
    )

    id = mapped_column(Integer)
    name = mapped_column(Text)

    permission: Mapped[List['Permission']] = relationship(
        'Permission', uselist=True, secondary='role_has_permission', back_populates='role')


class Scope(Base):
    __tablename__ = 'scope'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='scope_pkey'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1,
                       minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name = mapped_column(Text, nullable=False)


t_funtionality_need_permission = Table(
    'funtionality_need_permission', metadata,
    Column('id_permission', Integer),
    Column('id_funtionality', Integer),
    ForeignKeyConstraint(['id_funtionality'], ['funtionality.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='funtionality_need_permission_funtionality_fk'),
    ForeignKeyConstraint(['id_permission'], ['permission.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='funtionality_need_permission_permission_fk'),
    UniqueConstraint('id_permission', 'id_funtionality',
                     name='funtionality_need_permission_unique')
)


t_role_has_permission = Table(
    'role_has_permission', metadata,
    Column('id_role', Integer),
    Column('id_permission', Integer),
    ForeignKeyConstraint(['id_permission'], ['permission.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='role_has_permission_permission_fk'),
    ForeignKeyConstraint(['id_role'], ['role.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='role_has_permission_role_fk'),
    UniqueConstraint('id_role', 'id_permission',
                     name='role_has_permission_unique')
)


t_role_has_scope = Table(
    'role_has_scope', metadata,
    Column('id_role', Integer, Identity(start=1, increment=1, minvalue=1,
           maxvalue=2147483647, cycle=False, cache=1), nullable=False),
    Column('id_scope', Integer, nullable=False),
    Column('value', Text),
    ForeignKeyConstraint(['id_role'], ['role.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='public_role_has_scope_id_role_fkey'),
    ForeignKeyConstraint(['id_scope'], ['scope.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='public_role_has_scope_id_scope_fkey')
)


class User(Role):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['role.id'], name='user_role_fk'),
        PrimaryKeyConstraint('id', name='user_pk')
    )

    id = mapped_column(Integer)
    status = mapped_column(Integer, nullable=False)
    username = mapped_column(Text)
    key = mapped_column(Text)
    email = mapped_column(Text)
    id_role = mapped_column(Integer)

    permission: Mapped[List['Permission']] = relationship(
        'Permission', uselist=True, secondary='user_has_permission', back_populates='user')
    audit_request: Mapped[List['AuditRequest']] = relationship(
        'AuditRequest', uselist=True, back_populates='user')
    audit_response: Mapped[List['AuditResponse']] = relationship(
        'AuditResponse', uselist=True, back_populates='user')


class AuditRequest(Base):
    __tablename__ = 'audit_request'
    __table_args__ = (
        ForeignKeyConstraint(['id_user'], ['user.id'],
                             name='audit_request_user_fk'),
        PrimaryKeyConstraint('id', name='audit_request_pk')
    )

    id = mapped_column(Integer)
    id_user = mapped_column(Integer, nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)
    ip = mapped_column(Text, nullable=False)
    url = mapped_column(Text, nullable=False)
    request = mapped_column(JSON)

    user: Mapped['User'] = relationship('User', back_populates='audit_request')


class AuditResponse(Base):
    __tablename__ = 'audit_response'
    __table_args__ = (
        ForeignKeyConstraint(['id_user'], ['user.id'],
                             name='audit_response_user_fk'),
        PrimaryKeyConstraint('id', name='audit_response_pk')
    )

    id = mapped_column(Integer)
    id_user = mapped_column(Integer, nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)
    id_request = mapped_column(Integer, nullable=False)
    response = mapped_column(JSON)

    user: Mapped['User'] = relationship(
        'User', back_populates='audit_response')


t_user_has_permission = Table(
    'user_has_permission', metadata,
    Column('id_user', Integer),
    Column('id_permission', Integer),
    ForeignKeyConstraint(['id_permission'], ['permission.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='user_has_permission_permission'),
    ForeignKeyConstraint(['id_user'], ['user.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='user_has_permission_user_fk'),
    UniqueConstraint('id_user', 'id_permission',
                     name='user_has_permission_unique')
)


t_user_has_scope = Table(
    'user_has_scope', metadata,
    Column('id_user', Integer, Identity(start=1, increment=1, minvalue=1,
           maxvalue=2147483647, cycle=False, cache=1), nullable=False),
    Column('id_scope', BigInteger, nullable=False),
    Column('value', Text),
    ForeignKeyConstraint(['id_scope'], ['scope.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='public_user_has_scope_id_scope_fkey'),
    ForeignKeyConstraint(['id_user'], ['user.id'], ondelete='CASCADE',
                         onupdate='CASCADE', name='public_user_has_scope_id_user_fkey')
)
