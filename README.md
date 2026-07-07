# 🏎️ ApexRace AI  
## F1 Tire Degradation, Pit Strategy & Race Pace Analytics Dashboard

ApexRace AI is an interactive Formula 1 sports analytics dashboard that analyzes lap-by-lap race data to understand whether a driver’s race performance was affected by **tire degradation**, **pit-stop timing**, or **race pace consistency**.

Built for the **AQX Sports Analytics Data Bowl 2.0**, this project turns real Formula 1 race data into clean strategy insights, interactive charts, driver comparisons, and a strategy scorecard.

---

## 🌐 Live Demo

🚀 **Live App:**  
https://apexrace-ai.streamlit.app/

📂 **GitHub Repository:**  
https://github.com/dharmiknakrani26/ApexRace-AI

---

## 🚀 Project Overview

Formula 1 race results usually show the final finishing order, fastest laps, and pit stops. However, they do not always explain **why** a driver gained or lost performance during the race.

ApexRace AI solves this problem by transforming raw F1 race data into a clean, visual, and actionable dashboard. It helps users answer one key question:

> **Was the driver’s race result affected more by tire wear, pit strategy, or inconsistent race pace?**

---

## 🎯 Problem Statement

In Formula 1, race performance is shaped by multiple connected factors:

- Tire degradation  
- Pit-stop timing  
- Race pace consistency  
- Stint length  
- Tire compound choice  
- Strategy execution  

Traditional race summaries do not clearly show when a driver started losing pace, whether they pitted at the right time, or how consistent they were compared to another driver.

ApexRace AI provides a data-driven way to analyze those factors using real Formula 1 race data.

---

## ✅ Solution

ApexRace AI provides an interactive Streamlit dashboard where users can:

- Select an F1 season and race
- Select a driver using full driver names
- Compare two drivers
- Analyze clean race pace trends
- Detect tire degradation patterns
- Review pit-stop strategy
- Generate a strategy score
- Understand race performance through a clear summary

The dashboard converts raw lap data into simple insights that fans, analysts, and strategy learners can understand quickly.

---

## ✨ Key Features

### 🏁 Race Selection  
Users can select the season, race, and driver from dropdown menus.

### 👤 Full Driver Names  
Driver codes are converted into readable full names such as:

```text
Max Verstappen (VER)
Lando Norris (NOR)
Charles Leclerc (LEC)
```

### 📊 Clean Race Pace Trend  
The dashboard removes pit laps and unusual slow laps to show a cleaner view of race pace.

### 🛞 Tire Degradation Analysis  
Shows how lap time changes as tire age increases. This helps identify when tire performance begins to drop.

### 🧠 Strategy Scorecard  
ApexRace AI calculates a strategy score out of 100 using:

- Tire degradation risk
- Pit timing rating
- Race pace consistency

### ⏱️ Pit Stop Strategy Analysis  
Shows each stint, tire compound, average lap time, and suggested pit window.

### 🆚 Driver Comparison  
Compare two drivers based on:

- Average clean lap time
- Best clean lap time
- Consistency score
- Pit stops
- Race pace trend

### 📝 Race Insight Summary  
Generates a clear summary explaining the driver’s performance, strategy score, tire risk, pit timing, and actionable impact.

### 🎨 Professional F1 Dashboard UI  
The app includes a dark racing-style layout with animated cards, metric panels, and a race-control dashboard feel.

---

## 🧮 Analytics Methodology

ApexRace AI uses lap-by-lap data and applies simple but useful analytics logic.

### 1. Clean Lap Filtering

The app removes:

- Pit-in laps
- Pit-out laps
- Missing lap times
- Extreme outlier laps
- Unreliable laps when available

This helps create a better view of true race pace.

### 2. Race Pace Consistency

The dashboard calculates consistency using lap-time variation. Lower variation means the driver maintained more stable pace.

### 3. Tire Degradation Risk

The app analyzes whether lap time increases as tire age increases.

Risk levels:

```text
Low      = tire performance stayed mostly stable
Medium   = moderate tire degradation detected
High     = strong lap-time increase as tires aged
Unknown  = not enough clean data
```

### 4. Suggested Pit Window

The dashboard estimates a possible pit window when tire performance begins to drop.

### 5. Strategy Score

The strategy score starts from 100 and applies deductions based on:

- Low consistency
- High tire degradation
- Early or late pit timing
- No pit stop when tire drop is detected

Final status examples:

```text
Excellent Strategy
Good Strategy
Strategy Review Needed
High Strategy Risk
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web dashboard framework |
| FastF1 | Formula 1 race data |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical calculations |
| Plotly | Interactive charts |
| Streamlit Cloud | Live app deployment |

---

## 📁 Project Structure

```text
ApexRace-AI/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Files ignored by GitHub
│
├── data/
│   └── cache/          # FastF1 cache data
│
└── screenshots/        # Optional project screenshots
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dharmiknakrani26/ApexRace-AI.git
cd ApexRace-AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

For Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the App Locally

```bash
streamlit run app.py
```

---

## 📦 Requirements

```txt
streamlit
fastf1
pandas
numpy
plotly
scikit-learn
```

---

## 📊 Example Use Case

A user selects:

```text
Season: 2025
Race: Australian Grand Prix
Driver: Lando Norris (NOR)
Compare With: Max Verstappen (VER)
```

ApexRace AI then shows:

- Clean race pace trend
- Tire degradation chart
- Pit stop strategy table
- Strategy score
- Driver comparison
- Race insight summary

---

## 💡 Project Impact

ApexRace AI helps make Formula 1 strategy easier to understand.

Instead of only showing the final race result, the dashboard explains:

- When the driver started losing pace
- Whether tire degradation affected performance
- Whether the pit stop timing looked good
- Which driver had stronger clean race pace
- How consistent the driver was over the race

This can be useful for:

- F1 fans
- Sports analysts
- Strategy learners
- Data science students
- Fantasy sports users
- Racing content creators

---

## 🔮 Future Improvements

Future versions of ApexRace AI could include:

- Machine learning lap-time prediction
- Weather impact analysis
- Safety car strategy analysis
- Undercut and overcut detection
- Team-level strategy comparison
- Race position change tracking
- PDF race report export
- AI-generated strategy recommendation
- More advanced predictive race strategy modeling

---

## ⚠️ Limitations

- Future races may not load until race data becomes available through FastF1.
- Tire degradation estimates are based on lap-time patterns and may be affected by traffic, safety cars, weather, fuel load, or race incidents.
- The strategy score is an analytical indicator, not an official Formula 1 strategy model.
- Some race sessions may have incomplete or missing data.

---

## 👨‍💻 Author

**Dharmik Nakrani**

Data Analytics & AI Enthusiast  
Built with Python, Streamlit, FastF1, Pandas, NumPy, and Plotly.

---

## 📌 Project Tagline

> **ApexRace AI turns Formula 1 lap data into clear race strategy intelligence.**
