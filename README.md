# Methallite
We use computer vision to recognise methane plumes on satellite images. This repository provides access to solution that we are using - an app that is able to predict risk that a satellite image contains a methane plume.

## Structure of the project

- notebooks: the best performing models that we tested
- src
  - app_utils: contents of an app
      - assets
          - left_panel.py
          - right_panel.py 
      - utils
          - main_app.py  (contains the main script of the app)
          - main_solution.py (contains the function running the model inference to be called in the app)
- requirements.txt (contains different libraries to be imported)
- .gitignore
- LICENSE
- README.md
