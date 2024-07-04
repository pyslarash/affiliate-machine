from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from . import db

# Users
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    user_type = Column(String, nullable=False)
    domains = relationship("UserDomains", back_populates="user")
    tokens = relationship("TokenBlacklist", back_populates="user")
    envs = relationship("UserEnv", back_populates="user")

class UserEnv(db.Model):
    __tablename__ = 'user_envs'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    user = relationship("User", back_populates="envs")
    jan_ip = Column(String)
    jan_port = Column(Integer)
    jan_prefix = Column(String)
    open_ai_api_key = Column(String)
    google_search_api_key = Column(String)
    google_cx = Column(String)
    myaddr_api_key = Column(String)
    porkbun_api_key = Column(String)
    porkbun_secret = Column(String)
    czds_login = Column(String)
    czds_password = Column(String)

class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    jti = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="tokens")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)

# Domains
class Domains(db.Model):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    domain = Column(String, unique=True, nullable=False)
    zone = Column(String, nullable=False)
    users = relationship("UserDomains", back_populates="domain", cascade='all, delete-orphan')
    available_domains = relationship("AvailableDomains", back_populates="domain", cascade='all, delete-orphan')
    unavailable_domains = relationship("UnavailableDomains", back_populates="domain", cascade='all, delete-orphan')

class UserDomains(db.Model):
    __tablename__ = 'user_domains'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    domain_id = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), unique=True)
    domain = relationship("Domains", back_populates="users", uselist=False)
    user = relationship("User", back_populates="domains")
    keywords = relationship("Keywords", back_populates="user_domain")
    
class AvailableDomains(db.Model):
    __tablename__ = 'available_domains'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), unique=True)
    domain = relationship("Domains", back_populates="available_domains", uselist=False)
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
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))

class UnavailableDomains(db.Model):
    __tablename__ = 'unavailable_domains'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), unique=True)
    domain = relationship("Domains", back_populates="unavailable_domains", uselist=False)
    creation_date = Column(String, nullable=False)
    creation_time = Column(String, nullable=False)
    expiration_date = Column(String, nullable=False)
    expiration_time = Column(String, nullable=False)
    name_servers = Column(String)
    updated_date = Column(String, nullable=False)
    updated_time = Column(String, nullable=False)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))

# Keywords
class Keywords(db.Model):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey('user_domains.id'), nullable=False)
    user_domain = relationship("UserDomains", back_populates="keywords")
    focus_keyword = Column(String, nullable=False, unique=True)
    avg_monthly_searches = Column(Integer)
    keyword_difficulty = Column(Integer)
    high_cpc = Column(DECIMAL(10, 2))
    low_cpc = Column(DECIMAL(10, 2))
    keyword_stats = relationship("KeywordStats", back_populates="keyword")
    articles = relationship("Articles", back_populates="keyword")

class KeywordStats(db.Model):
    __tablename__ = 'keyword_stats'
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id', ondelete='CASCADE'), nullable=False, unique=True)
    keyword = relationship("Keywords", back_populates="keyword_stats", cascade='all, delete-orphan')
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
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))

    # Define relationship with Keywords
    keyword = relationship("Keywords", back_populates="keyword_stats")

# Articles
class Articles(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), nullable=False)
    keyword = relationship("Keywords", back_populates="articles")
    title = Column(String, nullable=False)
    html_text = Column(String, nullable=False)
    cover_image = Column(String)
    title_of_cover_image = Column(String)
    alt_of_cover_image = Column(String)
    meta_description = Column(String)