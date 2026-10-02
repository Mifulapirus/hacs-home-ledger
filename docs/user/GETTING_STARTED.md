# Getting Started with Home Ledger

Home Ledger tracks your household utility bills (electricity, gas, water, and flat `other` charges) and calculates totals, averages, and cost-per-unit — all stored locally in Home Assistant, in the currency Home Assistant is configured for.

## Prerequisites

- Home Assistant 2026.8.0 or newer
- HACS installed (recommended) or manual file copy

## Installation

### Via HACS (recommended)

1. Open HACS in Home Assistant
2. Search for "Home Ledger"
3. Click **Install**
4. Restart Home Assistant

### Manual

1. Copy `custom_components/home_ledger/` into your `config/custom_components/` directory
2. Restart Home Assistant

## Setup

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Home Ledger**
3. Click **Submit** — no credentials or configuration needed

A single config entry is created. All bills are stored locally under this entry.

## Add Your First Bill

You have two ways to add bills:

### Option A: Settings UI (recommended for first-time users)

1. Go to **Settings → Devices & services → Home Ledger**
2. Click **Options**
3. Fill in the form: utility type, start date, end date, total cost, consumption
4. Click **Submit**

### Option B: Service Action (recommended for automations)

Open **Developer Tools → Services** and call `home_ledger.add_bill`:

```yaml
service: home_ledger.add_bill
data:
  utility_type: electricity
  start_date: "2026-01-01"
  end_date: "2026-01-31"
  total_cost: 143.52
  consumption: 412.0
```

Or with a custom bill ID (useful for identifying bills):

```yaml
service: home_ledger.add_bill
data:
  bill_id: electricity_jan_feb_2026
  utility_type: electricity
  start_date: "2026-01-01"
  end_date: "2026-02-28"
  total_cost: 143.52
  consumption: 412.0
```

## What Gets Created

After adding bills, 16 sensor entities appear under the Home Ledger device:

| Category                        | Sensors                                                                                                                                |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Total cost**                  | `sensor.total_electricity_cost`, `sensor.total_gas_cost`, `sensor.total_water_cost`, `sensor.total_utility_cost`                       |
| **Total consumption**           | `sensor.total_electricity_consumption`, `sensor.total_gas_consumption`, `sensor.total_water_consumption`                               |
| **Average monthly cost**        | `sensor.electricity_average_monthly_cost`, `sensor.gas_average_monthly_cost`, `sensor.water_average_monthly_cost`                      |
| **Average monthly consumption** | `sensor.electricity_average_monthly_consumption`, `sensor.gas_average_monthly_consumption`, `sensor.water_average_monthly_consumption` |
| **Cost per unit**               | `sensor.electricity_cost_per_unit`, `sensor.gas_cost_per_unit`, `sensor.water_cost_per_unit`                                           |

## Your First Dashboard Card

Add a sensor card to your dashboard to track electricity costs over time:

```yaml
type: sensor
entity: sensor.total_electricity_cost
graph: line
name: Electricity Cost
```

## Next Steps

- [Configuration reference](CONFIGURATION.md) — service actions, entity details
- [Dashboard guide](DASHBOARDS.md) — standalone Lovelace dashboards, monthly tables, and charts
- [Automation examples](EXAMPLES.md) — alerts, reminders, and blueprints
