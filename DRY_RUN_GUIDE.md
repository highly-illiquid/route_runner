# DRY RUN MODE - Safe Testing Guide

## Problem
You're worried about getting locked out of Infocon after requesting 20+ 2FA codes. Test scripts work, but `main.py` might fail differently.

## Solution: Dry Run Mode

Run `main.py` with `--dry-run` flag to test the COMPLETE flow without connecting to Infocon.

## Usage

```bash
# Dry run mode (SAFE - no Infocon connection)
python main.py --dry-run

# Or short form
python main.py -d

# Production mode (CONNECTS to Infocon)
python main.py
```

## What Dry Run Does

### ✅ WILL DO (Normal Operation):
- ✅ Scan `invoices/input` for PDFs
- ✅ Extract data using Gemini AI
- ✅ Create JSON files
- ✅ Move files to `staging`
- ✅ Process staged files
- ✅ Show what WOULD be uploaded

### ❌ WILL NOT DO (Skipped):
- ❌ Launch browser
- ❌ Connect to Infocon portal
- ❌ Trigger 2FA emails
- ❌ Submit any forms
- ❌ Risk account lockout

## Example Output

```
🔒 DRY RUN MODE ENABLED
   - Will process files normally
   - Will extract data with AI
   - Will NOT connect to Infocon
   - Will NOT trigger 2FA emails
   - Safe to test complete flow

======================================================================
Invoice Bot Starting: 2025-12-04 15:10:00
⚠️  DRY RUN MODE - Will NOT connect to Infocon portal ⚠️
======================================================================

--- Phase 1: Processing Staged Files ---
Found 1 staged files.

>>> Uploading Staged: invoice_20251204.json
  Processing BOL: BOL123456

[DRY RUN] Simulating upload for BOL: BOL123456
  [DRY RUN] Would launch browser...
  [DRY RUN] Would login to Infocon...
  [DRY RUN] Would handle 2FA...
  [DRY RUN] Would fill form with:
    - BOL: BOL123456
    - Date: 2025-12-04
    - Shipper: ABC Company
    - Items: 3 line items
  [DRY RUN] ✓ Upload simulated successfully

======================================================================
Run Complete
======================================================================
```

## Testing Strategy

### Step 1: Test with Dry Run
```bash
# Put a test PDF in invoices/input
cp test_invoice.pdf invoices/input/

# Run in dry-run mode
python main.py --dry-run
```

**Watch for**:
- File gets processed
- AI extraction works
- JSON created in staging
- Upload simulation shows correct data
- No browser launches
- No 2FA emails sent

### Step 2: Verify Output
Check that:
- `invoices/input` is empty (file moved)
- `invoices/staging` has JSON file
- JSON contains correct extracted data
- Dry run simulation shows expected BOL data

### Step 3: Production Run (When Ready)
```bash
# Only run this when you're confident!
python main.py
```

## Benefits

1. **Safe Testing**: Test the entire pipeline without risking lockout
2. **Real Data**: Uses actual AI extraction, file management, etc.
3. **Confidence**: See exactly what will be uploaded before doing it
4. **Debugging**: Identify issues in the flow before hitting production

## When to Use Each Mode

### Use Dry Run When:
- ✅ Testing after code changes
- ✅ Verifying AI extraction quality
- ✅ Checking file management logic
- ✅ Not sure if everything works
- ✅ Want to see what WOULD happen

### Use Production When:
- ✅ Dry run succeeded multiple times
- ✅ Confident in the extracted data
- ✅ Ready to actually upload to Infocon
- ✅ Have verified 2FA email logic separately

## Important Notes

- **Dry run uses the EXACT same code path** as production
- **Only the browser/portal connection is skipped**
- **All other logic (AI, files, validation) runs normally**
- **This is the safest way to test the complete flow**

---

**Bottom Line**: Always test with `--dry-run` first. Only use production mode when dry run succeeds and you're ready to actually upload.
