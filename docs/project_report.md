# FuzzyFit: Adaptive Workout Intensity & Recovery Guide
## Final Project Report for CENG 386 - Fuzzy Logic

### Abstract
This project presents a Fuzzy Logic-based Personal Fitness Assistant designed to determine optimal workout intensity and volume based on a user's daily physiological and psychological state. Unlike static workout plans, this system models the "fuzzy" nature of human readiness using variables such as Sleep Quality, Muscle Soreness, Energy Level, and Stress Level. The system utilizes Mamdani inference and centroid defuzzification to generate crisp workout recommendations. Furthermore, the project features a modern, interactive web-based graphical user interface designed in accordance with Gestalt UI/UX principles.

---

### 1. Introduction
Traditional fitness applications often rely on rigid, binary logic or predefined calendars. However, human recovery is inherently ambiguous. A user might feel "somewhat tired" or have had an "average night of sleep." Fuzzy logic is uniquely suited to handle this linguistic ambiguity. The objective of this project is to build a robust Fuzzy Inference System (FIS) that maps linguistic inputs regarding a user's daily status to continuous workout recommendations.

### 2. System Design & Variables (Fuzzification)
The FIS takes four crisp inputs and produces two crisp outputs. We mapped these variables using Triangular (`trimf`) and Trapezoidal (`trapmf`) membership functions to ensure smooth transitions between states.

**Inputs (Antecedents):**
1. **Sleep Quality (0-10):** Poor [0,0,3,5], Average [4,6,8], Good [7,9,10,10]
2. **Muscle Soreness (0-10):** Low [0,0,2,4], Moderate [3,5,7], High [6,8,10,10]
3. **Energy Level (0-10):** Deficit [0,0,3,5], Balanced [4,6,8], Surplus [7,9,10,10]
4. **Stress Level (0-10):** Low [0,0,2,4], Normal [3,5,7], High [6,8,10,10]

**Outputs (Consequents):**
1. **Workout Intensity (0-100%):** Very Light, Light, Moderate, High, Maximum
2. **Workout Volume (0-120 Min):** Low, Medium, High

### 3. Rule Base & Inference
The system uses the **Mamdani Inference Method**. A comprehensive set of 18 rules was developed to cover the input space and prevent "dead zones" where no rules are activated. 

*Examples:*
* **Rule 1 (Extreme Fatigue):** IF Sleep is Poor OR Soreness is High OR Stress is High THEN Intensity is Very Light and Volume is Low.
* **Rule 2 (Optimal State):** IF Sleep is Good AND Soreness is Low AND Energy is Surplus AND Stress is Low THEN Intensity is Maximum and Volume is High.
* **Rule 3 (Average Day):** IF Sleep is Average AND Soreness is Moderate AND Energy is Balanced THEN Intensity is Moderate and Volume is Medium.

*Aggregation & Implication:* The logic utilizes MIN for the fuzzy AND operator and MAX for the fuzzy OR operator. The implication method used for rule evaluation is minimum truncation.

### 4. Defuzzification & Control Surfaces
To convert the fuzzy output sets back into actionable, crisp values, the **Centroid (Center of Gravity)** defuzzification method is used by default. The system architecture also supports dynamic switching to Bisector, Mean of Maximum (MOM), Smallest of Maximum (SOM), and Largest of Maximum (LOM) for comparative analysis.

**3D Control Surfaces:**
To analyze the non-linear decision boundaries of the system, 3D control surfaces were plotted. For example, by fixing Stress and Soreness at 5.0, we can visualize a 3D surface showing how the interaction between Sleep Quality and Energy Level directly manipulates Workout Intensity.

### 5. Technology Stack Justification (Python vs. MATLAB)
While MATLAB provides a visual Fuzzy Logic Toolbox, **Python (`scikit-fuzzy`) combined with `Streamlit` and `Plotly`** was chosen for this project for several critical academic and practical reasons:

1. **Real-world Application:** Python allows the FIS to be deployed as a standalone, interactive web application rather than a script confined to a MATLAB environment.
2. **Advanced UI/UX & Gestalt Principles:** The project incorporates modern UI design principles (Proximity, Common Region, Figure/Ground) which are highly difficult to implement in standard MATLAB GUI tools (App Designer). The interface enhances user accessibility.
3. **Interactive 3D Rendering:** Utilizing `Plotly`, the 3D control surfaces are fully interactive (zoom, pan, rotate) directly within the browser, providing a superior analytical experience compared to static MATLAB `surf()` plots.

### 6. Conclusion
The FuzzyFit project successfully demonstrates the application of fuzzy set theory to human physiology and fitness planning. By utilizing Python, the project not only fulfills the mathematical and logical requirements of a Fuzzy Inference System but also delivers a polished, user-centric software product.
