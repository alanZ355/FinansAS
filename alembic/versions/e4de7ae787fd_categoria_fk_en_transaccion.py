"""categoria_fk_en_transaccion

Revision ID: e4de7ae787fd
Revises: e511343dc65f
Create Date: 2026-06-11 15:47:05.845586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4de7ae787fd'
down_revision: Union[str, Sequence[str], None] = 'e511343dc65f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Paso 1 — nullable=True para no romper filas existentes
    op.add_column('transacciones',
        sa.Column('categoria_id', sa.Integer(), nullable=True)
    )
    
    # Paso 2 — foreign key con nombre explícito
    op.create_foreign_key(
        'fk_transacciones_categoria_id',
        'transacciones',
        'categorias',
        ['categoria_id'],
        ['id']
    )
    
    # Paso 3 — eliminar columna vieja
    op.drop_column('transacciones', 'categoria')


def downgrade() -> None:
    op.add_column('transacciones',
        sa.Column('categoria', sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.drop_constraint('fk_transacciones_categoria_id', 'transacciones', type_='foreignkey')
    op.drop_column('transacciones', 'categoria_id')
