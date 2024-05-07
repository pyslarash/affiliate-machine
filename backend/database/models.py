from . import db
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import DECIMAL

class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)  # Store the full JWT here
    jti = Column(String, unique=True, nullable=False)  # Store the JWT ID here, ensure it's unique
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)  # Tracks if the token is active

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_type = Column(String, nullable=False)

class Domain(db.Model):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="domains")
    domain_name = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

class DomainStats(db.Model):
    __tablename__ = 'domain_stats'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.id'))
    domain = relationship("Domain", back_populates="domain_stats")
    moz_da = Column(Integer)
    moz_pa = Column(Integer)
    ahrefs_dr = Column(Integer)
    ahrefs_eb = Column(Integer)
    ahrefs_rd = Column(Integer)
    ahrefs_dofollow = Column(Integer)
    ahrefs_ips = Column(Integer)
    semrush_rank = Column(Integer)
    semrush_keywords = Column(Integer)
    fb_comments = Column(Integer)
    fb_shares = Column(Integer)
    fb_reactions = Column(Integer)

class ProcessedDomain(db.Model):
    __tablename__ = 'processed_domains'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="processed_domains")
    domain_stats_id = Column(Integer, ForeignKey('domain_stats.id'))
    domain_stats = relationship("DomainStats", back_populates="processed_domains")
    website_name = Column(String)
    price_per_year = Column(DECIMAL(10, 2))
    date_bought = Column(DateTime)
    admin_link = Column(String)
    website_description = Column(String(255))
    tags = Column(String)
    group = Column(String)

class UserEnv(db.Model):
    __tablename__ = 'user_envs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="user_envs")
    name = Column(String, nullable=False)
    codename = Column(String, nullable=False)
    value = Column(String, nullable=False)

class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    processed_domain_id = Column(Integer, ForeignKey('processed_domains.id'))
    processed_domain = relationship("ProcessedDomain", back_populates="keywords")
    focus_keyword = Column(String, nullable=False)
    avg_monthly_searches = Column(Integer)
    keyword_difficulty = Column(Integer)
    high_cpc = Column(DECIMAL(10, 2))
    low_cpc = Column(DECIMAL(10, 2))

class KeywordStats(db.Model):
    __tablename__ = 'keyword_stats'
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'))
    keyword = relationship("Keyword", back_populates="keyword_stats")
    total_results = Column(Integer)
    min_word_count = Column(Integer)
    max_word_count = Column(Integer)
    min_num_paragraphs = Column(Integer)
    max_num_paragraphs = Column(Integer)
    min_num_h1_headers = Column(Integer)
    max_num_h1_headers = Column(Integer)
    min_num_h2_headers = Column(Integer)
    max_num_h2_headers = Column(Integer)
    min_num_h3_headers = Column(Integer)
    max_num_h3_headers = Column(Integer)
    min_num_h4_headers = Column(Integer)
    max_num_h4_headers = Column(Integer)
    min_num_h5_headers = Column(Integer)
    max_num_h5_headers = Column(Integer)
    min_num_h6_headers = Column(Integer)
    max_num_h6_headers = Column(Integer)
    min_total_headers = Column(Integer)
    max_total_headers = Column(Integer)
    min_num_images = Column(Integer)
    max_num_images = Column(Integer)
    min_num_links = Column(Integer)
    max_num_links = Column(Integer)
    min_num_internal_links = Column(Integer)
    max_num_internal_links = Column(Integer)
    min_num_external_links = Column(Integer)
    max_num_external_links = Column(Integer)

class Article(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'))
    keyword = relationship("Keyword", back_populates="articles")
    title = Column(String, nullable=False)
    html_text = Column(String, nullable=False)
    cover_image = Column(String)
    title_of_cover_image = Column(String)
    alt_of_cover_image = Column(String)
    meta_description = Column(String)

# Define relationships
User.domains = relationship("Domain", back_populates="user")
User.processed_domains = relationship("ProcessedDomain", back_populates="user")
User.user_envs = relationship("UserEnv", back_populates="user")
Domain.domain_stats = relationship("DomainStats", back_populates="domain")
DomainStats.processed_domains = relationship("ProcessedDomain", back_populates="domain_stats")
ProcessedDomain.keywords = relationship("Keyword", back_populates="processed_domain")
Keyword.keyword_stats = relationship("KeywordStats", back_populates="keyword")
Keyword.articles = relationship("Article", back_populates="keyword")
