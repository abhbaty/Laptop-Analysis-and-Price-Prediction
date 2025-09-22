# 💻 Laptop Analysis and Price Prediction  

## 💻 Project Overview  
Laptop prices vary significantly due to factors like brand reputation, specifications, and market dynamics. This project leverages **machine learning** to analyze laptop specifications and predict their prices accurately.  

The goal is to:  
- Help **buyers** make informed purchase decisions.  
- Assist **retailers** in setting competitive prices.  
- Provide **market insights** into key features driving laptop pricing.  


## 💻 Objectives  
- Perform **Exploratory Data Analysis (EDA)** to uncover pricing patterns.  
- Engineer new **features** (e.g., touchscreen, PPI, CPU brand).  
- Apply and compare **machine learning models**.  
- Identify the most influential factors affecting laptop prices.  
- Build a predictive system with strong generalization performance.  


## 💻 Dataset  
The dataset consists of **1303 laptop entries**, each described by **12 key features**:  

- `Company` – Manufacturer brand  
- `TypeName` – Category (Gaming, Business, Ultrabook, etc.)  
- `Inches` – Screen size  
- `ScreenResolution` – Display details  
- `Cpu` – Processor type  
- `Ram` – Memory (GB)  
- `Memory` – Storage type & capacity  
- `Gpu` – Graphics card  
- `OpSys` – Operating system  
- `Weight` – Laptop weight (kg)  
- `Price` – Target variable  


## ⚡ Exploratory Data Analysis (EDA)  
- **Price Distribution**: Skewed, normalized using log transformation.  
- **Key Drivers**:  
  - Apple & MSI laptops are premium.  
  - Gaming & Workstation laptops are most expensive.  
  - Mac OS devices command higher prices than Windows/Linux.  


## ⚡ Feature Engineering  
- **Screen Features**: Touchscreen, IPS Panel, Resolution (X & Y), PPI.  
- **CPU Grouping**: Intel i3/i5/i7, Other Intel, AMD.  
- **Memory Features**: Split into HDD, SSD, Hybrid, Flash.  
- **GPU & OS Grouping**: Nvidia, Intel, AMD; Windows, Mac, Others.  


## ⚡ Modeling  
Machine learning models applied:  
- Linear Regression  
- K-Nearest Neighbors (KNN)  
- Support Vector Machine (SVM)  
- Decision Tree  
- Random Forest  

### ⚡ Best Model: Random Forest  
- **R² Score:** 0.82  
- Strong predictive accuracy on unseen data.  
- Key Features: RAM, SSD, CPU brand, GPU brand, and PPI.  


## ⚡ Business Applications  
- **For Manufacturers**: Optimize pricing strategies & production planning.  
- **For Retailers**: Dynamic pricing and inventory management.  
- **For Consumers**: Identify fair laptop prices and make better purchase decisions.  


## ⚡ Deployment  
The project includes:  
- **Jupyter Notebook** for full analysis.  
- **Streamlit App** for interactive price prediction.  
- **GitHub Repository** with preprocessing, model training, and evaluation.  

❤️ **Presentation Link**: [View Project Presentation](./P1.pptx)  
❤️ **Files Used**: [Laptop Analysis and Price Prediction](https://github.com/abhbaty/Laptop-Analysis-and-Price-Prediction)  


## ⚡ Future Enhancements  
- Handle extreme outliers more effectively.  
- Periodic retraining with new laptop models & specifications.  
- Extend prediction system to other electronic devices.  
