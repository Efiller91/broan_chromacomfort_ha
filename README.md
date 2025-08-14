# Broan ChromaComfort - Home Assistant Integration

Custom integration to control the Broan ChromaComfort Bluetooth-enabled bathroom fan/light.

## Installation

1. In Home Assistant, go to **HACS → Integrations → Custom repositories**.
2. Add `https://github.com/Efiller91/broan_chromacomfort_ha` as **Integration**.
3. Install and restart Home Assistant.
4. Go to **Settings → Devices & Services** and add the "Broan ChromaComfort" integration.

## Notes
- Requires Bluetooth on the Home Assistant host.
- Uses [Bleak](https://github.com/hbldh/bleak) for BLE communication.
