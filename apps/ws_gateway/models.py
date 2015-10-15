# -*- coding: utf-8 -*-


from datetime import datetime, timedelta

from sqlalchemy import create_engine, func
from sqlalchemy.sql.expression import or_
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from tornado.options import options

ENGINE = create_engine(options.db_engine, echo=options.db_echo)
BASE = declarative_base()


class Trade(BASE):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    counter_order_id = Column(Integer, nullable=False)
    buyer_username = Column(String(15), nullable=False)
    seller_username = Column(String(15), nullable=False)
    side = Column(String(1), nullable=False)
    symbol = Column(String(12), nullable=False, index=True)
    size = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    trade_type = Column(Integer, nullable=False, default=0)  # regular trade

    def __repr__(self):
        return "<Trade(id=%r, order_id=%r, counter_order_id=%r, buyer_username=%r,seller_username=%r,  " \
               "side=%r, symbol=%r, size=%r, price=%r, created=%r, trade_type=%r )>"\
            % (self.id, self.order_id, self.counter_order_id, self.buyer_username, self.seller_username,
               self.side, self.symbol, self.size, self.price, self.created, self.trade_type)

    @staticmethod
    def get_trade(session, trade_id=None):
        if trade_id:
            filter_obj = or_(Trade.id == trade_id)
        else:
            return None
        trade = session.query(Trade).filter(filter_obj).first()
        if trade:
            return trade
        return None

    @staticmethod
    def get_all_trades(session):
      return session.query(Trade)

    @staticmethod
    def get_trades(session, symbol, since):

        trades = session.query(Trade).filter(
            Trade.id > since).filter(Trade.symbol == symbol).order_by(Trade.created.desc())

        return trades

    @staticmethod
    def get_last_trade_id():

        session = scoped_session(sessionmaker(bind=ENGINE))
        res = session.query(func.max(Trade.id)).one()

        return res[0]

    @staticmethod
    def get_last_trades(page_size = None, offset = None, sort_column = None, sort_order='ASC'):
        session = scoped_session(sessionmaker(bind=ENGINE))

        today = datetime.now()
        timestamp = today - timedelta(days=1)

        trades = session.query(Trade).filter(
            Trade.created >= timestamp).order_by(
            Trade.created.desc())

        if page_size:
            trades = trades.limit(page_size)
        if offset:
            trades = trades.offset(offset)
        if sort_column:
            if sort_order == 'ASC':
                trades = trades.order(sort_column)
            else:
                trades = trades.order(sort_column).desc()

        return trades

    @staticmethod
    def create(session, msg):
        trade = Trade.get_trade(session, msg['id'])
        if not trade:
            trade = Trade(id=msg['id'],
                          order_id=msg['order_id'],
                          counter_order_id=msg['counter_order_id'],
                          buyer_username=msg['buyer_username'],
                          seller_username=msg['seller_username'],
                          side=msg['side'],
                          symbol=msg['symbol'],
                          size=msg['size'],
                          price=msg['price'],
                          created=datetime.strptime(msg['trade_date'] + ' ' + msg['trade_time'], "%Y-%m-%d %H:%M:%S"))

            session.add(trade)
            session.commit()

        return trade

BASE.metadata.create_all(ENGINE)


def db_bootstrap(session):
    pass
