"""Added jobs and job statuses

Revision ID: 9f9a6f0e5ac2
Revises: 
Create Date: 2024-06-08 16:32:10.293750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlalchemy_utils
from backend.models.jobs import JobStatusEnum
# revision identifiers, used by Alembic.
revision: str = '9f9a6f0e5ac2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jobstatus',
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(JobStatusEnum), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jobstatus')
    op.drop_table('job')
    # ### end Alembic commands ###
