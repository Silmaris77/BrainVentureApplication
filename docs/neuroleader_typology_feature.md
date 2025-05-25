# Neurolider Typology Feature Documentation

## Overview

The Neurolider Typology feature is a core component of the BrainVenture application that provides users with insights into their leadership style from a neurobiological perspective. This feature classifies users into six different neurolider types and offers personalized recommendations based on their results.

## Key Components

### 1. Neurolider Types

The feature defines six neurolider types, each with its own neurobiological profile:

1. **Neuroanalityk (Neuroanalyst)** - Risk-avoidant leader with high amygdala activity
2. **Neuroreaktor (Neuroreactor)** - Impulsive guardian with high limbic system activity
3. **Neurobalanser (Neurobalancer)** - Balanced integrator with equilibrium between prefrontal cortex and limbic system
4. **Neuroempata (Neuroempathist)** - Relationship architect with high oxytocin system activity
5. **Neuroinnowator (Neuroinnovator)** - Change navigator with high neuroplasticity
6. **Neuroinspirator (Neuroinspirer)** - Charismatic visionary with strong limbic system activity

### 2. Diagnostic Test

The diagnostic test consists of 30 questions that measure different aspects of leadership style. Each question is associated with one of the six neurolider types.

### 3. Results Analysis

The system calculates the user's scores for each type and determines:
- Dominant neurolider type
- Secondary neurolider type
- Full neuroleader profile visualized on a radar chart

### 4. Recommendations

Based on the user's dominant type, the system provides:
- Personalized development recommendations
- Book recommendations
- Course suggestions
- Development exercises
- Useful tools and resources

### 5. User Data Persistence

The feature saves the user's test results to enable:
- Historical tracking of test results
- Analysis of changes in leadership style over time
- Comparison between different test attempts

## Technical Implementation

### Core Files:

1. **`utils/neuroleader_types_new.py`** - Core class that manages all neurolider typology functionality
2. **`data/content/neuroleader_types.json`** - Basic data about each neurolider type
3. **`data/content/neuroleader_type_test.json`** - Test questions and scoring logic
4. **`data/content/neuroleader_types/*.md`** - Detailed descriptions for each neurolider type
5. **`pages/5_Typy_Neuroliderow_new.py`** - Main page for taking the test and viewing results

### User Data Storage:

Test results are stored in the user data JSON file (`data/content/user_data.json`) in the `neuroleader_tests` array, allowing for multiple test results to be tracked over time.

## Images

The feature includes two types of images for each neurolider type:
1. **Representative image** - Visual representation of each type
2. **Brain activity visualization** - Illustrates the neurological basis of each type

## Future Developments

Planned enhancements for this feature include:

1. **Trend Analysis** - Visualizing how a user's neurolider profile changes over time
2. **Team Compatibility** - Analyzing team composition based on neurolider types
3. **Expanded Resources** - Adding more personalized resources and development paths
4. **Interactive Exercises** - Creating interactive exercises specific to each neurolider type
5. **PDF Report Generation** - Allowing users to download a detailed report of their results

## Usage

To access this feature:
1. Navigate to "Typy Neuroliderów" in the sidebar menu
2. Choose to explore the types or take the diagnostic test
3. Once completed, view your results in the "Twój Profil" tab
4. Access your historical test results by toggling "Pokaż historię testów"

A shortcut to your most recent neurolider type is also available on the Dashboard.
