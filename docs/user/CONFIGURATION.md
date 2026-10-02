# Configuration Reference

Home Ledger has no configuration options. Bills are added via the Settings UI (options flow) or four service actions.

## Options Flow (Settings UI)

Go to **Settings → Devices & services → Home Ledger → Options** to add bills through a form.

| Field          | Type    | Required | Description                                          |
| -------------- | ------- | -------- | ---------------------------------------------------- |
| `utility_type` | select  | yes      | `electricity`, `gas`, `water`, or `other`            |
| `months`       | integer | yes      | Number of months the bill covers (≥ 1)               |
| `total_cost`   | float   | yes      | Total cost in Home Assistant's currency (≥ 0)        |
| `consumption`  | float   | yes      | Total consumption in the unit for that utility (≥ 0) |
| `bill_id`      | string  | no       | Custom ID. Auto-generated if omitted                 |

The options flow is add-only. To update or delete bills, use the service actions below.

## Service Actions

### `home_ledger.add_bill`

Create a new bill.

| Field             | Type   | Required | Description                                          |
| ----------------- | ------ | -------- | ---------------------------------------------------- |
| `config_entry_id` | string | yes      | The config entry ID (from Developer Tools → States)  |
| `utility_type`    | string | yes      | `electricity`, `gas`, `water`, or `other`            |
| `start_date`      | string | yes      | Start date in ISO format (YYYY-MM-DD)                |
| `end_date`        | string | yes      | End date in ISO format (YYYY-MM-DD)                  |
| `total_cost`      | float  | yes      | Total cost in Home Assistant's currency (≥ 0)        |
| `consumption`     | float  | yes      | Total consumption in the unit for that utility (≥ 0) |
| `bill_id`         | string | no       | Custom ID. Auto-generated if omitted                 |

**Unit of measurement by utility type:**

| Utility     | Unit |
| ----------- | ---- |
| electricity | kWh  |
| gas         | m³   |
| water       | m³   |

**Response:** returns the stored bill with its `id`.

```yaml
service: home_ledger.add_bill
data:
  config_entry_id: YOUR_ENTRY_ID
  utility_type: electricity
  start_date: "2026-01-01"
  end_date: "2026-01-31"
  total_cost: 143.52
  consumption: 412.0
```

### `home_ledger.update_bill`

Update an existing bill. Only the fields you provide are changed.

| Field             | Type   | Required | Description                 |
| ----------------- | ------ | -------- | --------------------------- |
| `config_entry_id` | string | yes      | The config entry ID         |
| `bill_id`         | string | yes      | The bill to update          |
| `utility_type`    | string | no       | New utility type            |
| `start_date`      | string | no       | New start date (YYYY-MM-DD) |
| `end_date`        | string | no       | New end date (YYYY-MM-DD)   |
| `total_cost`      | float  | no       | New total cost              |
| `consumption`     | float  | no       | New consumption             |

**Response:** returns the updated bill.

```yaml
service: home_ledger.update_bill
data:
  config_entry_id: YOUR_ENTRY_ID
  bill_id: electricity_jan_feb_2026
  total_cost: 155.00
```

### `home_ledger.delete_bill`

Remove a bill.

| Field             | Type   | Required | Description         |
| ----------------- | ------ | -------- | ------------------- |
| `config_entry_id` | string | yes      | The config entry ID |
| `bill_id`         | string | yes      | The bill to delete  |

**Response:** returns `{"bill_id": "..."}`.

```yaml
service: home_ledger.delete_bill
data:
  config_entry_id: YOUR_ENTRY_ID
  bill_id: electricity_jan_feb_2026
```

### `home_ledger.list_bills`

Return all stored bills.

| Field             | Type   | Required | Description         |
| ----------------- | ------ | -------- | ------------------- |
| `config_entry_id` | string | yes      | The config entry ID |

**Response:** returns `{"bills": [...]}`.

```yaml
service: home_ledger.list_bills
data:
  config_entry_id: YOUR_ENTRY_ID
```

## Bill Period

The `start_date` and `end_date` fields define the exact period covered by the bill.

This affects the **average monthly** calculations:

1. Total days are summed across all bills for a utility.
2. Daily average cost = Total Cost / Total Days.
3. Monthly average cost = Daily Average \* 30.44.

Example: A bill from 2026-01-01 to 2026-01-30 (30 days) with a cost of 300 EUR contributes a daily cost of 10 EUR, resulting in a monthly average of 304.40 EUR.

## Entity Categories

### Total Cost

Cumulative cost across all bills for each utility, plus a combined total. Updates instantly when bills change. Uses `state_class: total`.

### Total Consumption

Cumulative consumption across all bills. Updates instantly. Uses `state_class: total`.

### Average Monthly Cost

Total cost divided by total months across all bills of that utility. Returns `None` if no bills exist. No `state_class` (derived value).

### Average Monthly Consumption

Total consumption divided by total months. Returns `None` if no bills exist. No `state_class` (derived value).

### Cost Per Unit

Total cost divided by total consumption. Returns `None` if consumption is zero. Displays as EUR/kWh or EUR/m³. No `state_class` (derived value).

## Finding Your Config Entry ID

1. Go to **Developer Tools → States**
2. Search for `home_ledger`
3. The config entry ID is visible in the entity attributes, or use **Developer Tools → Actions** and select the `home_ledger` integration — the UI will show available entries.
