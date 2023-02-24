"""Initial

Revision ID: c0f532f7c0ce
Revises:
Create Date: 2023-02-24 00:44:05.516085

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "c0f532f7c0ce"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "player",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nickname"),
    )
    op.create_index(op.f("ix_player_rating"), "player", ["rating"], unique=False)
    op.create_table(
        "season",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("final_date", sa.Date(), nullable=True),
        sa.Column("winner", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["winner"], ["player.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_season_winner"), "season", ["winner"], unique=False)
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("season", sa.Integer(), nullable=True),
        sa.Column("series_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["season"], ["season.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_series_season"), "series", ["season"], unique=False)
    op.create_table(
        "game",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("series", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("winner_command", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["series"], ["series.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_game_series"), "game", ["series"], unique=False)
    op.create_table(
        "player_game",
        sa.Column("player_id", sa.UUID(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["player_id"], ["player.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("player_id", "game_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("player_game")
    op.drop_index(op.f("ix_game_series"), table_name="game")
    op.drop_table("game")
    op.drop_index(op.f("ix_series_season"), table_name="series")
    op.drop_table("series")
    op.drop_index(op.f("ix_season_winner"), table_name="season")
    op.drop_table("season")
    op.drop_index(op.f("ix_player_rating"), table_name="player")
    op.drop_table("player")
    # ### end Alembic commands ###
