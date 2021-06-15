class BaseBacktesting(object): 
  ''' Base class for event-based backtesting of trading strategies.
  Attributes
  ==========
  symbol: str
      TR RIC (financial instrument) to be used. If the .csv file has the 
      Yahoo Finance format, the pricing element must be specified insted 
      (i.e. "Close").
  start: str
      start date for data selection
  end: str
      end date for data selection
  amount: float
      amount to be invested either once or per trade
  datapath: string
      path to the csv file to be imported
  ftc: float
      fixed transaction costs per trade (buy or sell). 
  ptc: float
      proportional transaction costs per trade (buy or sell)

  Methods
  =======
  get_data:
      retrieves and prepares the base data set
  plot_data:
      plots the closing price for the symbol
  get_date_price:
      returns the date and price for the given bar
  print_balance:
      prints out the current (cash) balance
  print_net_wealth:
      prints out the current net wealth
  place_buy_order:
      places a buy order
  place_sell_order:
      places a sell order
  close_out:
      closes out a long or short position
  '''
  def __init__(self, symbol, start, end, amount, datapath, 
               ftc=0.0, ptc=0.0, verbose=True):
    self.symbol = symbol
    self.start = start
    self.end = end
    self.initial_amount = amount
    self.amount = amount
    self.datapath = datapath
    self.ftc = ftc
    self.ptc = ptc
    self.units = 0
    self.position = 0
    self.trades = 0
    self.verbose = verbose
    self.net_wealth_serie = []
    self.get_data()

  def get_data(self):
    ''' Retrieves and prepares the data.
    '''
    raw = pd.read_csv(self.datapath, index_col=0, parse_dates=True).dropna()
    raw = pd.DataFrame(raw[self.symbol])
    raw = raw.loc[self.start:self.end]
    raw.rename(columns={self.symbol: 'price'}, inplace=True)
    raw['return'] = np.log(raw / raw.shift(1))
    self.data = raw.fillna(0)

  def plot_data(self, cols=None):
    ''' Plots the closing prices for symbol.
    '''
    if cols is None:
      cols = ['price']
    self.data['price'].plot(figsize=(10, 6), title=self.symbol)

  def get_date_price(self, bar):
    ''' Return date and price for bar.
    '''
    date = str(self.data.index[bar])[:10]
    price = self.data.price.iloc[bar]
    return date, price

  def print_balance(self, bar):
    ''' Print out current cash balance info.
    '''
    date, price = self.get_date_price(bar)
    print(f'{date} | current balance {self.amount:.2f}')

  def print_net_wealth(self, bar):
    ''' Print out current cash balance info.
    '''
    date, price = self.get_date_price(bar)
    net_wealth = self.units * price + self.amount
    print(f'{date} | current net wealth {net_wealth:.2f}')

  def get_net_wealth(self, bar):
    ''' Get current cash balance info.
    '''
    date, price = self.get_date_price(bar)
    return self.units * price + self.amount

  def place_buy_order(self, bar, units=None, amount=None):
    ''' Place a buy order.
    '''
    date, price = self.get_date_price(bar)
    if units is None:
      units = int(amount / price)
    self.amount -= (units * price) * (1 + self.ptc) + self.ftc
    self.units += units
    self.trades += 1
    if self.verbose:
      print(f'{date} | buying {units} units at {price:.2f}')
      self.print_balance(bar)
      self.print_net_wealth(bar)

  def place_sell_order(self, bar, units=None, amount=None):
    ''' Place a sell order.
    '''
    date, price = self.get_date_price(bar)
    if units is None:
      units = int(amount / price)
    self.amount += (units * price) * (1 - self.ptc) - self.ftc
    self.units -= units
    self.trades += 1
    if self.verbose:
      print(f'{date} | selling {units} units at {price:.2f}')
      self.print_balance(bar)
      self.print_net_wealth(bar)

  def close_out(self, bar):
    ''' Closing out a long or short position. To be used at the end of the 
    backtesting strategy, to translate the assets involved in the open 
    positions into liquidity.
        '''
    date, price = self.get_date_price(bar)
    self.amount += self.units * price
    self.units = 0
    self.trades += 1
    if self.verbose:
      print(f'{date} | inventory {self.units} units at {price:.2f}')
      print('=' * 55)
      print('Final balance [$] {:.2f}'.format(self.amount))
      perf = ((self.amount - self.initial_amount) /
      self.initial_amount * 100)
      print('Net Performance [%] {:.2f}'.format(perf))
      print('Trades Executed [#] {:.2f}'.format(self.trades))
      print('=' * 55)
     
 class BacktestLongShort(BaseBacktesting):

  def go_long(self, bar, units=None, amount=None):
      #Note that no alternative is presented for the case in which neither 
      #unit or amount is defined.
    if self.position == -1: #If the position is short, close it
      self.place_buy_order(bar, units=-self.units)
    #Open a new position
    if units:
      self.place_buy_order(bar, units=units)
    elif amount:
      if amount == 'all':
        amount = self.amount
      elif isinstance(amount, (float,int)):
        amount = self.amount*amount
      self.place_buy_order(bar, amount=amount)

  def go_short(self, bar, units=None, amount=None):
      #Note that no alternative is presented for the case in which neither 
      #unit or amount is defined.
    if self.position == 1: #If the position is long, close it
      self.place_sell_order(bar, units=self.units)
      #Open a new position
    if units:
      self.place_sell_order(bar, units=units)
    elif amount:
      if amount == 'all':
        amount = self.amount
      elif isinstance(amount, (float,int)):
        amount = self.amount*amount
      self.place_sell_order(bar, amount=amount)

  def run_by_matrix(self, signals:pd.Series, units_per_trade=None, amount_per_trade='all', min_signals=1, verbose=True, plot_result=True):
    ''' This method implements the strategy based on a matrix of signals
    for positioning short (-1) or long (1) on the market
    '''
    msg = f'\n\nRunning strategy based on a matrix of signals'
    msg += f'\nfixed costs {self.ftc} | '
    msg += f'proportional costs {self.ptc}'
    print(msg)
    self.net_wealth_serie = [] #Re-initialise the net_wealth_serie list
    self.verbose = verbose #Give the possibility to explicit verbosity
    self.position = 0 # initial neutral position
    self.trades = 0 # no trades yet
    self.amount = self.initial_amount # reset initial capital
    for bar in range(len(self.data)):
      if (sum([signals.iloc[bar]]) >= min_signals) and self.position != 1:
        self.go_long(bar, units=units_per_trade, amount=amount_per_trade)
        self.position = 1 # long position
      if (sum([signals.iloc[bar]]) <= -min_signals) and self.position != -1:
        self.go_short(bar, units=units_per_trade, amount=amount_per_trade)
        self.position = -1 # short position
      self.net_wealth_serie.append(self.get_net_wealth(bar))
    self.close_out(bar)
    if plot_result:
      self.plot_vector_strategy(signals)

  def plot_vector_strategy(self, unidim_matrix):
    ''' This function plots the strategy, with the entry long and short 
    points over the instrument price, and the net wealth value overlaid
    '''
    # Create figure with secondary y-axis
    fig_backt = make_subplots(specs=[[{"secondary_y": True}]])

    def set_buysell_marker(signal):
      #This function is conceived to be used by mapping
      # It returns a tuple of properties (color, symbol, size, opacity)
      if (signal==1):
        return ('green', 'triangle-up', 10, 1)
      elif (signal==-1):
        return ('red', 'triangle-down', 10, 1)
      else:
        return ('white', 'circle', 0, 0)
    prop_list=list(map(set_buysell_marker, unidim_matrix))
    marker_props=dict(color=[i[0] for i in prop_list],
                      symbol=[i[1] for i in prop_list],
                      size=[i[2] for i in prop_list],
                      opacity=[i[3] for i in prop_list])
    fig_backt.add_trace(go.Scatter(x=self.data.index, y=self.data.price,
                        mode='lines+markers',
                        name='S&P500 closing price',
                        line=dict(color='black'),
                        marker = marker_props))
    fig_backt.add_trace(go.Scatter(x=self.data.index, y=self.net_wealth_serie,
                        mode='lines',
                        fill='tozeroy',
                        name='Net wealth of the fund',
                        fillcolor='rgba(0, 0, 255, 0.15)',
                        line=dict(color='rgba(0, 0, 255, 0.2)')),
                        secondary_y=True,)
    fig_backt.update_layout(title='Backtesting of the trading strategy',
                      xaxis_title='Time',
                      yaxis_title='S&P500 closing price ($)',
                      )
    fig_backt.show()
