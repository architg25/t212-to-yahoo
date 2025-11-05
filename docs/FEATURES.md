# Features & Roadmap

## Current Features (v0.3)

### Account Data
- ✅ Fetch account cash/balance
- ✅ Fetch account info (currency, ID)
- ✅ Support for both demo and live environments
- ✅ Environment variable configuration
- ✅ JSON data export with timestamps
- ✅ Console output formatting with PnL indicators
- ✅ Basic error handling

### Portfolio Management
- ✅ Fetch all open positions
- ✅ Fetch specific position by ticker
- ✅ Search positions
- ✅ Calculate position value and PnL percentage
- ✅ Display formatted portfolio summary

### Instruments Metadata
- ✅ Fetch all tradable instruments (8000+ stocks/ETFs)
- ✅ Get instrument names and ISINs
- ✅ Smart caching (in-memory + daily disk cache)
- ✅ Automatic cleanup of old cache files
- ✅ Enriched portfolio display with company names

## Planned Features

### Phase 1: Extended Account Data (PARTIALLY COMPLETE)
- [x] Account metadata (currency, account ID)
- [ ] Account summary endpoint
- [ ] Historical balance tracking
- [ ] Balance change alerts

### Phase 2: Portfolio Management (COMPLETED)
- [x] List all positions
- [x] Get position details
- [x] Portfolio value calculation
- [x] Profit/loss analysis
- [ ] Portfolio performance metrics (charts, trends)

### Phase 3: Order Management
- [ ] View open orders
- [ ] View order history
- [ ] Place market orders
- [ ] Place limit orders
- [ ] Cancel orders
- [ ] Order status tracking

### Phase 4: Market Data
- [ ] Get instrument details
- [ ] Search instruments
- [ ] Real-time price quotes
- [ ] Historical price data
- [ ] Market hours information

### Phase 5: Reporting & Analytics
- [ ] Generate transaction reports
- [ ] Tax reporting data
- [ ] Performance analytics
- [ ] Export to CSV/Excel
- [ ] Custom date range filtering
- [ ] Dividend tracking

### Phase 6: Advanced Features
- [ ] Webhook support for real-time updates
- [ ] Rate limiting with retry logic
- [ ] Caching layer for frequently accessed data
- [ ] CLI interface with commands
- [ ] Configuration file support
- [ ] Multi-account support
- [ ] Data visualization (charts/graphs)
- [ ] Automated testing suite

### Phase 7: Integration
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] REST API wrapper
- [ ] Discord/Slack notifications
- [ ] Portfolio tracking dashboard
- [ ] Automated trading strategies

## Architecture Improvements

### Code Quality
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Type hints throughout
- [ ] Logging framework
- [ ] Configuration validation

### Documentation
- [ ] Add code documentation (docstrings)
- [ ] API usage examples
- [ ] Video tutorials
- [ ] Migration guides

### Security
- [ ] API key encryption at rest
- [ ] Secure credential storage
- [ ] Audit logging
- [ ] Permission validation

## Configuration Options

Future environment variables:
```
# Rate limiting
T212_MAX_REQUESTS_PER_MINUTE=60

# Retry behavior
T212_MAX_RETRIES=3
T212_RETRY_DELAY=1

# Output
T212_OUTPUT_FORMAT=json|csv|table
T212_DATA_DIR=./data

# Logging
T212_LOG_LEVEL=INFO
T212_LOG_FILE=./logs/t212.log
```

## Contributing

If you'd like to contribute to any of these features, please:
1. Check if there's an existing issue/discussion
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

## Version History

### v0.3 (Current)
- Instruments metadata integration
- Smart caching (in-memory + daily disk cache)
- Enriched portfolio display with company names and ISINs
- Automatic cache cleanup

### v0.2
- Portfolio management integration
- Fetch all positions
- Position-level PnL calculations
- Enhanced display formatting

### v0.1
- Initial release
- Basic account cash fetching
- Environment configuration
- JSON export

## Notes

Features are prioritized based on:
1. **User value**: Most common use cases first
2. **API availability**: What Trading212 API supports
3. **Complexity**: Balance quick wins with complex features
4. **Dependencies**: Build foundational features first

This roadmap is subject to change based on user feedback and API updates.
