# Home Ledger

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

Home Ledger is a Home Assistant custom integration for tracking household utility costs, consumption, photovoltaic investments and return on investment.

## Features

- **Utility Bill Tracking**: Track electricity, gas, and water bills, plus flat charges with no metered consumption
  (`other`), with full CRUD operations
- **Any Currency**: Cost sensors use the currency configured in Home Assistant
- **Persistent Storage**: All data is stored locally using Home Assistant's storage system
- **Smart Calculations**: Automatic calculation of totals, averages, and cost per unit
- **Service Actions**: Add, update, delete, and list bills via service calls
- **16 Sensor Entities**: Comprehensive sensors for costs, consumption, averages, and cost per unit
- **Simple Setup**: No credentials required - just install and start tracking

## Supported Utilities

| Utility     | Unit | Description                             |
| ----------- | ---- | --------------------------------------- |
| Electricity | kWh  | Track electricity consumption and costs |
| Gas         | m³   | Track gas consumption and costs         |
| Water       | m³   | Track water consumption and costs       |

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Search for "Home Ledger"
4. Click Download
5. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/home_ledger/` folder
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for "Home Ledger"
4. Follow the setup wizard

The integration requires no credentials or external connections - it stores all data locally.

## Usage

### Adding Bills via Service Actions

Use the `home_ledger.add_bill` service to add utility bills:

```yaml
service: home_ledger.add_bill
data:
  config_entry_id: "YOUR_CONFIG_ENTRY_ID"
  utility_type: "electricity"
  months: 2
  total_cost: 143.52
  consumption: 412.0
```

#### Parameters

| Parameter         | Required | Description                                     |
| ----------------- | -------- | ----------------------------------------------- |
| `config_entry_id` | Yes      | The Home Ledger config entry ID                 |
| `utility_type`    | Yes      | `electricity`, `gas`, `water`, or `other`       |
| `months`          | Yes      | Number of months covered (1, 2, 3, 6, 12, etc.) |
| `total_cost`      | Yes      | Total cost, in Home Assistant's currency        |
| `consumption`     | Yes      | Total consumption value                         |
| `bill_id`         | No       | Custom ID (auto-generated if omitted)           |

### Updating Bills

```yaml
service: home_ledger.update_bill
data:
  config_entry_id: "YOUR_CONFIG_ENTRY_ID"
  bill_id: "electricity_january"
  total_cost: 150.00
```

### Deleting Bills

```yaml
service: home_ledger.delete_bill
data:
  config_entry_id: "YOUR_CONFIG_ENTRY_ID"
  bill_id: "electricity_january"
```

### Listing Bills

```yaml
service: home_ledger.list_bills
data:
  config_entry_id: "YOUR_CONFIG_ENTRY_ID"
```

## Available Sensors

### Cost Sensors

"currency" is the currency set in Home Assistant under **Settings → System → General**, so a household billed in
USD sees USD. `other` is for flat charges with no metered consumption — waste collection, drainage, account and
late-payment fees — so they count toward the total without distorting water's or gas's cost per unit. Record them
with `consumption: 0`; `other` has no consumption or cost-per-unit sensors.

| Sensor                 | Unit     | Description                                |
| ---------------------- | -------- | ------------------------------------------ |
| Total electricity cost | currency | Sum of all electricity bills               |
| Total gas cost         | currency | Sum of all gas bills                       |
| Total water cost       | currency | Sum of all water bills                     |
| Total other charges    | currency | Sum of all `other` bills                   |
| Total utility cost     | currency | Sum of all utility costs, `other` included |

### Consumption Sensors

| Sensor                        | Unit | Description                        |
| ----------------------------- | ---- | ---------------------------------- |
| Total electricity consumption | kWh  | Sum of all electricity consumption |
| Total gas consumption         | m³   | Sum of all gas consumption         |
| Total water consumption       | m³   | Sum of all water consumption       |

### Average Monthly Sensors

| Sensor                                  | Unit     | Description                      |
| --------------------------------------- | -------- | -------------------------------- |
| Electricity average monthly cost        | currency | Total cost / total months        |
| Gas average monthly cost                | currency | Total cost / total months        |
| Water average monthly cost              | currency | Total cost / total months        |
| Other charges average monthly cost      | currency | Total cost / total months        |
| Electricity average monthly consumption | kWh      | Total consumption / total months |
| Gas average monthly consumption         | m³       | Total consumption / total months |
| Water average monthly consumption       | m³       | Total consumption / total months |

### Cost per Unit Sensors

A price per unit is not an amount of money, so these sensors carry no `monetary` device class.

| Sensor                    | Unit         | Description                    |
| ------------------------- | ------------ | ------------------------------ |
| Electricity cost per unit | currency/kWh | Total cost / total consumption |
| Gas cost per unit         | currency/m³  | Total cost / total consumption |
| Water cost per unit       | currency/m³  | Total cost / total consumption |

## Dashboard Example

```yaml
type: entities
entities:
  - entity: sensor.total_electricity_cost
  - entity: sensor.total_gas_cost
  - entity: sensor.total_water_cost
  - entity: sensor.total_utility_cost
  - type: divider
  - entity: sensor.total_electricity_consumption
  - entity: sensor.total_gas_consumption
  - entity: sensor.total_water_consumption
  - type: divider
  - entity: sensor.electricity_average_monthly_cost
  - entity: sensor.gas_average_monthly_cost
  - entity: sensor.water_average_monthly_cost
  - type: divider
  - entity: sensor.electricity_cost_per_unit
  - entity: sensor.gas_cost_per_unit
  - entity: sensor.water_cost_per_unit
```

## Important Notes

### Bill Periods

The `months` parameter is crucial for accurate calculations. Bills can cover different periods:

- 1 = monthly bill
- 2 = bimonthly bill
- 3 = quarterly bill
- 6 = semi-annual bill
- 12 = annual bill

The integration correctly calculates averages using total months, not just the number of bills.

### Example Calculation

```text
Bills:
- Electricity 2 months → €100
- Electricity 2 months → €120
- Electricity 1 month → €60

Total = €280
Total months = 5
Average monthly cost = €56
```

## Troubleshooting

### Enable Debug Logging

Add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.home_ledger: debug
```

## Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [@andmaroz89][user_profile]**

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/andmaroz89/hacs-home-ledger.svg?style=for-the-badge
[commits]: https://github.com/andmaroz89/hacs-home-ledger/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/andmaroz89/hacs-home-ledger.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40andmaroz89-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/andmaroz89/hacs-home-ledger.svg?style=for-the-badge
[releases]: https://github.com/andmaroz89/hacs-home-ledger/releases
[user_profile]: https://github.com/andmaroz89
