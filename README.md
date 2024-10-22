

# `pg_upgrade2o` Script Documentation

The `pg_upgrade2o` script is a flexible utility designed for managing PostgreSQL version upgrades with minimal manual intervention. It supports various upgrade modes (clone, copy, link) and can handle tasks such as promoting standby nodes, managing extensions, and conducting a full database analysis after upgrade using parallel vacuuming.

## Features

- **Multiple Upgrade Modes**: Supports `clone`, `copy`, and `link` methods for upgrading.
- **Extension Management**: Optionally drops specific extensions in the old version and recreates them in the new version.
- **Automated Timing Logs**: Captures the time taken for each major step, including vacuum operations, and logs a detailed summary.
- **Parallel Vacuuming**: Leverages multi-core systems by allowing a configurable number of parallel jobs during the vacuum operation.

## Usage

```bash
pg_upgrade2o [command] [options]
```

### Commands

- **check**: Checks the upgrade status without performing upgrade or timing operations.
- **clone**: Performs the upgrade by cloning data from the old version to the new version.
- **copy**: Performs the upgrade by copying data from the old version to the new version.
- **link**: Performs the upgrade by linking data from the old version to the new version.
- **help**: Displays the help menu.

### Options (Required for `clone`, `copy`, or `link` Commands)

- `--old-path PATH`: Path to the old PostgreSQL data directory.
- `--new-path PATH`: Path to the new PostgreSQL data directory.
- `--old-bin-path PATH`: Path to the old PostgreSQL binaries.
- `--new-bin-path PATH`: Path to the new PostgreSQL binaries.
- `--old-port PORT`: Port for the old PostgreSQL instance.
- `--new-port PORT`: Port for the new PostgreSQL instance.
- `--pguser USERNAME`: PostgreSQL user.
- `--pg-old-version VERSION`: Old PostgreSQL version number (e.g., 13).
- `--pg-new-version VERSION`: New PostgreSQL version number (e.g., 14).
- `--extensions EXT1,EXT2`: *(Optional)* Comma-separated list of extensions to drop before the upgrade and recreate after the upgrade.
- `--jobs JOBS`: *(Optional)* Number of parallel jobs for `vacuumdb` after the upgrade; defaults to the system's CPU core count.

### Examples

1. **Checking Upgrade Status**

   ```bash
   pg_upgrade2o check
   ```

2. **Performing a Clone Upgrade with Extension Management**

   ```bash
   pg_upgrade2o clone --old-path /var/lib/pgsql/old --new-path /var/lib/pgsql/new \
                           --old-bin-path /usr/pgsql-13/bin --new-bin-path /usr/pgsql-14/bin \
                           --old-port 5432 --new-port 5433 \
                           --pguser postgres --pg-old-version 13 --pg-new-version 14 \
                           --extensions hstore,pgcrypto --jobs 4
   ```

3. **Linking Data for Upgrade**

   ```bash
   pg_upgrade2o link --old-path /var/lib/pgsql/old --new-path /var/lib/pgsql/new \
                          --old-bin-path /usr/pgsql-13/bin --new-bin-path /usr/pgsql-14/bin \
                          --old-port 5432 --new-port 5433 \
                          --pguser postgres --pg-old-version 13 --pg-new-version 14
   ```

## Workflow Overview

### 1. **Help Menu Display**
   - If no command is specified or an invalid command is entered, the help menu is displayed, outlining the available commands and options.

### 2. **Command and Option Parsing**
   - The script processes the specified command (`check`, `clone`, `copy`, `link`, or `help`) and options. It verifies that required parameters for upgrade commands (`clone`, `copy`, `link`) are provided and assigns default values where applicable (e.g., setting `JOBS` to CPU core count if `--jobs` isn’t specified).

### 3. **Extension Handling**
   - If `--extensions` is provided, the script will drop specified extensions from the old PostgreSQL version before upgrading and recreate them in the new version.

### 4. **Upgrade Process (for `clone`, `copy`, or `link` Commands)**
   - When an upgrade command is selected (`clone`, `copy`, or `link`):
     - The script promotes the old version to primary if it is in recovery mode.
     - Executes `pg_upgrade` with the selected upgrade method.
     - Starts the new PostgreSQL version and runs a parallel `vacuumdb` with the specified or default job count to analyze the data.

### 5. **Timing Summary**
   - The script logs start and end times for each significant step in the upgrade process. For `clone`, `copy`, and `link` commands, it captures:
     - **Total Time**: Duration of the entire upgrade process.
     - **Time Before Vacuum Operation**: Time spent on initial upgrade tasks before `vacuumdb`.
     - **Vacuum Operation Time**: Duration of the `vacuumdb` command.
   - A detailed timing summary is saved to a log file (`pg_upgrade_summary.log`), providing insights into the upgrade’s performance.

### 6. **`check` Command**
   - The `check` command is intended for status verification and does not perform timing or upgrade operations. When `check` is run, the script skips timing calculations, and no entries are added to the timing log.

## Script Functions

- **`_pg_upgrade`**: Performs the PostgreSQL upgrade based on the selected mode (`clone`, `copy`, or `link`) and handles timing calculations if applicable.
- **Conditional Timing**: Timing operations are executed only for `clone`, `copy`, and `link` commands. If `check` is selected, the script bypasses timing functions.
- **Summary Log**: Outputs a summary of the total time taken, time before vacuuming, and vacuuming time to `pg_upgrade_summary.log` when applicable.

## Summary Log File

Upon completion, the script creates or updates the log file `pg_upgrade_summary.log` with timing details. This file contains:

- **Total Upgrade Time**: Total time for the upgrade process.
- **Pre-Vacuum Time**: Time spent on tasks before the vacuum operation.
- **Vacuum Time**: Duration of the vacuum operation.

Example log file entry:

```
******************************* SUMMARY REPORT ********************************
Total time for entire upgrade process: 15 minutes and 30 seconds
Time taken before vacuum operation: 12 minutes and 10 seconds
Time taken for vacuum operation: 3 minutes and 20 seconds
*******************************************************************************
```

## Important Notes

- **Prerequisites**: Ensure both old and new PostgreSQL binaries and data directories are correctly specified.
- **Parallel Vacuuming**: The `--jobs` option can be set to manage the level of parallelism for `vacuumdb` in systems with multiple CPU cores. If not specified, it defaults to the full core count.
- **Log File**: `pg_upgrade_summary.log` provides a summary of the time taken for each critical phase during an upgrade, offering a performance overview for clone, copy, and link operations.

This documentation covers the essential features and usage of the `pg_upgrade2o` script, making it easier to execute and monitor PostgreSQL upgrades efficiently.
