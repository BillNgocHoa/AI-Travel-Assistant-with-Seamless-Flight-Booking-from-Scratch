# SkyMate: AI Travel Assistant with Seamless Flight Booking from Scratch

This project is a scratch-built, **NLP-based AI chatbot** designed for a travel agency. It can **book flights**, **answer questions**, **manage user identity**,  and handle **small talk** — all through a natural, interactive conversation. The chatbot guides users through the full flight booking process with robust intent recognition, clear prompts, and real-time error handling.

[Detailed_Report.pdf](https://github.com/user-attachments/files/21684515/Report-NgocNguyen_Submitted.pdf)

Demonstrated Video: https://youtu.be/RJpiHTrE57Q 

> ✈️ **Goal:** Deliver a smooth, human-like travel assistant and booking experience using modular NLP design and smart conversational flow.

---

## 🧠 Core Features

- 💬 **Flight Booking Transactions**  
  Step-by-step dialogue system with backtracking, restarts, and confirmations.
  
- 🧭 **Intent Classification**  
  Classifies user intent into booking, small talk, identity requests, or general queries using TF-IDF + cosine similarity.

- 👤 **Identity Management**  
  Dynamically stores user data (name, age, preferences) using POS + NER for personalisation.

- ❓ **FAQ & Question Answering**  
  Efficient similarity matching from a pre-defined dataset for fast, relevant answers.

- 😄 **Small Talk Engine**  
  Responds to casual dialogue and fallback topics, enhancing naturalness.

- 🔄 **Context Tracking with Stack**  
  Maintains conversation state and navigation across booking stages.

---

## 🧪 Methodology at a Glance

- **Text Preprocessing**
  - Lowercasing, tokenization, stopword removal, lemmatization, and symbol cleaning.
  - Two modes: with/without stopword removal for different NLP pipelines.

- **Intent Matching**
  - TF-IDF + cosine similarity (lightweight and effective).
  - 4-class intent detection with 0.3 threshold filter.

- **Conversational Flow Design**
  - Prompts show next steps and confirm actions.
  - Visual confirmation of ticket details and guided responses.
  - Handles negation (“go back”, “restart”, “cancel”) with reprompt strategies.

- **POS + NER Tagging**
  - For name, place, and age detection in user input.
  - Ensures flexible natural input handling.

---

## 📊 Results & Impact

The chatbot was tested with 4 users across different tech backgrounds.

### ✅ Usability Highlights:
- **Personalization:** Remembers names, flight info, and preferences.
- **Clarity:** Structured prompts like “Let’s move to the next step: Payment” increased confidence.
- **Discoverability:** "What can you do?" command lets users navigate more easily.
- **Error Handling:** Smart fallbacks for invalid input, misformatted dates, and unsupported routes.

### 📈 Performance Snapshot:
| Metric                      | Result                       |
|----------------------------|------------------------------|
| Intent Matching Accuracy   | 85% (9/12 correctly classified) |
| Booking Robustness         | Full flow handled w/o error   |
| System Responsiveness      | Fast on all user actions      |
| Memory Usage               | Stable during execution       |

---

## 🛠️ Tech Stack

- Python
- TF-IDF, Cosine Similarity
- POS & Named Entity Recognition (spaCy/NLTK)
- Modular Class-Based Design

---

## 🧾 License

This project is released under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.  
You are free to learn from and adapt the code for **non-commercial purposes only**, with attribution.  
Commercial use is strictly prohibited.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## ✍️ Author

**Ngoc Hoa Nguyen**  

BSc Hons Computer Science, University of Nottingham

**Portfolio**: https://mavenshowcase.com/profile/48d1b3e0-4041-70ba-5a7f-4b39e89b3bc2

**LinkedIn**: https://www.linkedin.com/in/billngochoa/ 

