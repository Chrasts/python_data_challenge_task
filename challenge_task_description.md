# challange_task_description

## Context

This task works with a temporal data model storing share price history using two related tables:

- SHARE_PRICE – contains the current valid state  
- SHARE_PRICE_HIST – contains historical versions of records  

Together, these tables implement a temporal storage pattern where each record is valid for a specific time interval defined by FROM and TO timestamps.


## Source Tables – Data Lifecycle

### Insert Logic
New records are inserted with:
- FROM = current timestamp (time of insertion)
- TO = 9999-12-31 (open-ended validity)

### Update Logic
Updates are handled in two steps:

1. The current row is moved from SHARE_PRICE to SHARE_PRICE_HIST and its TO timestamp is set to the update time.  
2. A new version is written into SHARE_PRICE with updated values, a new FROM timestamp, updated SHARE_PRICE value, updated TS_FROM timestamp, and updated COMMENT.


## Target Table – OUTPUT

The OUTPUT table represents monthly share price change snapshots.

The table is conceptually updated once per month (first day of the month shortly after midnight).  
The process evaluates how much the share price changed during the previous month and stores this difference together with relevant metadata.

Rules:
- If the share price was not updated in source tables during the whole previous month, no OUTPUT record is generated.  
- If the difference between compared share prices equals zero, no OUTPUT record is generated.


## Task Objectives

### 1. OUTPUT Reconstruction Algorithm
Design a generally understandable algorithm that can recreate the OUTPUT table using only:
- SHARE_PRICE  
- SHARE_PRICE_HIST  

### 2. Current OUTPUT State Estimation
Determine how many rows would exist in OUTPUT today (if it still existed) based on the data available in SHARE_PRICE and SHARE_PRICE_HIST.

### 3. Trading Strategy Optimization Scenario
Assume:
- You currently have CHF 100,000  
- You have access to historical share prices  
- You can perform historical buy or sell operations  
- You are limited to 3 transactions  

Determine which transactions you would perform to maximize your wealth as of today.


## Evaluation Criteria

- Correctness and clarity of the reconstruction algorithm  
- Correctness of the resulting OUTPUT reconstruction result  
- Quality and critical evaluation of the trading strategy and assumptions
