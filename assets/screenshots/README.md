# Screenshots Guide

Add screenshots here to make the main README more visual and appealing.

## Recommended Screenshots

### 1. Terminal Output (`terminal-output.png`)
**What to capture:**
- Run `python main.py` with a demo/live account
- Show the formatted portfolio output
- Include the export confirmation messages

**Tips:**
- Use a clean terminal with good contrast
- Resize terminal to ~120 columns for readability
- Include full output from start to finish

### 2. Yahoo Finance Import (`yahoo-import.png`)
**What to capture:**
- Yahoo Finance portfolio import page
- Show the "Upload from File" dialog
- Display the CSV being selected

**Steps:**
1. Go to Yahoo Finance → My Portfolio
2. Create New Portfolio or open existing
3. Click Import → Upload from File
4. Take screenshot showing file selection

### 3. Yahoo Finance Portfolio Dashboard (`yahoo-dashboard.png`)
**What to capture:**
- Final portfolio view in Yahoo Finance
- Show multiple positions imported
- Include chart/performance metrics

**Tips:**
- Show positions with proper tickers (VUSA.L, ADYEN.AS, etc.)
- Include performance chart if visible
- Highlight the imported positions

### 4. Exchange Mapping Example (`ticker-mapping.png`)
**What to capture:**
- Side-by-side comparison showing:
  - Trading212 ticker: VUSAl_EQ
  - CSV output: VUSA.L
  - Yahoo Finance: VUSA.L imported successfully

### 5. CLI Demo GIF (`demo.gif`) - Optional but Impressive!
**What to create:**
- Screen recording of complete workflow:
  1. Run `python main.py`
  2. Show output scrolling
  3. Navigate to data/YYYY-MM-DD/yahoo/
  4. Show the CSV file

**Tools:**
- [asciinema](https://asciinema.org/) for terminal recording
- [terminalizer](https://github.com/faressoft/terminalizer) for GIF export
- Keep it under 30 seconds

## File Naming Convention

Use kebab-case for all files:
- `terminal-output.png`
- `yahoo-import.png`
- `yahoo-dashboard.png`
- `ticker-mapping.png`
- `demo.gif`

## Image Specifications

- **Format**: PNG for screenshots, GIF for animations
- **Max width**: 1200px
- **Compression**: Use tools like TinyPNG to reduce file size
- **Quality**: High enough to read text clearly

## Privacy Considerations

Before adding screenshots:
- ✅ Use demo account data
- ✅ Blur/redact actual account balances if using real account
- ✅ Remove any personal identifiable information
- ✅ Use example tickers (NVDA, AAPL, etc.)

## Usage in README

Once added, uncomment the screenshot section in README.md:

```markdown
## 📸 Screenshots

### Export Process
![Terminal Output](assets/screenshots/terminal-output.png)

### Yahoo Finance Import
![Yahoo Import](assets/screenshots/yahoo-import.png)

### Final Result
![Portfolio Dashboard](assets/screenshots/yahoo-dashboard.png)
```
