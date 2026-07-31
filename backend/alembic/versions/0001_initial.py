"""initial schema"""
from alembic import op
import sqlalchemy as sa
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False, unique=True), sa.Column("full_name", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("projects", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("idea", sa.Text(), nullable=False), sa.Column("status", sa.String(50), nullable=False, server_default="draft"), sa.Column("generated_files", sa.JSON(), nullable=False, server_default="{}"), sa.Column("documentation", sa.Text(), nullable=False, server_default=""), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("agents", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id")), sa.Column("role", sa.String(100), nullable=False), sa.Column("prompt", sa.Text(), nullable=False), sa.Column("memory", sa.JSON(), nullable=False, server_default="{}"), sa.Column("output", sa.Text(), nullable=False, server_default=""), sa.Column("status", sa.String(50), nullable=False, server_default="pending"), sa.Column("position", sa.Integer(), nullable=False))
    op.create_table("executions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id")), sa.Column("status", sa.String(50), nullable=False, server_default="queued"), sa.Column("started_at", sa.DateTime()), sa.Column("completed_at", sa.DateTime()))
    op.create_table("logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id")), sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=True), sa.Column("message", sa.Text(), nullable=False), sa.Column("level", sa.String(20), nullable=False, server_default="info"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
def downgrade():
    op.drop_table("logs"); op.drop_table("executions"); op.drop_table("agents"); op.drop_table("projects"); op.drop_table("users")
