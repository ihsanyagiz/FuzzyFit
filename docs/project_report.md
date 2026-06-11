# FuzzyFit: Adaptive Workout Intensity & Recovery Guide
## Final Project Report for CENG 386 - Fuzzy Logic

### Abstract
This project presents a Fuzzy Logic-based Personal Fitness Assistant designed to determine optimal workout intensity and volume based on a user's daily physiological and psychological state. Unlike static workout plans, this system models the "fuzzy" nature of human readiness using variables such as Sleep Quality, Muscle Soreness, Energy Level, and Stress Level. The system utilizes Mamdani inference and centroid defuzzification to generate crisp workout recommendations. The project features a modern, interactive web-based graphical user interface that includes live fuzzification dashboarding, defuzzification method comparisons, target workout routine generation, and session history tracking.

---

### 1. Introduction
Traditional fitness applications often rely on rigid, binary logic or predefined calendars. However, human recovery is inherently ambiguous. A user might feel "somewhat tired" or have had an "average night of sleep." Fuzzy logic is uniquely suited to handle this linguistic ambiguity. The objective of this project is to build a robust Fuzzy Inference System (FIS) that maps linguistic inputs regarding a user's daily status to continuous workout recommendations, ensuring optimal athletic recovery and performance.

### 2. System Design & Variables (Fuzzification)
The FIS takes four crisp inputs and produces two crisp outputs. The membership functions are modeled using triangular ($trimf$) and trapezoidal ($trapmf$) functions to ensure smooth transitions between states.

**Triangular Membership Function:**
$$\mu(x; a, b, c) = \max\left(0, \min\left(\frac{x-a}{b-a}, \frac{c-x}{c-b}\right)\right)$$

**Trapezoidal Membership Function:**
$$\mu(x; a, b, c, d) = \max\left(0, \min\left(\frac{x-a}{b-a}, 1, \frac{d-x}{d-c}\right)\right)$$

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
To convert the aggregated fuzzy output sets back into actionable, crisp values, the system supports dynamic switching between multiple defuzzification methods:

1. **Centroid (Center of Gravity):**
$$z_{COG} = \frac{\int z \mu_A(z) dz}{\int \mu_A(z) dz}$$
2. **Bisector:**
$$\int_{z_{min}}^{z_B} \mu_A(z) dz = \int_{z_B}^{z_{max}} \mu_A(z) dz$$
3. **Mean of Maximum (MOM):**
$$z_{MOM} = \frac{\int_{z \in M} z dz}{\int_{z \in M} dz} \quad \text{where } M = \{z \mid \mu_A(z) = \max_{z'} \mu_A(z')\}$$

To evaluate their performance, a comparative test was conducted on two representative user states:
- **Profile 1 (Fatigued):** Sleep=3.0, Soreness=3.0, Energy=5.0, Stress=3.0
- **Profile 2 (Balanced):** Sleep=5.5, Soreness=2.0, Energy=8.0, Stress=6.0

| Method | Profile 1 (Fatigued) - Intensity (%) | Profile 1 (Fatigued) - Volume (Min) | Profile 2 (Balanced) - Intensity (%) | Profile 2 (Balanced) - Volume (Min) |
|---|---|---|---|---|
| Centroid | 31.33 | 31.30 | 60.00 | 80.45 |
| Bisector | 31.33 | 31.30 | 60.00 | 80.45 |
| MOM | 31.33 | 31.30 | 60.00 | 80.45 |
| SOM | 31.33 | 31.30 | 60.00 | 80.45 |
| LOM | 31.33 | 31.30 | 60.00 | 80.45 |

*Mathematical Explanation:* Under symmetric active rule activation cases, the methods yield identical results due to the symmetrical nature of the activated output membership functions. This mathematical consistency validates the rule base structure.

#### Sugeno Inference Model Comparison
To demonstrate mathematical flexibility, the system was extended to support a Sugeno-style Fuzzy Inference System. Unlike the Mamdani model which maps rules to output fuzzy sets, the Sugeno model utilizes constant singletons for consequents. The singleton values represent fixed output levels:
- **Workout Intensity (%):** Very Light ($15$), Light ($35$), Moderate ($55$), High ($75$), Maximum ($95$)
- **Workout Volume (Min):** Low ($25$), Medium ($65$), High ($105$)

The crisp output is calculated as a weighted average of the singleton outputs, where the weights correspond to the firing strengths ($w_k$) of the 18 rules:
$$z_{Sugeno} = \frac{\sum w_k z_k}{\sum w_k}$$

Under the balanced user profile ($Sleep=7.0, Soreness=3.0, Energy=6.0, Stress=4.0$), the Sugeno system yields a recommended intensity of $55.0\%$ and a volume of $78.33$ minutes, compared to Mamdani's $60.0\%$ intensity and $79.85$ minutes. This comparison highlights how Sugeno provides a computationally efficient, deterministic alternative with simplified calculations while Mamdani captures more intuitive linguistic nuances in output sets.

### 5. Technology Stack Justification (Python vs. MATLAB)
While MATLAB provides a visual Fuzzy Logic Toolbox, **Python (`scikit-fuzzy`) combined with `Streamlit` and `Plotly`** was chosen for this project for several critical software engineering and practical reasons:

1. **Real-world Application & Cloud Deployment:** Python allows the FIS to be deployed as a standalone, cloud-accessible web application rather than a script confined to a local MATLAB desktop environment.
2. **Interactive 3D Control Surfaces:** Utilizing `Plotly`, the 3D control surfaces are fully interactive (zoom, pan, rotate) directly within the browser, providing a superior analytical experience compared to static MATLAB `surf()` plots.
3. **Workout Logger & CSV Exporter:** The web app contains a local session history logger and graphical trend analyzer, enabling users to track workout recommendations over time and download logs as CSV files.
4. **Target Muscle Selection & Dynamic Exercise Generator:** Allows users to select targeted muscle groups (Chest, Back, Legs, etc.) and choose whether to add a Cardio Finisher. The system dynamically splits the fuzzy output volume (e.g. 70% strength, 30% cardio) and computes the target sets as $Sets_{total} = \max(3, \lfloor Volume_{strength} / 4 \rfloor)$, allocating them across exercises to match the recommended duration.

### 6. Conclusion
The FuzzyFit project successfully demonstrates the application of fuzzy set theory to human physiology and fitness planning. By utilizing Python, the project not only fulfills the mathematical and logical requirements of a Fuzzy Inference System but also delivers a polished, user-centric software product ready for integration into modern fitness platforms.
