# ratbag-emu

Mouse emulation stack. Used as a test suite for libratbag.

### Usage

Dependencies
  - connexion
  - hid-tools
  - connexion[swagger-ui] (optional)

Dependencies for running the tests:
  - pytest
  - pytest-dependency

Run the server:
```
sudo python3 -m ratbag_emu
```

If you have `swagger-ui` installed, you will be able to access the `/ui` page on the server where you will be presented with the auto generated openapi web interface. There you can find curl commands to interface with the API.
