# v2.0.0

- Implemented a coordinator for Modbus requests, allowing all sensors to fetch data simultaneously. This ensures that values are synchronized and eliminates potential time mismatches, which could previously be up to 19 seconds.