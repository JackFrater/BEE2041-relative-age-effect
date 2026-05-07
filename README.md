# The Birth Timing Advantage: Uncovering the Relative Age Effect
## Research Quesiton 
Does the ***Relative Age Effect(RAE)*** persist at the elite level of international sport, and does it have varying affects on different countries and sports?

This project examines the ***Relative Age Effect(RAE)*** in World Cups squads for rugby and cricket. The RAE is a phenomenon that individuals born earlier in the selection year hold an advantage over peers born later in the year. 

This study compares South Africa (January 1st cutoff) and England (Spetember 1st cutoff) across two varying sports: Cricket and Rugby each require a different skill set with cricket being more technical and rugby more physical. 

## Key Findings
- Relative Age Effect presence: Our anaylsis shows that at the elite level there is limited evidence of statistical significance of the RAE.
- Sporting Divergence: Cricket cohorts exhibit a potential "reverse RAE" (though non-significant), where as rugby displays a more traditional RAE signal (though non-significant)
- Normalisation: By normalising the the year to nation cutoffs, our models explainitory power increase significantly.

## Technology Stack
- Language: Python 3.x
- Libraires: 
     - Data collection: `beautifulsoup4` and `requests` (Web scraping), `lxml` (HTML parsing).
     - Modeling and Analysis: `pandas` (Data Manipulation),  `statsmodels` (Poisson & OLS regression), `scipy` (Statistical distributions)
     - Infrastucture: `numpy` ( Numerical computing)
     - Visualisations: `seaborn`/`matplotlib` (Kernel Density Estimation(KDE) visualisations)

## Project Structure
```text
├── data/
│   ├── raw/
│   └── clean/
├── images/
├── output/
│   └── figures/
├── scripts/
│   └── data_collection.py
├── blog.ipynb
├── README.md   
└── requirements.txt
``` 

## Limitations
- Small sample size (N=103)
- Results not statistically significant
- Potential national development mismatches due to player migration
- Wikipedia data reliability constraints


## How To Replicate:
1. Clone the repository: 
```bash
git clone https://github.com/JackFrater/BEE2041-relative-age-effect
``` 
2. Install Libraries:
```bash
pip install -r requirements.txt
```
3. Run the Analysis:
```bash
 Run `blog.ipynb` in VS Code or Jupter Notebook and execute all cells.
 ```

 ## Conclusion 
 The findings suggest while directional patterns may appear in some cohorts, there is limited evidence statistically significant evidence of the Relative Age Effect at the eltie international level. 


         