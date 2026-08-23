# No dependencies: python3 ships sqlite3, and nothing here needs a network.

.PHONY: check check-sql check-links

check: check-sql check-links

# Run every SQL sample against the sample data the notes define, and diff the results.
check-sql:
	python3 scripts/check_sql.py

# Every relative link and #anchor resolves.
check-links:
	python3 scripts/check_links.py
