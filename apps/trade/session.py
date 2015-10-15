
from errors import *
from views import *


class Session(object):
  def __init__(self, session_id, remote_ip=None, client_version=None):
    self.session_id     = session_id
    self.remote_ip      = remote_ip
    self.client_version = client_version

    self.user           = None
    self.is_broker      = False
    self.profile        = None
    self.broker         = None
    self.should_end     = False

  def set_user(self, user):
    if user is None:
      self.user = None
      self.is_broker = False
      self.profile = None
      self.should_end = False
      return

    if self.user:
      raise UserAlreadyLogged
    self.user = user

    self.is_broker = self.user.is_broker

    from models import Broker
    if self.is_broker:
      self.profile = Broker.get_broker( application.db_session,user.id)
    else:
      self.profile = user

    if user.broker_id is not None:
      self.broker = Broker.get_broker( application.db_session,user.broker.id)

  def process_message(self, msg):
    if  msg.type == '1': # TestRequest
      return processTestRequest(self, msg)

    elif msg.type == 'BE': # login

      reqId = msg.get('UserReqTyp')
      if reqId == '1':
        return processLogin(self, msg)

      if reqId == '3':
        return processChangePassword(self, msg)

    elif msg.type == 'D':  # New Order Single
      return processNewOrderSingle(self, msg)

    elif  msg.type == 'F' : # Cancel Order Request
      return processCancelOrderRequest(self, msg)

    elif msg.type == 'x': # Security List Request
      return processSecurityListRequest(self, msg)

    elif msg.type == 'U0': # signup
      return processSignup(self, msg)

    elif msg.type == 'U2': # Request for Balances
      return processRequestForBalances(self, msg)

    elif msg.type == 'U4': # Request for Open Orders
      return processRequestForOpenOrders(self, msg)

    elif msg.type == 'U6': # CryptoCoin Withdraw Request
      return processWithdrawRequest(self, msg)

    elif msg.type == 'U10': # Request password request
      return processRequestPasswordRequest(self, msg)

    elif msg.type == 'U12': # Password request
      return processPasswordRequest(self, msg)

    elif msg.type == 'U16':  #Enable Disable Two Factor Authentication
      return processEnableDisableTwoFactorAuth(self, msg)

    elif msg.type == 'U18': #Request Deposit
      return processRequestDeposit(self, msg)

    elif msg.type == 'U20': # Request Deposit Method List
      return processRequestDepositMethods(self, msg)

    elif msg.type == 'U48': # Request Deposit Method
      return processRequestDepositMethod(self, msg)

    elif msg.type == 'U24': # Withdraw Confirmation Request
      return processWithdrawConfirmationRequest(self, msg)

    elif msg.type == 'U26': # Withdraw List Request
      return processWithdrawListRequest(self, msg)

    elif msg.type == 'U28': # Request broker lists
      return processBrokerListRequest(self, msg)

    elif msg.type == 'U30': # Deposit List Request
      return  processDepositListRequest(self, msg)

    elif msg.type == 'U34': # Ledger List Request
      return  processLedgerListRequest(self, msg)

    elif msg.type == 'U36': # Ledger List Request
      return  processTradersRankRequest(self, msg)

    elif msg.type == 'U38': # Update User Profile
      return  processUpdateUserProfile(self, msg)

    elif msg.type == 'U42': # Request for Positions
      return  processRequestForPositions(self,msg)

    elif msg.type == 'U44':
      return processConfirmTrustedAddressRequest(self, msg)

    elif msg.type == 'B0':  # Deposit Payment Confirmation
      return processProcessDeposit(self, msg)

    elif msg.type == 'B2':  # Customer List Request
      return processCustomerListRequest(self, msg)

    elif msg.type == 'B4':  # Customer Detail Request
      return processCustomerDetailRequest(self, msg)

    elif msg.type == 'B6':  # Process Withdraw
      return processProcessWithdraw(self, msg)

    elif msg.type == 'B8':  # Verify Customer
      return  processVerifyCustomer(self, msg)

    elif msg.type == 'A0':  # Request Query in Database
      return processRequestDatabaseQuery(self, msg)
    raise InvalidMessageError()
