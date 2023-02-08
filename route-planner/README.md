1. Install poetry [here](https://python-poetry.org/docs/).

2. Create a poetry environment

   ```
   poetry init
   ```

3. Initialise the poetry shell using
   ```
   poetry shell
   ```
4. Install the dependencies from the `pyproject.toml` using

   ```
   poetry install
   ```

## Running OSRM as backend

[This](https://download.openstreetmap.fr/extracts/asia/india/) site has the latest
OSRM extracts for India. Download the Karnataka extract and extract it to the
`data` folder ideally but this is very slow.

