# Introduction

Methane (CH4) is one of the primary greenhouse gases responsible for the increase in global temperatures. Detecting and quantifying methane emissions is vital for both the scientific community and environmental policymakers. This project presents a solution developed during a Hackathon to detect methane plumes using computer vision AI techniques.

# Methallite

We use computer vision to recognise methane plumes on satellite images. This repository provides access to solution that we are using - an app that is able to predict risk that a satellite image contains a methane plume.

# Dataset

The dataset used comprises 64x64 greyscale satellite images capturing areas suspected of methane emissions. Each image is labeled with bounding boxes indicating the presence of a methane plume.

# Importance
Detecting methane plumes in real-time offers numerous benefits:

- Environmental Conservation: By identifying methane hotspots, necessary measures can be taken to reduce emissions, thereby conserving the environment.
- Policy Framework: Accurate data on methane emissions can guide environmental policies, regulations, and mitigation strategies.
- Public Awareness: Transparency in data can create public awareness and drive community efforts towards sustainability.

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

# Acknowledgements

Thanks to our McKinsey technical and business mentors.

# Contributors

Matthieu Nordin
Zofia Smoleń
Madhura Nirale
Aristide Guasquet
Timothée Gypteau
Kenzo Bounegta
