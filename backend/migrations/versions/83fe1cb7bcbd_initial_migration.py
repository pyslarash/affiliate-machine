"""Initial migration

Revision ID: 83fe1cb7bcbd
Revises: 
Create Date: 2024-06-28 17:49:54.573292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83fe1cb7bcbd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('jti', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('user_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('domain_name', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('domain_name')
    )
    op.create_table('user_envs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('jan_ip', sa.String(), nullable=True),
    sa.Column('jan_port', sa.Integer(), nullable=True),
    sa.Column('jan_prefix', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=True),
    sa.Column('moz_da', sa.Integer(), nullable=True),
    sa.Column('moz_pa', sa.Integer(), nullable=True),
    sa.Column('ahrefs_dr', sa.Integer(), nullable=True),
    sa.Column('ahrefs_eb', sa.Integer(), nullable=True),
    sa.Column('ahrefs_rd', sa.Integer(), nullable=True),
    sa.Column('ahrefs_dofollow', sa.Integer(), nullable=True),
    sa.Column('ahrefs_ips', sa.Integer(), nullable=True),
    sa.Column('semrush_rank', sa.Integer(), nullable=True),
    sa.Column('semrush_keywords', sa.Integer(), nullable=True),
    sa.Column('fb_comments', sa.Integer(), nullable=True),
    sa.Column('fb_shares', sa.Integer(), nullable=True),
    sa.Column('fb_reactions', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('processed_domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('domain_stats_id', sa.Integer(), nullable=True),
    sa.Column('website_name', sa.String(), nullable=True),
    sa.Column('price_per_year', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('date_bought', sa.DateTime(), nullable=True),
    sa.Column('admin_link', sa.String(), nullable=True),
    sa.Column('website_description', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['domain_stats_id'], ['domain_stats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keywords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('processed_domain_id', sa.Integer(), nullable=True),
    sa.Column('focus_keyword', sa.String(), nullable=False),
    sa.Column('avg_monthly_searches', sa.Integer(), nullable=True),
    sa.Column('keyword_difficulty', sa.Integer(), nullable=True),
    sa.Column('high_cpc', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('low_cpc', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['processed_domain_id'], ['processed_domains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('html_text', sa.String(), nullable=False),
    sa.Column('cover_image', sa.String(), nullable=True),
    sa.Column('title_of_cover_image', sa.String(), nullable=True),
    sa.Column('alt_of_cover_image', sa.String(), nullable=True),
    sa.Column('meta_description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['keyword_id'], ['keywords.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keyword_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=True),
    sa.Column('total_results', sa.Integer(), nullable=True),
    sa.Column('min_word_count', sa.Integer(), nullable=True),
    sa.Column('max_word_count', sa.Integer(), nullable=True),
    sa.Column('min_num_paragraphs', sa.Integer(), nullable=True),
    sa.Column('max_num_paragraphs', sa.Integer(), nullable=True),
    sa.Column('min_num_h1_headers', sa.Integer(), nullable=True),
    sa.Column('max_num_h1_headers', sa.Integer(), nullable=True),
    sa.Column('min_num_h2_headers', sa.Integer(), nullable=True),
    sa.Column('max_num_h2_headers', sa.Integer(), nullable=True),
    sa.Column('min_num_h3_headers', sa.Integer(), nullable=True),
    sa.Column('max_num_h3_headers', sa.Integer(), nullable=True),
    sa.Column('min_num_h4_headers', sa.Integer(), nullable=True),
    sa.Column('max_num_h4_headers', sa.Integer(), nullable=True),
    sa.Column('min_num_h5_headers', sa.Integer(), nullable=True),
    sa.Column('max_num_h5_headers', sa.Integer(), nullable=True),
    sa.Column('min_num_h6_headers', sa.Integer(), nullable=True),
    sa.Column('max_num_h6_headers', sa.Integer(), nullable=True),
    sa.Column('min_total_headers', sa.Integer(), nullable=True),
    sa.Column('max_total_headers', sa.Integer(), nullable=True),
    sa.Column('min_num_images', sa.Integer(), nullable=True),
    sa.Column('max_num_images', sa.Integer(), nullable=True),
    sa.Column('min_num_links', sa.Integer(), nullable=True),
    sa.Column('max_num_links', sa.Integer(), nullable=True),
    sa.Column('min_num_internal_links', sa.Integer(), nullable=True),
    sa.Column('max_num_internal_links', sa.Integer(), nullable=True),
    sa.Column('min_num_external_links', sa.Integer(), nullable=True),
    sa.Column('max_num_external_links', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['keyword_id'], ['keywords.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('keyword_stats')
    op.drop_table('articles')
    op.drop_table('keywords')
    op.drop_table('processed_domains')
    op.drop_table('domain_stats')
    op.drop_table('user_envs')
    op.drop_table('domains')
    op.drop_table('users')
    op.drop_table('token_blacklist')
    # ### end Alembic commands ###