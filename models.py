from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Offer(Base):
    __tablename__ = 'offers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    casino_url = Column(String(1024), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    # Relationships
    clicks = relationship('Click', back_populates='offer')
    ftd_events = relationship('FTDEvent', back_populates='offer')
    weights = relationship('OfferWeight', back_populates='offer')
    
    def __repr__(self):
        return f"<Offer(id={self.id}, name='{self.name}')>"


class OfferWeight(Base):
    """Stores weights per (sub1, offer_id) combination"""
    __tablename__ = 'offer_weights'
    
    id = Column(Integer, primary_key=True)
    sub1 = Column(String(255), nullable=False, index=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), nullable=False)
    weight = Column(Float, default=1.0, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    offer = relationship('Offer', back_populates='weights')
    
    __table_args__ = (
        UniqueConstraint('sub1', 'offer_id', name='uix_sub1_offer'),
        Index('idx_sub1', 'sub1'),
    )
    
    def __repr__(self):
        return f"<OfferWeight(sub1='{self.sub1}', offer_id={self.offer_id}, weight={self.weight})>"


class Click(Base):
    __tablename__ = 'clicks'
    
    id = Column(Integer, primary_key=True)
    click_id = Column(String(64), unique=True, nullable=False, index=True)
    sub1 = Column(String(255), nullable=False, index=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_agent = Column(String(512))
    ip_address = Column(String(45))
    referrer = Column(String(1024))
    source = Column(String(255))
    campaign = Column(String(255))
    
    # Relationships
    offer = relationship('Offer', back_populates='clicks')
    ftd_event = relationship('FTDEvent', back_populates='click', uselist=False)
    
    __table_args__ = (
        Index('idx_sub1_offer_timestamp', 'sub1', 'offer_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<Click(id={self.id}, click_id='{self.click_id}', sub1='{self.sub1}', offer_id={self.offer_id})>"


class FTDEvent(Base):
    __tablename__ = 'ftd_events'
    
    id = Column(Integer, primary_key=True)
    click_id = Column(String(64), ForeignKey('clicks.click_id'), nullable=False, unique=True, index=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), nullable=False)
    ftd_timestamp = Column(DateTime, default=datetime.utcnow)
    external_player_id = Column(String(255))
    
    # Relationships
    click = relationship('Click', back_populates='ftd_event')
    offer = relationship('Offer', back_populates='ftd_events')
    payout = relationship('Payout', back_populates='ftd_event', uselist=False)
    
    def __repr__(self):
        return f"<FTDEvent(id={self.id}, click_id='{self.click_id}')>"


class Payout(Base):
    __tablename__ = 'payouts'
    
    id = Column(Integer, primary_key=True)
    ftd_event_id = Column(Integer, ForeignKey('ftd_events.id'), nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ftd_event = relationship('FTDEvent', back_populates='payout')
    
    def __repr__(self):
        return f"<Payout(id={self.id}, amount={self.amount})>"


def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(engine)
    print("✓ Database tables created successfully")


def get_session():
    """Get a new database session"""
    return SessionLocal()
